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
                params=params,
            )

            for k, v in self.__data.items():
                setattr(self, k, v)

        return self

    def list(self, params={}):
        if "page" in params:
            return self._session._api_get(
                object_name=self.url,
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

    def campaign(self, id=None):
        return SurveyCampaign(
            parent=self, session=self._session, name="surveycampaign", id=id
        )

    def page(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveypage", id=id
        )

    def question(self, id=None):
        return SurveyQuestion(
            parent=self, session=self._session, name="surveyquestion", id=id
        )

    def quota(self, id=None):
        return AlchemerObject(parent=self, session=self._session, name="quotas", id=id)

    def report(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveyreport", id=id
        )

    def reporting(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="reporting", id=id
        )

    def response(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveyresponse", id=id
        )

    def results(self, id=None):
        return AlchemerObject(parent=self, session=self._session, name="results", id=id)

    def statistic(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="surveystatistic", id=id
        )


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


class Reporting(AlchemerObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def element(self, id=None):
        return AlchemerObject(
            parent=self, session=self._session, name="reportelement", id=id
        )
