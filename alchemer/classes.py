class AlchemerObject(object):
    def __init__(self, session, name, **kwargs):
        self.__name__ = name
        self.__parent = kwargs.pop("parent", None)
        self._session = getattr(self.__parent, "_session", session)
        self.url = f"{getattr(self.__parent, 'url', session.base_url)}/{name}"

    def get(self, id, params={}):
        self.url = f"{self.url}/{id}"
        self.__data = self._session._api_get(
            url=self.url,
            params=params,
        )

        for k, v in self.__data.items():
            setattr(self, k, v)

        return self

    def list(self, params={}):
        if "page" in params:
            return self._session._api_get(
                url=self.url,
                params=params,
            )
        else:
            return self._session._api_list(
                url=self.url,
                params=params,
            )

    def create(self, params):
        return self._session._api_call(method="PUT", url=self.url, params=params)

    def update(self, id, params):
        self.url = f"{self.url}/{id}"
        return self._session._api_call(method="POST", url=self.url, params=params)

    def delete(self, id):
        self.url = f"{self.url}/{id}"
        return self._session._api_call(method="DELETE", url=self.url, params={})


class Survey(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def campaign(self):
        return SurveyCampaign(parent=self, session=self._session, name="surveycampaign")

    @property
    def page(self):
        return AlchemerObject(parent=self, session=self._session, name="surveypage")

    @property
    def question(self):
        return SurveyQuestion(parent=self, session=self._session, name="surveyquestion")

    @property
    def quota(self):
        return AlchemerObject(parent=self, session=self._session, name="quotas")

    @property
    def report(self):
        return AlchemerObject(parent=self, session=self._session, name="surveyreport")

    @property
    def reporting(self):
        return AlchemerObject(parent=self, session=self._session, name="reporting")

    @property
    def response(self):
        return AlchemerObject(parent=self, session=self._session, name="surveyresponse")

    @property
    def results(self):
        return AlchemerObject(parent=self, session=self._session, name="results")

    @property
    def statistic(self):
        return AlchemerObject(
            parent=self, session=self._session, name="surveystatistic"
        )


class SurveyQuestion(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def option(self):
        return AlchemerObject(parent=self, session=self._session, name="surveyoption")


class SurveyCampaign(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def contact(self):
        return AlchemerObject(
            parent=self, session=self._session, name="surveycontact"
        )  # TODO: returns None?

    @property
    def email_message(self):
        return AlchemerObject(parent=self, session=self._session, name="emailmessage")


class ContactList(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def contact(self):
        return AlchemerObject(
            parent=self, session=self._session, name="contactlistcontact"
        )


class Reporting(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def element(self):
        return AlchemerObject(parent=self, session=self._session, name="reportelement")
