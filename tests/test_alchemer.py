import os
from _pytest.monkeypatch import monkeypatch

from pytest import fixture

from alchemer import __version__, AlchemerSession
from alchemer.classes import AlchemerObject, Survey, SurveyQuestion
import pytest

ALCHEMER_API_TOKEN = os.getenv("ALCHEMER_API_TOKEN")
ALCHEMER_API_TOKEN_SECRET = os.getenv("ALCHEMER_API_TOKEN_SECRET")


def get_client(api_version):
    return AlchemerSession(
        api_version=api_version,
        api_token=ALCHEMER_API_TOKEN,
        api_token_secret=ALCHEMER_API_TOKEN_SECRET,
    )


@fixture
def survey_keys():
    return [
        "id",
        "team",
        "type",
        "status",
        "created_on",
        "modified_on",
        "title",
        "statistics",
        "links",
    ]


@fixture
def question_keys():
    return []


def test_version():
    assert __version__ == "0.3.0"


def test_client_authentication():
    client = get_client("v5")

    assert client.auth_params.get("api_token") == ALCHEMER_API_TOKEN
    assert client.auth_params.get("api_token_secret") == ALCHEMER_API_TOKEN_SECRET


def test_survey_v5(survey_keys):
    client = get_client("v5")

    # get list of surveys
    survey_list = client.survey.list()
    assert isinstance(survey_list, list)
    assert len(survey_list) > 0

    # check 1st survey list item is dict with expected keys
    s = survey_list[0]
    assert isinstance(s, dict)
    assert set(survey_keys).issubset(s.keys())

    # get survey object of 1st item
    survey = client.survey.get(s["id"])
    assert isinstance(survey, Survey)
    assert set(survey_keys).issubset(survey.__dict__.keys())

    # get list of survey questions
    sq_list = survey.question.list()
    assert isinstance(sq_list, list)
    assert len(sq_list) > 0

    # check 1st question list item is dict with expected keys
    sq = sq_list[0]
    assert isinstance(sq, dict)
    # assert set(sq_keys).issubset(sq.keys())

    # get question object of 1st item
    question = survey.question.get(sq["id"])
    assert isinstance(question, SurveyQuestion)
    # assert set(sq_keys).issubset(question.__dict__.keys())
