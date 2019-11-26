from app.kfmController import KfmWorker
from app.xmlParser import Parser


class Action:
    @classmethod
    def add_active_persons(cls):
        xml = KfmWorker().get_active()
        arr_persons = Parser(xmldoc=xml).get_persons()

    @classmethod
    def add_active_organisations(cls):
        xml = KfmWorker().get_active()
        arr_organisations = Parser(xmldoc=xml).get_organisations()

    @classmethod
    def add_active_organisationscis(cls):
        xml = KfmWorker().get_active()
        arr_organisationscis = Parser(xmldoc=xml).get_organisationscis()

    @classmethod
    def add_included(cls):
        xml = KfmWorker().get_included()

    @classmethod
    def delete_excluded(cls):
        xml = KfmWorker().get_excluded()

    @classmethod
    def update_active(cls):
        pass
