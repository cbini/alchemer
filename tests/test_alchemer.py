import os

from alchemer import __version__, AlchemerSession

ALCHEMER_API_TOKEN = os.getenv("ALCHEMER_API_TOKEN")
ALCHEMER_API_TOKEN_SECRET = os.getenv("ALCHEMER_API_TOKEN_SECRET")


def intantiate_client(
    api_version="v5",
    api_token=ALCHEMER_API_TOKEN,
    api_token_secret=ALCHEMER_API_TOKEN_SECRET,
):
    return AlchemerSession(
        api_version=api_version,
        api_token=api_token,
        api_token_secret=api_token_secret,
    )


def test_version():
    assert __version__ == "0.2.0"


def test_client_authentication():
    client = intantiate_client()
    assert client.auth_params.get("api_token") == ALCHEMER_API_TOKEN
    assert client.auth_params.get("api_token_secret") == ALCHEMER_API_TOKEN_SECRET


def test_alchemer_object_list():
    client = intantiate_client()
    surveys = client.survey.list()
    assert type(surveys) == list

    if len(surveys) > 0:
        s = surveys[0]
        assert type(s) == dict

        s_keys = ['id', 'team', 'type', 'status', 'created_on', 'modified_on', 'title', 'statistics', 'links']
        assert list(s.keys()) == s_keys

def test_alchemer_object_get():
    pass
