import datetime as dt
import requests
import base64
from urllib.parse import urlencode
from typing import Any, Iterable
from flask import current_app
from collections.abc import Collection

from core.helpers import get_missing_keys, LoadFromEnvMixin, truncate_text
from core.client.base import Client, SUCCESS_STATUSES
from core.client.spotify.models import SpotifyUser, SpotifyTrack, SpotifyPlaylist

# TODO: use cache to save requests made
class SpotifyClient(Client, LoadFromEnvMixin):
    SPOTIFY_AUTH_URL = 'https://accounts.spotify.com'
    SPOTIFY_API_URL = 'https://api.spotify.com/v1'

    SCOPES = (
        'playlist-read-private',
        'playlist-read-collaborative',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-top-read',
        'user-read-email'
    )

    client_secret = None
    client_id = None

    load_from_env = {
        'client_secret': 'SPOTIFY_CLIENT_SECRET',
        'client_id': 'SPOTIFY_CLIENT_ID'
    }

    def _make_request(self,
                      method: str,
                      keys_to_check: Iterable[str] = [],
                      **request_kwargs: Any) -> dict[str, Any]:
        current_app.logger.debug(
            f'{method.upper()} Request to Spotify API: {request_kwargs}')
        
        r = requests.request(method.upper(), **request_kwargs)

        current_app.logger.debug(
            f'{r.status_code} Response from Spotify API: {truncate_text(r.text, 100)}')
        
        if r.status_code not in SUCCESS_STATUSES:
            raise Exception(f"Error {r.status_code} received from Spotify API")
        
        resp: dict[str, Any] = r.json()

        missing_keys = get_missing_keys(resp, *keys_to_check)
        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found in response.")
        
        return resp

    def generate_auth_url(self, redirect_url: str, state: str | None = None) -> str:
        query_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': ' '.join(self.SCOPES),
            'show_dialog': False
        }

        if state is not None:
            query_params['state'] = state

        return f'{self.SPOTIFY_AUTH_URL}/authorize?{urlencode(query_params)}'
    
    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        auth_code = kwargs.get('auth_code')
        redirect_url = kwargs.get('redirect_url')
        
        body = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_url
        }
        b64_auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()).decode()
        headers = {
            'Authorization': f'Basic {b64_auth_string}'
        }
        
        keys_to_check = ('access_token', 'refresh_token', 'expires_in')
        resp = self._make_request(method='post', 
                                  keys_to_check=keys_to_check,
                                  url=f'{self.SPOTIFY_AUTH_URL}/api/token',
                                  data=body,
                                  headers=headers)
        
        expiry_date = dt.datetime.now() + dt.timedelta(seconds=resp['expires_in'])
        return {
            'token': resp['access_token'],
            'refresh_token': resp['refresh_token'],
            'expiry_date': expiry_date
        }
    
    def handle_token_refresh(self,
                             token: str,
                             refresh_token: str,
                             expiry_date: dt.datetime) -> dict[str, Any]:
        if dt.datetime.now() < expiry_date:
            return {
                'token': token,
                'expiry_date': expiry_date,
                'refreshed': False
            }
        
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id
        }
        b64_auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()).decode()
        headers = {
            'Authorization': f'Basic {b64_auth_string}'
        }

        keys_to_check = ('access_token', 'expires_in')
        resp = self._make_request(method='post',
                                  keys_to_check=keys_to_check,
                                  url=f'{self.SPOTIFY_AUTH_URL}/api/token',
                                  data=body,
                                  headers=headers)
        
        new_expiry_date = dt.datetime.now() + dt.timedelta(seconds=resp['expires_in'])
        return {
            'token': resp['access_token'],
            'expiry_date': new_expiry_date,
            'refreshed': True
        }
    
    def get_user(self, user_identifier: str) -> SpotifyUser:        
        resp = self._make_request(
            method='get',
            url=f'{self.SPOTIFY_API_URL}/me',
            headers={'Authorization': f'Bearer {user_identifier}'})
        return SpotifyUser.from_api_response(resp)
    
    # ignoring type here as I'm pretty sure there is a bug in mypy
    def get_top_tracks_from_user(self, user: SpotifyUser, amount: int = 50) -> list[SpotifyTrack]: # type: ignore
        # could move validation logic to _make_request
        offset = 0
        max_limit = 50
        remaining = amount
        time_range = 'short_term'

        tracks: list[SpotifyTrack] = []
        while remaining > 0:
            current_app.logger.debug(f"'remaining', {remaining}, 'max_limit', {max_limit}")
            if remaining < max_limit:
                limit = remaining
            else:
                limit = max_limit

            query_params = {
                'time_range': time_range, #TODO: make this customizable
                'limit': limit,
                'offset': offset
            }

            resp = self._make_request(method='get',
                                      url=f'{self.SPOTIFY_API_URL}/me/top/tracks',
                                      params=query_params,
                                      headers={'Authorization': f'Bearer {user.token}'})
            
            if resp['total'] < amount:
                current_app.logger.info(
                    f"User {user.email}'s top tracks from last month arent enough."
                    f"Amount requested: {amount}, total: {resp['total']}.")
                time_range = 'medium_term'
                continue
                
            tracks += [SpotifyTrack.from_api_response(track) for track in resp["items"]]
            offset += limit
            remaining -= limit
        
        return tracks
    
    def create_playlist(self,
                        *,
                        user: SpotifyUser,
                        name: str,
                        public: bool,
                        collaborative: bool,
                        description: str) -> SpotifyPlaylist:
        
        resp = self._make_request(
            'post',
            ['id'],
            url=f'{self.SPOTIFY_API_URL}/users/{user.api_id}/playlists',
            json={
                'name': name,
                'public': public,
                'collaborative': collaborative,
                'description': description
            },
            headers={'Authorization': f'Bearer {user.token}'}
        )
        
        return SpotifyPlaylist.from_api_response(resp)

    def update_playlist_tracks(self, user: SpotifyUser, playlist: SpotifyPlaylist, tracks: list[SpotifyTrack]) -> str:
        resp = self._make_request(
            'put',
            ['snapshot_id'],
            url=f'{self.SPOTIFY_API_URL}/playlists/{playlist.id}/tracks',
            json={'uris': [t.uri for t in tracks]},
            headers={'Authorization': f'Bearer {user.token}'}
        )
        
        snapshot_id: str = resp['snapshot_id']
        return snapshot_id
    
SpotifyUser._client_cls = SpotifyClient