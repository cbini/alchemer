import os

import pytest

from alchemer import __version__, AlchemerSession
from alchemer.classes import AlchemerObject, Survey, SurveyQuestion

from dotenv import load_dotenv
load_dotenv()

ALCHEMER_API_TOKEN = os.getenv("ALCHEMER_API_TOKEN")
ALCHEMER_API_TOKEN_SECRET = os.getenv("ALCHEMER_API_TOKEN_SECRET")


def get_client(api_version, time_zone=None):
    return AlchemerSession(
        api_version=api_version,
        api_token=ALCHEMER_API_TOKEN,
        api_token_secret=ALCHEMER_API_TOKEN_SECRET,
        time_zone=time_zone,
    )


@pytest.fixture
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


@pytest.fixture
def question_keys():
    return []


@pytest.fixture
def account_keys():
    return []


def test_version():
    assert __version__ == "0.3.1"


def test_client_authentication():
    client = get_client("v5")

    assert client.auth_params.get("api_token") == ALCHEMER_API_TOKEN
    assert client.auth_params.get("api_token_secret") == ALCHEMER_API_TOKEN_SECRET


def test_account_v5(account_keys):
    client = get_client("v5")

    # get list of surveys
    account_list = client.account.list()
    assert isinstance(account_list, list)
    assert len(account_list) > 0

    # check 1st survey list item is dict with expected keys
    a = account_list[0]
    assert isinstance(a, dict)
    assert set(account_keys).issubset(a.keys())

    # get survey object of 1st item
    account = client.account.get(a["id"])
    assert isinstance(account, AlchemerObject)
    # assert set(account_keys).issubset(survey.__dict__.keys())


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


def test_surveycampaign_filter_v5():
    client = get_client("v5")
    survey_list = client.survey.list()
    s = survey_list[0]
    survey = client.survey.get(s["id"])

    sc_list_filtered = (
        survey.campaign.filter("name", "=", "My New Web Link")
        .filter("date_created", ">=", "2021-08-01 13:55:51 EDT")
        .list()
    )
    print(sc_list_filtered)
    assert isinstance(sc_list_filtered, list)

# def test_surveyresponse_page_v5():
#     client = get_client("v5")
#     survey = client.survey.get(4561325)
#     r = survey.response.filter("status", "=", "Disqualified").list()
