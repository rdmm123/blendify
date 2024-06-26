import { BlendResponse, User, UserResponse, UserSessionResponse, Playlist, ErrorResponse } from "./api.types";

const API_URL = BACKEND_HOST + '/api';

export const fetchCurrentUser = async () => {
    const response = await fetch(API_URL + '/users/me', {credentials: 'include'})

    if (!response.ok) {
        return null
    }

    const userResponse: UserResponse = await response.json()
    
    return userResponse.user;
}

export const fetchUserSession = async ({ id }: User) => {
    const response = await fetch(`${API_URL}/users/${id}/session`)

    if (!response.ok) {
        return null
    }

    const userSessionResponse: UserSessionResponse = await response.json()
    
    return userSessionResponse.session;
}

export const createBlend = async (users: User[], playlistLength: number, create: boolean = false) => {
    let response;
    try {
        response = await fetch(`${API_URL}/blender/blend`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
              },
            body: JSON.stringify({
                users: users.map(user => user.id),
                playlist_length: playlistLength,
                create: create
            })
        })
    } catch {
        return {
            isSuccess: false,
            message: `An unknown error has ocurred. Please try again later.`,
            playlist: { tracks: [] } as Playlist
        }
    }

    if (!response.ok) {
        const errorResponse: ErrorResponse = await response.json()
        return {
            isSuccess: false,
            message: `Ooops! Something went wrong: ${errorResponse.message}. Please try again later.`,
            playlist: { tracks: [] } as Playlist
        }
    }

    const blendResponse: BlendResponse = await response.json()
    const playlist: Playlist = { ...blendResponse.playlist, tracks: [] };
    
    playlist.tracks = blendResponse.playlist.tracks.map(track => ({
        ...track,
        user: users.filter(user => user.id === track.user)[0]
    }))

    return { isSuccess: true, playlist };
}