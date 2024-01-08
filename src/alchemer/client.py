import copy

from requests import Session

from .classes import AlchemerObject, ContactList, Survey


class AlchemerSession(Session):
    def __init__(
        self,
        api_version,
        api_token,
        api_token_secret,
        auth_method="api_key",
        time_zone=None,
        timeout=None,
    ):
        self.api_version = api_version
        self.base_url = f"https://api.alchemer.com/{api_version}"
        self.time_zone = time_zone
        self.timeout = timeout

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

    def request(self, method, url, params, **kwargs):
        params.update(self.auth_params)

        return super(AlchemerSession, self).request(
            method=method, url=url, params=params, timeout=self.timeout, **kwargs
        )

    def _api_call(self, method, url, params):
        try:
            r = self.request(method=method, url=url, params=params)

            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise e

    def _api_get(self, url, params):
        params = copy.deepcopy(params)

        return self._api_call(method="GET", url=url, params=params)

    def _api_list(self, url, params):
        request_params = copy.deepcopy(params)
        all_data = []

        while True:
            response = self._api_get(url=url, params=request_params)

            total_pages = response.get("total_pages", 1)
            page = response.get("page", 1)
            data = response.get("data", [])

            if isinstance(data, dict):
                all_data.extend([data])
            else:
                all_data.extend(data)

            if page == total_pages:
                break
            elif total_pages == 0:
                break
            elif "page" in params:
                break
            else:
                request_params.update({"page": page + 1})

        return all_data

    @property
    def account(self):
        return AlchemerObject(session=self, name="account")

    @property
    def account_teams(self):
        return AlchemerObject(session=self, name="accountteams")

    @property
    def account_user(self):
        return AlchemerObject(session=self, name="accountuser")

    @property
    def domain(self):
        return AlchemerObject(session=self, name="domain")

    @property
    def sso(self):
        return AlchemerObject(session=self, name="sso")

    @property
    def survey(self):
        return Survey(session=self, name="survey")

    @property
    def survey_theme(self):
        return AlchemerObject(session=self, name="surveytheme")

    @property
    def contact_list(self):
        return ContactList(session=self, name="contactlist")

    @property
    def contact_custom_field(self):
        return AlchemerObject(session=self, name="contactcustomfield")
