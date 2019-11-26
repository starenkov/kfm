# -*- coding: utf-8 -*-
import pytz
import datetime
import re

from sqlalchemy.orm.exc import NoResultFound

from models.kfm_dbmodels import *
from app.creds import DB


class Kfm:
    def __init__(self):
        self.session = session

    def _get_criterion_for_person(self, packet: dict):
        """
        Формирует критерий для запроса в БД по персоне. Если данные по персоне содержат пустое поле, или же
        данные содержат корректировку или примечание по какому-либо из полей персоны, поле не попадает в критерий.

        :param packet: ответ API со списком персон
        :return: словарь с полями для запроса в БД
        """
        criterion = {  # Начальный критерий
            'lname': packet.get('lname'),
            'fname': packet.get('fname'),
            'mname': packet.get('mname'),
            'birthdate': packet.get('birthdate'),
        }

        if packet.get('iin').isdigit():  # Поле с ИИН не добавляется в критерий, если оно будет пустым.
            criterion['iin'] = packet.get('iin')

        corrections_map = {
            'fname': 'Имя',
            'mname': 'Отчество',
            'lname': 'Фамилия',
            'iin': 'ИИН'
        }
        for field, correction in corrections_map.items():
            field_corrected = re.search(correction.lower(), ' '.join([packet['note'], packet['correction']]).lower())
            field_in_criterion = field in criterion
            if field_corrected and field_in_criterion:
                del criterion[field]
        return criterion

    def add_person(self, packet: dict):
        """
        Функция добавляет в базу персону, а при её наличии в базе, обновляет по ней данные,
        т.к. может прийти корректировка.

        :param packet: словарь данных клиента
        :type packet: dict
        :return:
        """
        try:
            criteria = self._get_criterion_for_person(packet)
            person = self.session.query(KfmPersons).filter_by(**criteria).one()
            descr = ''
            if person.num != packet.get('num'):
                descr += 'num: ' + person.num + ' -> ' + packet.get('num') + '. '
                person.num = packet.get('num')
            if person.lname != packet.get('lname'):
                descr += 'lname: ' + person.lname + ' -> ' + packet.get('lname') + '. '
                person.lname = packet.get('lname')
            if person.fname != packet.get('fname'):
                descr += 'fname: ' + person.fname + ' -> ' + packet.get('fname') + '. '
                person.fname = packet.get('fname')
            if person.mname != packet.get('mname'):
                descr += 'mname: ' + person.mname + ' -> ' + packet.get('mname') + '. '
                person.mname = packet.get('mname')
            if str(person.birthdate) != packet.get('birthdate'):
                descr += 'birthdate: ' + person.birthdate + ' -> ' + packet.get('birthdate') + '. '
                person.birthdate = packet.get('birthdate')
            if person.note != packet.get('note'):
                descr += 'note: ' + person.note + ' -> ' + packet.get('note') + '. '
                person.note = packet.get('note')
            if person.correction != packet.get('correction'):
                descr += 'note: ' + person.correction + ' -> ' + packet.get('correction') + '. '
                person.correction = packet.get('correction')

            if len(descr) > 0:
                self.session.commit()
                self.history(
                    item=packet,
                    item_type='persons',
                    action_type='update',
                    action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                    descr=descr
                )
            return True
        except NoResultFound:
            person = KfmPersons(
                num=packet.get('num'),
                iin=packet.get('iin'),
                lname=packet.get('lname'),
                fname=packet.get('fname'),
                mname=packet.get('mname'),
                birthdate=packet.get('birthdate'),
                note=packet.get('note'),
                correction=packet.get('correction')
            )
            self.session.add(person)
            self.session.commit()

            self.history(
                item=packet,
                item_type='persons',
                action_type='add',
                action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                descr=''
            )
            return True

    def add_organisation(self, packet: dict):
        """
        Функция добавляет в базу организацию, а при её наличии в базе, обновляет по ней данные,
        т.к. может прийти корректировка.
        :param packet: словарь данных организации
        :type packet: dict
        :return:
        """
        try:
            org = self.session.query(KfmOrganisations).filter(KfmOrganisations.org_name == packet.get('org_name')).one()
            descr = ''
            if org.num != packet.get('num'):
                org.num = packet.get('num')
                descr += 'num: ' + org.num + ' -> ' + packet.get('num') + '. '
            if org.org_name != packet.get('org_name'):
                org.org_name = packet.get('org_name')
                descr += 'name: ' + org.org_name + ' -> ' + packet.get('org_name') + '. '
            if org.note != packet.get('note'):
                org.note = packet.get('note')
                descr += 'note: ' + org.note + ' -> ' + packet.get('note') + '. '

            if len(descr) > 0:
                self.session.commit()
                self.history(
                    item=packet,
                    item_type='organisations',
                    action_type='update',
                    action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                    descr=descr
                )
            return True
        except NoResultFound:
            org = KfmOrganisations(
                num=packet.get('num'),
                org_name=packet.get('org_name'),
                note=packet.get('note'),
            )
            self.session.add(org)
            self.session.commit()

            self.history(
                item=packet,
                item_type='organisation',
                action_type='add',
                action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                descr=''
            )
            return True

    def add_organisationcis(self, packet: dict):
        """
        Функция добавляет в базу организацию, а при её наличии в базе, обновляет по ней данные,
        т.к. может прийти корректировка.

        :param packet: словарь данных организации
        :type packet: dict
        :return:
        """
        try:
            org = self.session.query(KfmOrganisationscis).filter(
                KfmOrganisationscis.org_name == packet.get('org_name')).one()
            descr = ''
            if org.num != packet.get('num'):
                org.num = packet.get('num')
                descr += 'num: ' + org.num + ' -> ' + packet.get('num') + '. '
            if org.org_name != packet.get('org_name'):
                org.org_name = packet.get('org_name')
                descr += 'org_name: ' + org.org_name + ' -> ' + packet.get('org_name') + '. '
            if org.org_name_en != packet.get('org_name_en'):
                org.org_name_en = packet.get('org_name_en')
                descr += 'org_name_en: ' + org.org_name_en + ' -> ' + packet.get('org_name_en') + '. '
            if org.note != packet.get('note'):
                org.note = packet.get('note')
                descr += 'note: ' + org.note + ' -> ' + packet.get('note') + '. '

            if len(descr) > 0:
                self.session.commit()
                self.history(
                    item=packet,
                    item_type='organisationcis',
                    action_type='update',
                    action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                    descr=descr
                )
            return True
        except NoResultFound:
            org = KfmOrganisationscis(
                num=packet.get('num'),
                org_name=packet.get('org_name'),
                org_name_en=packet.get('org_name_en'),
                note=packet.get('note')
            )
            self.session.add(org)
            self.session.commit()

            self.history(
                item=packet,
                item_type='organisationcis',
                action_type='add',
                action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                descr=''
            )
            return True

    def add_un_individuals(self, packet: dict):
        """
        Функция добавляет в базу индвидуальную организацию, а при её наличии в базе, обновляет по ней данные,
        т.к. может прийти корректировка.

        :param packet: dict of un individuals
        :return:
        """

        try:
            individual = self.session.query(KfmUnIndividuals).filter(KfmUnIndividuals.dataid == packet.get('dataid')).one()
            descr = ''

            if individual.dataid != packet.get('dataid'):
                individual.dataid = packet.get('dataid')
                descr += 'data id: ' + individual.dataid + ' -> ' + packet.get('dataid') + '. '

            if individual.versionnum != packet.get('versionnum'):
                individual.versionnum = packet.get('versionnum')
                descr += 'versionnum: ' + individual.versionnum + ' -> ' + packet.get('versionnum') + '. '

            if individual.first_name != packet.get('first_name'):
                individual.first_name = packet.get('first_name')
                descr += 'first name: ' + individual.first_name + ' -> ' + packet.get('first_name') + '. '

            if individual.second_name != packet.get('second_name'):
                individual.second_name = packet.get('second_name')
                descr += 'second name: ' + individual.second_name + ' -> ' + packet.get('second_name') + '. '

            if individual.third_name != packet.get('third_name'):
                individual.third_name = packet.get('third_name')
                descr += 'third name: ' + individual.third_name + ' -> ' + packet.get('third_name') + '. '

            if individual.fourth_name != packet.get('third_name'):
                individual.fourth_name = packet.get('third_name')
                descr += 'third name: ' + individual.fourth_name + ' -> ' + packet.get('third_name') + '. '

            if individual.un_list_type != packet.get('un_list_type'):
                individual.un_list_type = packet.get('un_list_type')
                descr += 'un list type: ' + individual.un_list_type + ' -> ' + packet.get('un_list_type') + '. '

            if individual.reference_number != packet.get('reference_number'):
                individual.reference_number = packet.get('reference_number')
                descr += 'reference number: ' + individual.reference_number + ' -> ' + \
                         packet.get('reference_number') + '. '

            if individual.listed_on != packet.get('listed_on'):
                individual.listed_on = packet.get('listed_on')
                descr += 'reference number: ' + individual.listed_on + ' -> ' + packet.get('listed_on') + '. '

            if individual.comments1 != packet.get('comments1'):
                individual.comments1 = packet.get('comments1')
                descr += 'comments1 ' + individual.comments1 + ' -> ' + packet.get('comments1') + '. '

            if individual.designation != packet.get('designation'):
                individual.designation = packet.get('designation')
                descr += 'designation ' + individual.designation + ' -> ' + packet.get('designation') + '. '

            if individual.nationality != packet.get('nationality'):
                individual.nationality = packet.get('designation')
                descr += 'designation ' + individual.nationality + ' -> ' + packet.get('designation') + '. '

            if individual.list_type != packet.get('list_type'):
                individual.list_type = packet.get('list_type')
                descr += 'list_type ' + individual.list_type + ' -> ' + packet.get('list_type') + '. '

            if individual.last_day_updated != packet.get('last_day_updated'):
                individual.last_day_updated = packet.get('last_day_updated')
                descr += 'last_day_updated ' + individual.last_day_updated + ' -> ' + \
                         packet.get('last_day_updated') + '. '

            if individual.individual_alias != packet.get('individual_alias'):
                individual.individual_alias = packet.get('individual_alias')
                descr += 'individual qualities and aliases' + individual.individual_alias + ' -> ' + \
                         packet.get('individual_alias') + '. '

            if individual.individual_address != packet.get('individual_address'):
                individual.individual_address = packet.get('individual_address')
                descr += 'individual address' + individual.individual_address + ' -> ' + \
                         packet.get('individual_address') + '. '

            if individual.individual_date_of_birth != packet.get('individual_date_of_birth'):
                individual.individual_date_of_birth = packet.get('individual_date_of_birth')
                descr += 'individual individual_date_of_birth' + individual.individual_date_of_birth + ' -> ' + \
                         packet.get('individual_date_of_birth') + '. '

            if individual.individual_place_of_birth != packet.get('individual_place_of_birth'):
                individual.individual_place_of_birth = packet.get('individual_place_of_birth')
                descr += 'individual_place_of_birth' + individual.individual_place_of_birth + ' -> ' + \
                         packet.get('individual_place_of_birth') + '. '

            if individual.individual_document != packet.get('individual_document'):
                individual.individual_document = packet.get('individual_document')
                descr += 'individual_document' + individual.individual_document + ' -> ' + \
                         packet.get('individual_document') + '. '

            if len(descr) > 0:
                self.session.commit()
                self.history(
                    item=packet,
                    item_type='un_individuals',
                    action_type='update',
                    action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                    descr=descr
                )
            return True
        except NoResultFound:
            individual = KfmUnIndividuals(
                dataid=packet.get('dataid'),
                versionnum=packet.get('versionnum'),
                first_name=packet.get('first_name'),
                second_name=packet.get('second_name'),
                third_name=packet.get('third_name'),
                fourth_name=packet.get('fourth_name'),
                un_list_type=packet.get('un_list_type'),
                reference_number=packet.get('reference_number'),
                listed_on=packet.get('listed_on'),
                comments1=packet.get('comments1'),
                designation=packet.get('designation'),
                nationality=packet.get('nationality'),
                list_type=packet.get('list_type'),
                last_day_updated=packet.get('last_day_updated'),
                individual_alias=packet.get('individual_alias'),
                individual_address=packet.get('individual_address'),
                individual_date_of_birth=packet.get('individual_date_of_birth'),
                individual_place_of_birth=packet.get('individual_place_of_birth'),
                individual_document=packet.get('individual_document')
            )
            self.session.add(individual)
            self.session.commit()

            self.history(
                item=packet,
                item_type='un_individuals',
                action_type='add',
                action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                descr=''
            )

            return True

    def add_un_entities(self, packet: dict):
        """
        Функция добавляет в базу группировку, а при её наличии в базе, обновляет по ней данные,
        т.к. может прийти корректировка.

        :param packet: dict of un entities
        :return:
        """

        try:
            entity = self.session.query(KfmUnEntities).filter(KfmUnEntities.dataid == packet.get('dataid')).one()
            descr = ''

            if entity.dataid != packet.get('dataid'):
                entity.dataid = packet.get('dataid')
                descr += 'data id: ' + entity.dataid + ' -> ' + packet.get('dataid') + '. '

            if entity.versionnum != packet.get('versionnum'):
                entity.versionnum = packet.get('versionnum')
                descr += 'versionnum: ' + entity.versionnum + ' -> ' + packet.get('versionnum') + '. '

            if entity.first_name != packet.get('first_name'):
                entity.first_name = packet.get('first_name')
                descr += 'first name: ' + entity.first_name + ' -> ' + packet.get('first_name') + '. '

            if entity.un_list_type != packet.get('un_list_type'):
                entity.un_list_type = packet.get('un_list_type')
                descr += 'un_list_type: ' + entity.un_list_type + ' -> ' + packet.get('un_list_type') + '. '

            if entity.reference_number != packet.get('reference_number'):
                entity.reference_number = packet.get('reference_number')
                descr += 'reference_number: ' + entity.reference_number + ' -> ' + packet.get('reference_number') + '. '

            if entity.listed_on != packet.get('listed_on'):
                entity.listed_on = packet.get('listed_on')
                descr += 'listed_on: ' + entity.listed_on + ' -> ' + packet.get('listed_on') + '. '

            if entity.name_original_script != packet.get('name_original_script'):
                entity.name_original_script = packet.get('name_original_script')
                descr += 'name_original_script: ' + entity.name_original_script + ' -> ' + \
                         packet.get('name_original_script') + '. '

            if entity.comments1 != packet.get('comments1'):
                entity.comments1 = packet.get('comments1')
                descr += 'comments1: ' + entity.comments1 + ' -> ' + \
                         packet.get('comments1') + '. '

            if entity.list_type != packet.get('list_type'):
                entity.list_type = packet.get('list_type')
                descr += 'list_type: ' + entity.list_type + ' -> ' + packet.get('list_type') + '. '

            if entity.last_day_updated != packet.get('last_day_updated'):
                entity.last_day_updated = packet.get('last_day_updated')
                descr += 'last_day_updated: ' + entity.last_day_updated + ' -> ' + packet.get('last_day_updated') + '. '

            if entity.entity_address != packet.get('entity_address'):
                entity.entity_address = packet.get('entity_address')
                descr += 'entity_address ' + entity.entity_address + ' -> ' + packet.get('entity_address') + '. '

            if entity.entity_alias != packet.get('entity_alias'):
                entity.entity_alias = packet.get('entity_alias')
                descr += 'entity_alias ' + entity.entity_alias + ' -> ' + packet.get('entity_alias') + '. '

            if len(descr) > 0:
                self.session.commit()
                self.history(
                    item=packet,
                    item_type='un_entities',
                    action_type='update',
                    action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                    descr=descr
                )
            return True
        except NoResultFound:
            entity = KfmUnEntities(
                dataid=packet.get('dataid'),
                versionnum=packet.get('versionnum'),
                first_name=packet.get('first_name'),
                un_list_type=packet.get('un_list_type'),
                reference_number=packet.get('reference_number'),
                listed_on=packet.get('listed_on'),
                name_original_script=packet.get('name_original_script'),
                comments1=packet.get('comments1'),
                list_type=packet.get('list_type'),
                last_day_updated=packet.get('last_day_updated'),
                entity_address=packet.get('entity_address'),
                entity_alias=packet.get('entity_alias')
            )
            self.session.add(entity)
            self.session.commit()

            self.history(
                item=packet,
                item_type='un_entities',
                action_type='add',
                action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
                descr=''
            )

            return True

    def del_person_without_iin(self):
        """
        Удаляет персон из БД без ИИН

        :return:
        """
        person = self.session.query(KfmPersons).filter(KfmPersons.iin == '').delete()
        person = self.session.query(KfmPersons).filter(KfmPersons.iin == ' ').delete()
        session.commit()

        self.history(
            item='{}',
            item_type='persons',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех, кто без ИИН, перед загрузкой списка. Чтобы избежать проблем с корректировкой.'
        )
        return True

    def del_person(self, packet: dict):
        """
        Удаляет персону из БД
        :param packet: словарь данных клиента
        :type packet: dict
        :return:
        """
        criteria = self._get_criterion_for_person(packet)
        person = self.session.query(KfmPersons).filter_by(**criteria).delete()
        session.commit()

        if not packet.get('correction'):
            descr = packet.get('note')
        else:
            descr = 'Необходимо выяснить у ответственного причину удаления из БД.'

        self.history(
            item=packet,
            item_type='persons',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr=descr
        )
        return True

    def del_organisation(self, packet: dict):
        """
        Удаляет организацию из БД
        :param packet: словарь данных организации
        :type packet: dict
        :return:
        """
        person = self.session.query(KfmOrganisations).filter(
            KfmOrganisations.org_name == packet.get('org_name')).delete()
        session.commit()
        self.history(
            item={},
            item_type='organisations',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление организации из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_organisationcis(self, packet: dict):
        """
        Удаляет организацию СНГ из БД
        :param packet: словарь данных организации СНГ
        :type packet: dict
        :return:
        """
        person = self.session.query(KfmOrganisationscis).filter(
            KfmOrganisationscis.org_name == packet.get('org_name')).delete()
        session.commit()
        self.history(
            item={},
            item_type='organisationscis',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление организации запрещённой в странах СНГ из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_un_individuals(self, packet: dict):
        """
        Удаляет индивидуальных организацию ООН из БД
        :param packet: словарь данных организации СНГ
        :type packet: dict
        :return:
        """
        individual = self.session.query(KfmUnIndividuals).filter(
            KfmUnIndividuals.dataid == packet.get('dataid')).delete()
        session.commit()
        self.history(
            item={},
            item_type='un_individuals',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление организации запрещённой в странах ООН из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_un_entities(self, packet: dict):
        """
        Удаляет организацию ООН из БД
        :param packet: словарь данных организации СНГ
        :type packet: dict
        :return:
        """
        entity = self.session.query(KfmUnEntities).filter(
            KfmUnEntities.dataid == packet.get('dataid')).delete()
        session.commit()
        self.history(
            item={},
            item_type='un_entities',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление организации запрещённой в странах ООН из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_organisations(self):
        """
        Удаляет все организации из БД
        :return:
        """
        person = self.session.query(KfmOrganisations).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='organisations',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех организаций из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_organisationscis(self):
        """
        Удаляет все организации стран СНГ из БД
        :return:
        """
        person = self.session.query(KfmOrganisationscis).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='organisationscis',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех организаций стран СНГ из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_un_individuals(self):
        """
        Удаляет все индивидуальные организации стран ООН из БД
        :return:
        """
        individual = self.session.query(KfmUnIndividuals).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='un_individuals',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех индивидуальных организаций стран ООН из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_un_entities(self):
        """
        Удаляет все организации стран ООН из БД
        :return:
        """
        entity = self.session.query(KfmUnEntities).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='un_entities',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех  организаций стран ООН из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_persons(self):
        """
        Удаляет всех персон из БД
        :return:
        """
        person = self.session.query(KfmPersons).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='persons',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всех персон из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def del_all_history(self):
        """
        Удаление всей истории из БД
        :return:
        """
        person = self.session.query(KfmHistory).filter().delete()
        session.commit()
        self.history(
            item={},
            item_type='history',
            action_type='delete',
            action_date=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone))),
            descr='Удаление всей истории из БД. Необходимо уточнить у ответственного.'
        )
        return True

    def update_relevance(self, subject_type: str):
        """
        Обновляет время в таблице, в которой можно смотреть актуальность записей
        :param subject_type: Тип субъекта persons, organisations, organisationcis
        :type subject_type: str
        :return:
        """
        try:
            current = self.session.query(KfmRelevance).filter(KfmRelevance.id == 1).one()
            if subject_type == 'persons':
                current.persons = str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
            if subject_type == 'organisations':
                current.organisations = str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
            if subject_type == 'organisationscis':
                current.organisationscis = str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
            if subject_type == 'un_individuals':
                current.un_individuals = str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
            if subject_type == 'un_entities':
                current.un_entities = str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
            self.session.commit()
            return True
        except NoResultFound:
            if subject_type == 'persons':
                current = KfmRelevance(
                    persons=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
                )
                self.session.add(current)
            if subject_type == 'organisations':
                current = KfmRelevance(
                    organisations=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
                )
                self.session.add(current)
            if subject_type == 'organisationscis':
                current = KfmRelevance(
                    organisationscis=str(datetime.datetime.now(pytz.timezone(DB.Cortigiana.timezone)))
                )
                self.session.add(current)
            self.session.commit()
            return True

    def history(self, item: dict, item_type: str, action_type: str, action_date: str, descr: str):
        """
        Пишет историю действий по субъектам
        :param item: Данные по субъекту, передаются словарём и конвертятся в json
        :type item: dict
        :param item_type: Тип субъекта persons, organisations, organisationcis
        :type item_type: str
        :param action_type: add, delete, update
        :type action_type: str
        :param action_date: время изменения
        :type action_date: str
        :param descr: Описание, например: Список включённые
        :type descr: str
        :return:
        """
        sub_history = KfmHistory(
            item=item,
            item_type=item_type,
            action_type=action_type,
            action_date=action_date,
            descr=descr
        )
        self.session.add(sub_history)
        self.session.commit()
        return True

    def session_rollback(self):
        self.session.rollback()

    def session_close(self):
        self.session.close()
