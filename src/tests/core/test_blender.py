import pytest
from pytest_unordered import unordered

from src.tests.core.mocks.mock_client import MockClient
from src.core.blender import Blender
from src.core.client.base import User, Track, Artist

RESULT_NO_CONFLICTS = [
    Track(
        name="Not Like Us",
        external_url="https://test.api.com/track/not-like-us",
        uri="uri:track:not-like-us",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="Not Like Us",
        cover_art="https://test.api.com/track/not-like-us/cover",
        preview="https://test.api.com/track/not-like-us/preview",
        user="user_1",
    ),
    Track(
        name="VOYCONTODO",
        external_url="https://test.api.com/track/voycontodo",
        uri="uri:track:voycontodo",
        artists=[
            Artist(name="Ralphie Choo", url="https://test.api.com/artist/ralphie-choo")
        ],
        album="SUPERNOVA",
        cover_art="https://test.api.com/track/voycontodo/cover",
        preview="https://test.api.com/track/voycontodo/preview",
        user="user_2",
    ),
    Track(
        name="euphoria",
        external_url="https://test.api.com/track/euphoria",
        uri="uri:track:euphoria",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="euphoria",
        cover_art="https://test.api.com/track/euphoria/cover",
        preview="https://test.api.com/track/euphoria/preview",
        user="user_1",
    ),
    Track(
        name="Sublime",
        external_url="https://test.api.com/track/sublime",
        uri="uri:track:sublime",
        artists=[Artist(name="Sen Senra", url="https://test.api.com/artist/sen-senra")],
        album="Corazón Cromado",
        cover_art="https://test.api.com/track/sublime/cover",
        preview="https://test.api.com/track/sublime/preview",
        user="user_2",
    ),
    Track(
        name="Flow de Pueblo",
        external_url="https://test.api.com/track/flow-de-pueblo",
        uri="uri:track:flow-de-pueblo",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/flow-de-pueblo/cover",
        preview="https://test.api.com/track/flow-de-pueblo/preview",
        user="user_1",
    ),
    Track(
        name="El Sentido de la Vida",
        external_url="https://test.api.com/track/el-sentido-de-la-vida",
        uri="uri:track:el-sentido-de-la-vida",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-sentido-de-la-vida/cover",
        preview="https://test.api.com/track/el-sentido-de-la-vida/preview",
        user="user_2",
    ),
    Track(
        name="meet the grahams",
        external_url="https://test.api.com/track/meet-the-grahams",
        uri="uri:track:meet-the-grahams",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="meet the grahams",
        cover_art="https://test.api.com/track/meet-the-grahams/cover",
        preview="https://test.api.com/track/meet-the-grahams/preview",
        user="user_1",
    ),
    Track(
        name="Ahora No Me Lloren",
        external_url="https://test.api.com/track/ahora-no-me-lloren",
        uri="uri:track:ahora-no-me-lloren",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/ahora-no-me-lloren/cover",
        preview="https://test.api.com/track/ahora-no-me-lloren/preview",
        user="user_2",
    ),
    Track(
        name="El Censor",
        external_url="https://test.api.com/track/el-censor",
        uri="uri:track:el-censor",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-censor/cover",
        preview="https://test.api.com/track/el-censor/preview",
        user="user_1",
    ),
    Track(
        name="TE VI EN MIS PESADILLAS",
        external_url="https://test.api.com/track/te-vi-en-mis-pesadillas",
        uri="uri:track:te-vi-en-mis-pesadillas",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/te-vi-en-mis-pesadillas/cover",
        preview="https://test.api.com/track/te-vi-en-mis-pesadillas/preview",
        user="user_2",
    ),
]

RESULT_REPEATING_DIFFERENT_SPOTS = [
    Track(
        name="Not Like Us",
        external_url="https://test.api.com/track/not-like-us",
        uri="uri:track:not-like-us",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="Not Like Us",
        cover_art="https://test.api.com/track/not-like-us/cover",
        preview="https://test.api.com/track/not-like-us/preview",
        user="user_1",
    ),
    Track(
        name="VOYCONTODO",
        external_url="https://test.api.com/track/voycontodo",
        uri="uri:track:voycontodo",
        artists=[
            Artist(name="Ralphie Choo", url="https://test.api.com/artist/ralphie-choo")
        ],
        album="SUPERNOVA",
        cover_art="https://test.api.com/track/voycontodo/cover",
        preview="https://test.api.com/track/voycontodo/preview",
        user="user_2",
    ),
    Track(
        name="euphoria",
        external_url="https://test.api.com/track/euphoria",
        uri="uri:track:euphoria",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="euphoria",
        cover_art="https://test.api.com/track/euphoria/cover",
        preview="https://test.api.com/track/euphoria/preview",
        user="user_1",
    ),
    Track(
        name="Sublime",
        external_url="https://test.api.com/track/sublime",
        uri="uri:track:sublime",
        artists=[Artist(name="Sen Senra", url="https://test.api.com/artist/sen-senra")],
        album="Corazón Cromado",
        cover_art="https://test.api.com/track/sublime/cover",
        preview="https://test.api.com/track/sublime/preview",
        user="user_2",
    ),
    Track(
        name="meet the grahams",
        external_url="https://test.api.com/track/meet-the-grahams",
        uri="uri:track:meet-the-grahams",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="meet the grahams",
        cover_art="https://test.api.com/track/meet-the-grahams/cover",
        preview="https://test.api.com/track/meet-the-grahams/preview",
        user="user_1",
    ),
    Track(
        name="El Sentido de la Vida",
        external_url="https://test.api.com/track/el-sentido-de-la-vida",
        uri="uri:track:el-sentido-de-la-vida",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-sentido-de-la-vida/cover",
        preview="https://test.api.com/track/el-sentido-de-la-vida/preview",
        user="user_2",
    ),
    Track(
        name="El Censor",
        external_url="https://test.api.com/track/el-censor",
        uri="uri:track:el-censor",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-censor/cover",
        preview="https://test.api.com/track/el-censor/preview",
        user="user_1",
    ),
    Track(
        name="TE VI EN MIS PESADILLAS",
        external_url="https://test.api.com/track/te-vi-en-mis-pesadillas",
        uri="uri:track:te-vi-en-mis-pesadillas",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/te-vi-en-mis-pesadillas/cover",
        preview="https://test.api.com/track/te-vi-en-mis-pesadillas/preview",
        user="user_2",
    ),
    Track(
        name="De la Rosa Prada",
        external_url="https://test.api.com/track/de-la-rosa-prada",
        uri="uri:track:de-la-rosa-prada",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/de-la-rosa-prada/cover",
        preview="https://test.api.com/track/de-la-rosa-prada/preview",
        user="user_1",
    ),
    Track(
        name="MAMI 100PRE SABE (INTERLUDE)",
        external_url="https://test.api.com/track/mami-100pre-sabe-(interlude)",
        uri="uri:track:mami-100pre-sabe-(interlude)",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/mami-100pre-sabe-(interlude)/cover",
        preview="https://test.api.com/track/mami-100pre-sabe-(interlude)/preview",
        user="user_2",
    ),
]

RESULT_REPEATING_EQUAL_SPOTS = [
    Track(
        name="Not Like Us",
        external_url="https://test.api.com/track/not-like-us",
        uri="uri:track:not-like-us",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="Not Like Us",
        cover_art="https://test.api.com/track/not-like-us/cover",
        preview="https://test.api.com/track/not-like-us/preview",
        user="user_1",
    ),
    Track(
        name="VOYCONTODO",
        external_url="https://test.api.com/track/voycontodo",
        uri="uri:track:voycontodo",
        artists=[
            Artist(name="Ralphie Choo", url="https://test.api.com/artist/ralphie-choo")
        ],
        album="SUPERNOVA",
        cover_art="https://test.api.com/track/voycontodo/cover",
        preview="https://test.api.com/track/voycontodo/preview",
        user="user_2",
    ),
    Track(
        name="euphoria",
        external_url="https://test.api.com/track/euphoria",
        uri="uri:track:euphoria",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="euphoria",
        cover_art="https://test.api.com/track/euphoria/cover",
        preview="https://test.api.com/track/euphoria/preview",
        user="user_1",
    ),
    Track(
        name="El Sentido de la Vida",
        external_url="https://test.api.com/track/el-sentido-de-la-vida",
        uri="uri:track:el-sentido-de-la-vida",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-sentido-de-la-vida/cover",
        preview="https://test.api.com/track/el-sentido-de-la-vida/preview",
        user="user_2",
    ),
    Track(
        name="Sublime",
        external_url="https://test.api.com/track/sublime",
        uri="uri:track:sublime",
        artists=[Artist(name="Sen Senra", url="https://test.api.com/artist/sen-senra")],
        album="Corazón Cromado",
        cover_art="https://test.api.com/track/sublime/cover",
        preview="https://test.api.com/track/sublime/preview",
        user="user_2",
    ),
    Track(
        name="meet the grahams",
        external_url="https://test.api.com/track/meet-the-grahams",
        uri="uri:track:meet-the-grahams",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="meet the grahams",
        cover_art="https://test.api.com/track/meet-the-grahams/cover",
        preview="https://test.api.com/track/meet-the-grahams/preview",
        user="user_1",
    ),
    Track(
        name="El Censor",
        external_url="https://test.api.com/track/el-censor",
        uri="uri:track:el-censor",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-censor/cover",
        preview="https://test.api.com/track/el-censor/preview",
        user="user_1",
    ),
    Track(
        name="TE VI EN MIS PESADILLAS",
        external_url="https://test.api.com/track/te-vi-en-mis-pesadillas",
        uri="uri:track:te-vi-en-mis-pesadillas",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/te-vi-en-mis-pesadillas/cover",
        preview="https://test.api.com/track/te-vi-en-mis-pesadillas/preview",
        user="user_2",
    ),
    Track(
        name="De la Rosa Prada",
        external_url="https://test.api.com/track/de-la-rosa-prada",
        uri="uri:track:de-la-rosa-prada",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/de-la-rosa-prada/cover",
        preview="https://test.api.com/track/de-la-rosa-prada/preview",
        user="user_1",
    ),
    Track(
        name="MAMI 100PRE SABE (INTERLUDE)",
        external_url="https://test.api.com/track/mami-100pre-sabe-(interlude)",
        uri="uri:track:mami-100pre-sabe-(interlude)",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/mami-100pre-sabe-(interlude)/cover",
        preview="https://test.api.com/track/mami-100pre-sabe-(interlude)/preview",
        user="user_2",
    ),
]

RESULT_REPEATING_EQUAL_SPOTS_UNEVEN_AMOUNT = [
    Track(
        name="Not Like Us",
        external_url="https://test.api.com/track/not-like-us",
        uri="uri:track:not-like-us",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="Not Like Us",
        cover_art="https://test.api.com/track/not-like-us/cover",
        preview="https://test.api.com/track/not-like-us/preview",
        user="user_1",
    ),
    Track(
        name="VOYCONTODO",
        external_url="https://test.api.com/track/voycontodo",
        uri="uri:track:voycontodo",
        artists=[
            Artist(name="Ralphie Choo", url="https://test.api.com/artist/ralphie-choo")
        ],
        album="SUPERNOVA",
        cover_art="https://test.api.com/track/voycontodo/cover",
        preview="https://test.api.com/track/voycontodo/preview",
        user="user_2",
    ),
    Track(
        name="euphoria",
        external_url="https://test.api.com/track/euphoria",
        uri="uri:track:euphoria",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="euphoria",
        cover_art="https://test.api.com/track/euphoria/cover",
        preview="https://test.api.com/track/euphoria/preview",
        user="user_1",
    ),
    Track(
        name="El Sentido de la Vida",
        external_url="https://test.api.com/track/el-sentido-de-la-vida",
        uri="uri:track:el-sentido-de-la-vida",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-sentido-de-la-vida/cover",
        preview="https://test.api.com/track/el-sentido-de-la-vida/preview",
        user="user_2",
    ),
    Track(
        name="Sublime",
        external_url="https://test.api.com/track/sublime",
        uri="uri:track:sublime",
        artists=[Artist(name="Sen Senra", url="https://test.api.com/artist/sen-senra")],
        album="Corazón Cromado",
        cover_art="https://test.api.com/track/sublime/cover",
        preview="https://test.api.com/track/sublime/preview",
        user="user_1",
    ),
    Track(
        name="TE VI EN MIS PESADILLAS",
        external_url="https://test.api.com/track/te-vi-en-mis-pesadillas",
        uri="uri:track:te-vi-en-mis-pesadillas",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/te-vi-en-mis-pesadillas/cover",
        preview="https://test.api.com/track/te-vi-en-mis-pesadillas/preview",
        user="user_2",
    ),
    Track(
        name="meet the grahams",
        external_url="https://test.api.com/track/meet-the-grahams",
        uri="uri:track:meet-the-grahams",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="meet the grahams",
        cover_art="https://test.api.com/track/meet-the-grahams/cover",
        preview="https://test.api.com/track/meet-the-grahams/preview",
        user="user_1",
    ),
    Track(
        name="MAMI 100PRE SABE (INTERLUDE)",
        external_url="https://test.api.com/track/mami-100pre-sabe-(interlude)",
        uri="uri:track:mami-100pre-sabe-(interlude)",
        artists=[
            Artist(name="Alvaro Diaz", url="https://test.api.com/artist/alvaro-diaz")
        ],
        album="SAYONARA",
        cover_art="https://test.api.com/track/mami-100pre-sabe-(interlude)/cover",
        preview="https://test.api.com/track/mami-100pre-sabe-(interlude)/preview",
        user="user_2",
    ),
    Track(
        name="El Censor",
        external_url="https://test.api.com/track/el-censor",
        uri="uri:track:el-censor",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-censor/cover",
        preview="https://test.api.com/track/el-censor/preview",
        user="user_1",
    ),
]

# As there is 1 user with an empty top, we will return half the playlist
RESULT_EMPTY_USER = [
    Track(
        name="Not Like Us",
        external_url="https://test.api.com/track/not-like-us",
        uri="uri:track:not-like-us",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="Not Like Us",
        cover_art="https://test.api.com/track/not-like-us/cover",
        preview="https://test.api.com/track/not-like-us/preview",
        user="user_1",
    ),
    Track(
        name="euphoria",
        external_url="https://test.api.com/track/euphoria",
        uri="uri:track:euphoria",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="euphoria",
        cover_art="https://test.api.com/track/euphoria/cover",
        preview="https://test.api.com/track/euphoria/preview",
        user="user_1",
    ),
    Track(
        name="Flow de Pueblo",
        external_url="https://test.api.com/track/flow-de-pueblo",
        uri="uri:track:flow-de-pueblo",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/flow-de-pueblo/cover",
        preview="https://test.api.com/track/flow-de-pueblo/preview",
        user="user_1",
    ),
    Track(
        name="meet the grahams",
        external_url="https://test.api.com/track/meet-the-grahams",
        uri="uri:track:meet-the-grahams",
        artists=[
            Artist(
                name="Kendrick Lamar", url="https://test.api.com/artist/kendrick-lamar"
            )
        ],
        album="meet the grahams",
        cover_art="https://test.api.com/track/meet-the-grahams/cover",
        preview="https://test.api.com/track/meet-the-grahams/preview",
        user="user_1",
    ),
    Track(
        name="El Censor",
        external_url="https://test.api.com/track/el-censor",
        uri="uri:track:el-censor",
        artists=[
            Artist(name="Nico Miseria", url="https://test.api.com/artist/nico-miseria")
        ],
        album="El Periplo del Héroe",
        cover_art="https://test.api.com/track/el-censor/cover",
        preview="https://test.api.com/track/el-censor/preview",
        user="user_1",
    ),
]


@pytest.fixture(scope="module")
def mock_client():
    return MockClient()


def test_blend_no_conflicts(mock_client):
    users = [
        User(
            id="user_1",
            api_id="no_conflicts",
            email="test@email.com",
            name="Test User 1",
        ),
        User(
            id="user_2",
            api_id="no_conflicts",
            email="test@email.com",
            name="Test User 2",
        ),
    ]
    blender = Blender(mock_client, users=users, playlist_length=10)

    playlist = blender.blend()
    assert playlist == unordered(RESULT_NO_CONFLICTS)


def test_blend_repeating_different_spots(mock_client):
    users = [
        User(
            id="user_1",
            api_id="repeating_different",
            email="test@email.com",
            name="Test User 1",
        ),
        User(
            id="user_2",
            api_id="repeating_different",
            email="test@email.com",
            name="Test User 2",
        ),
    ]
    blender = Blender(mock_client, users=users, playlist_length=10)

    playlist = blender.blend()
    assert playlist == unordered(RESULT_REPEATING_DIFFERENT_SPOTS)


def test_blend_repeating_equal_spots(mock_client):
    users = [
        User(
            id="user_1",
            api_id="repeating_equal",
            email="test@email.com",
            name="Test User 1",
        ),
        User(
            id="user_2",
            api_id="repeating_equal",
            email="test@email.com",
            name="Test User 2",
        ),
    ]

    blender = Blender(mock_client, users=users, playlist_length=9)

    playlist = blender.blend()
    assert playlist == unordered(RESULT_REPEATING_EQUAL_SPOTS_UNEVEN_AMOUNT)


def test_blend_repeating_equal_spots_random(mock_client, mocker):
    mock_random_choice = mocker.patch("random.choice")
    mock_random_choice.side_effect = ["user_1", "user_2"]

    users = [
        User(
            id="user_1",
            api_id="repeating_equal",
            email="test@email.com",
            name="Test User 1",
        ),
        User(
            id="user_2",
            api_id="repeating_equal",
            email="test@email.com",
            name="Test User 2",
        ),
    ]

    blender = Blender(mock_client, users=users, playlist_length=10)

    playlist = blender.blend()
    assert playlist == unordered(RESULT_REPEATING_EQUAL_SPOTS)


def test_blend_empty_user_top(mock_client, mocker):
    mock_random_choice = mocker.patch("random.choice")
    mock_random_choice.side_effect = ["user_1", "user_2"]

    users = [
        User(
            id="user_1",
            api_id="no_conflicts",
            email="test@email.com",
            name="Test User 1",
        ),
        User(
            id="nouser", api_id="empty_top", email="test@email.com", name="Test User 2"
        ),
    ]

    blender = Blender(mock_client, users=users, playlist_length=10)

    playlist = blender.blend()
    assert playlist == unordered(RESULT_EMPTY_USER)
