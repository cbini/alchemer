import requests

from .classes import AlchemerObject, Survey, ContactList


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

    def _api_call(self, method, object_name, params):
        try:
            r = self.request(method, url=object_name, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as xc:
            raise xc

    def _api_get(self, object_name, params):
        return self._api_call(method="GET", object_name=object_name, params=params).get(
            "data"
        )

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
