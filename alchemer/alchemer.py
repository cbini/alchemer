import requests


class AlchemerSession(requests.Session):
    def __init__(self, api_version, api_token, api_token_secret, auth_method="api_key"):
        self.api_version = api_version
        self.base_url = f"https://api.alchemer.com/{self.api_version}"

        if api_version != "v5":
            raise NotImplementedError(
                "This library currently only works with v5+"
            )  # TODO: add < v5

        if auth_method == "api_key":
            self.auth_params = {
                "api_token": api_token,
                "api_token_secret": api_token_secret,
            }
        elif auth_method == "oauth":
            raise NotImplementedError(
                "This library currently only works with 'api_key' authentication"
            )  # TODO: add oauth

        super(AlchemerSession, self).__init__()

    def request(self, method, url, params, *args, **kwargs):
        params.update(self.auth_params)
        return super(AlchemerSession, self).request(
            method=method, url=url, params=params, *args, **kwargs
        )

    def _api_call(self, method, object_name, params, id=None):
        try:
            r = self.request(method, url=object_name, id=id, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as xc:
            raise xc

    def _api_get(self, object_name, id, params):
        return self._api_call(
            method="GET", object_name=object_name, id=id, params=params
        ).get("data")

    def _api_list(self, object_name, params):
        all_data = []
        while True:
            r = self._api_call(method="GET", object_name=object_name, params=params)

            data = r.get("data")
            if type(data) == list:
                all_data.extend(data)
            elif type(data) == dict:
                all_data.append(data)

            page = r.get("page", 1)
            params.update({"page": page + 1})
            total_pages = r.get("total_pages", 1)

            if page == total_pages:
                break

        return all_data

    def survey(self, id=None):
        return Survey(session=self, name="survey", id=id)

    def account(self, id=None):
        return AlchemerObject(session=self, name="account", id=id)

    def account_teams(self, id=None):
        return AlchemerObject(session=self, name="accountteams", id=id)

    def account_user(self, id=None):
        return AlchemerObject(session=self, name="accountuser", id=id)

    def domain(self, id=None):
        return AlchemerObject(session=self, name="domain", id=id)

    def sso(self, id=None):
        return AlchemerObject(session=self, name="sso", id=id)

    def survey_theme(self, id=None):
        return AlchemerObject(session=self, name="surveytheme", id=id)

    def contact_list(self, id=None):
        return ContactList(session=self, name="contactlist", id=id)

    def contact_custom_field(self, id=None):
        return AlchemerObject(session=self, name="contactcustomfield", id=id)


class AlchemerObject(object):
    def __init__(self, session, name, id, **kwargs):
        self.__name__ = name
        self.__parent = kwargs.pop("parent", None)
        self._session = getattr(self.__parent, "_session", session)
        self.id = id or ""

    @property
    def url(self):
        url = getattr(self.__parent, "url", self._session.base_url)
        return f"{url}/{self.__name__}/{self.id}"

    def get(self, params={}):
        if self.id:
            self.__data = self._session._api_get(
                object_name=self.url,
                id=self.id,
                params=params,
            )

            for k, v in self.__data.items():
                setattr(self, k, v)

        return self

    def list(self, params={}):
        if "page" in params:
            return self._session._api_get(
                object_name=self.url,
                id=self.id,
                params=params,
            )
        else:
            return self._session._api_list(
                object_name=self.url,
                params=params,
            )

    def create(self, params):
        return self._session._api_call(
            method="PUT", object_name=self.__name__, id=self.id, params=params
        )

    def update(self, params):
        return self._session._api_call(
            method="POST", object_name=self.__name__, id=self.id, params=params
        )

    def delete(self):
        return self._session._api_call(
            method="DELETE", object_name=self.__name__, id=self.id, params={}
        )


class Survey(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def question(self, id=None):
        return SurveyQuestion(
            parent=self, session=self._session, name="surveyquestion", id=id
        )

    def campaign(self, id=None):
        return SurveyCampaign(
            parent=self, session=self._session, name="surveycampaign", id=id
        )

    def page(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveypage", id=id
        )

    def report(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveyreport", id=id
        )

    def response(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveyresponse", id=id
        )

    def statistic(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveystatistic", id=id
        )

    def quota(self, id=None):
        return AlchemerObject(parent=self, session=self._session, name="quotas", id=id)


class SurveyQuestion(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def option(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveyoption", id=id
        )


class SurveyCampaign(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def contact(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveycontact", id=id
        )  # TODO: returns None?

    def email_message(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="emailmessage", id=id
        )


class ContactList(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def contact(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="contactlistcontact", id=id
        )


"""
TODO:
SUB-OBJECTS:
[BETA] Reporting Object
[BETA] Results Object
SUB-SUB-OBJECTS:
[BETA] ReportElement Object
"""
