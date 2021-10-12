from dateutil import parser, tz

TZINFOS = {
    "EST": tz.gettz("US/Eastern"),
    "EDT": tz.gettz("US/Eastern"),
    "CST": tz.gettz("US/Central"),
    "CDT": tz.gettz("US/Central"),
    "MST": tz.gettz("US/Mountain"),
    "MDT": tz.gettz("US/Mountain"),
    "PST": tz.gettz("US/Pacific"),
    "PDT": tz.gettz("US/Pacific"),
}


class AlchemerObject(object):
    def __init__(self, session, name, **kwargs):
        self.__name__ = name
        self.__parent = kwargs.pop("parent", None)
        self._session = getattr(self.__parent, "_session", session)
        self._data = {}
        self._filters = []
        self.url = f"{getattr(self.__parent, 'url', session.base_url)}/{name}"

    def _prepare_filters(self, params={}):
        for f in self._filters:
            params.update(f)
        return params

    def get_object_data(self, id, params={}):
        self.url = f"{self.url}/{id}"
        return self._session._api_get(
            url=self.url,
            params=params,
        )

    def get(self, id, params={}):
        self.data = self.get_object_data(id=id, params=params).get("data")

        for k, v in self.data.items():
            try:
                v = parser.parse(v, tzinfos=TZINFOS)
                if not v.tzinfo and self._session.time_zone:
                    v = v.replace(tzinfo=self._session.time_zone)
            except:
                pass
            setattr(self, k, v)

        return self

    def list(self, params={}):
        params = self._prepare_filters(params)
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

    def filter(self, field, operator, value):
        i = len(self._filters)
        self._filters.append(
            {
                f"filter[field][{i}]": field,
                f"filter[operator][{i}]": operator,
                f"filter[value][{i}]": value,
            }
        )
        return self


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
