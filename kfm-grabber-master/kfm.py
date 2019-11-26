from app.kfmController import KfmWorker
from app.xmlParser import Parser
from app.creds import AppSetting
from app.db_queries import Kfm
import logging
from app.mailer import wooppay_smtp

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] | %(message)s',
    level=logging.INFO,
    filename=AppSetting.logfile
)


class Monitor(object):

    def update(self, sess, kfm_data):
        """
        Обновляет при необходимости список активных

        :param sess: Сессии БД
        :param kfm_data: Объект с данными КФМ
        :return:
        """
        xml = kfm_data
        arr_persons = Parser(xmldoc=xml).get_persons()
        arr_organisations = Parser(xmldoc=xml).get_organisations()
        arr_organisationscis = Parser(xmldoc=xml).get_organisationscis()
        arr_ogranisationsus = Parser(xmldoc=xml).get_ogranisationsun()

        for person in arr_persons:
            sess.add_person(person)
        for org in arr_organisations:
            sess.add_organisation(org)
        for org_cis in arr_organisationscis:
            sess.add_organisationcis(org_cis)
        for org_un in arr_ogranisationsus:
            sess.add_ogranisationus(org_un)

    def update_excluded(self, sess, kfm_data):
        """
        Удаляет из БД исключенных

        :param sess: Сессии БД
        :param kfm_data: Объект с данными КФМ
        :return:
        """
        xml = kfm_data
        arr_persons = Parser(xmldoc=xml).get_persons()
        arr_organisations = Parser(xmldoc=xml).get_organisations()
        arr_organisationscis = Parser(xmldoc=xml).get_organisationscis()
        arr_ogranisationsun = Parser(xmldoc=xml).get_ogranisationsun()
        for person in arr_persons:
            if not person.get('correction'):
                sess.del_person(person)
        for org in arr_organisations:
            sess.del_organisation(org)
        for org_cis in arr_organisationscis:
            sess.del_all_organisationscis(org_cis)
        for org_un in arr_ogranisationsun:
            sess.del_all_organisationsun(org_un)


    def start(self):
        kfm_data = KfmWorker()
        kfm_data.login()
        db_sess = Kfm()
        try:
            logging.info('add from active list')
            self.update(db_sess, kfm_data.get_active())
            db_sess.update_relevance('persons')
            self.update(db_sess, kfm_data.get_included())
            db_sess.update_relevance('organisations')
            self.update_excluded(db_sess, kfm_data.get_excluded())
            db_sess.update_relevance('organisationscis')
            db_sess.session_close()
        except Exception as e:
            db_sess.session_rollback()
            db_sess.session_close()
            logging.exception(e)
            wooppay_smtp('kfm-grabber', str(e), AppSetting.trace_mail)


if __name__ == '__main__':
    m = Monitor()
    m.start()
