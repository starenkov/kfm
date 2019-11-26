# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from requests import get
from bs4 import BeautifulSoup
from app.creds import KFM


class Parser:
    def __init__(self, xmldoc=None):
        if xmldoc:
            self.xmldoc = xmldoc
            self.tree = ET.fromstring(self.xmldoc)

    def _(self, s: str):
        """
        Возвращает raw
        :param s: строка данных
        :type s: str
        :return:
        """
        return r'{}'.format(s)

    def _cleaner(self, item: str, birthday=False):
        """
        Функция очищает данные от мусора
        :param item: текстовые данные
        :type item: str
        :param birthday: день рождения
        :type birthday: str
        :return:
        """
        if item and not birthday:
            return r'{}'.format(item.replace(r'\xa', ''))
        elif item and birthday:
            item = item.replace('.', '-').split('-')
            if len(item[0]) == 4:
                birthd = item[0] + '-' + item[1] + '-' + item[2]
                return r'{}'.format(birthd)
            if len(item[2]) == 4:
                birthd = item[2] + '-' + item[1] + '-' + item[0]
                return r'{}'.format(birthd)
        elif not item and birthday:
            return r'1666-06-06'
        elif not item:
            return r''

    def get_persons(self):
        """
        Возвращает лист словарей с данными персон террористов
        :return:
        """
        tree_index = 0
        for i, item in enumerate(self.tree):
            tree_index = i
            if self.tree[i].tag == 'persons':
                break

        array_persons = []
        for element in self.tree[tree_index]:
            person = {}
            person['num'] = self._cleaner(element.find('num').text)
            person['lname'] = self._cleaner(element.find('lname').text)
            person['fname'] = self._cleaner(element.find('fname').text)
            person['mname'] = self._cleaner(element.find('mname').text)
            person['birthdate'] = self._cleaner(element.find('birthdate').text, birthday=True)
            person['iin'] = self._cleaner(element.find('iin').text)
            person['note'] = self._cleaner(element.find('note').text)
            person['correction'] = self._cleaner(element.find('correction').text)
            array_persons.append(person)
        return array_persons

    def get_organisations(self):
        """
        Возвращает лист словарей с данными террористических организаций
        :return:
        """
        tree_index = 0
        for i, item in enumerate(self.tree):
            tree_index = i
            if self.tree[tree_index].tag == 'organisations':
                break

        array_org = []
        for element in self.tree[tree_index]:
            org = dict()
            org['num'] = self._cleaner(element.find('num').text)
            org['org_name'] = self._cleaner(element.find('org_name').text)
            org['note'] = self._cleaner(element.find('note').text)
            array_org.append(org)
        return array_org

    def get_un_individuals(self):

        """
        Возвращает список индвидуальных терр. организаций ООН
        :return:
         """

        text = get('https://scsanctions.un.org/resources/xml/en/consolidated.xml').text
        xml = BeautifulSoup(text, 'lxml')

        repeated_tags = ['individual_alias', 'individual_document', 'individual_place_of_birth']
        individuals = xml.find_all('individual')

        array_individuals = []
        sort_data_ind = []

        for i in individuals:
            tags = list(i.childGenerator())
            params = dict()

            for tag in tags:

                name = tag.name
                child_tags = [child for child in tag.findChildren()]

                if name not in params.keys() and len(child_tags) == 0:
                    params[name] = tag.getText()
                elif name not in repeated_tags:
                    params[name] = {child.name: child.getText() for child in
                                    child_tags}
                else:
                    value = params.get(name) or []
                    tags_values = {child.name: child.getText() for child in
                                   child_tags}
                    value.append(tags_values)
                    params[name] = value

            sort_data_ind.append(params)

        for value in sort_data_ind:

            un_individuals = {'dataid': value.get('dataid'), 'versionnum': value.get('versionnum'),
                              'first_name': value.get('first_name'), 'second_name': value.get('second_name'),
                              'third_name': value.get('third_name'), 'fourth_name': value.get('fourth_name'),
                              'un_list_type': value.get('un_list_type'),
                              'reference_number': value.get('reference_number'), 'listed_on': value.get('listed_on'),
                              'comments1': value.get('comments1')}

            dict_of_data = value.get('designation')
            sorting_string = ''
            if dict_of_data:
                for data in dict_of_data.values():
                    sorting_string += data + '. '
            else:
                continue
            un_individuals['designation'] = sorting_string

            dict_of_data = value.get('nationality')
            sorting_string = ''
            if dict_of_data:
                for data in dict_of_data.values():
                    sorting_string += data + '. '
            else:
                continue
            un_individuals['nationality'] = sorting_string

            dict_of_data = value.get('list_type')
            sorting_string = ''
            if dict_of_data:
                for data in dict_of_data.values():
                    sorting_string += data + '. '
            else:
                continue
            un_individuals['list_type'] = sorting_string

            dict_of_data = value.get('last_day_updated')
            sorting_string = ''
            if dict_of_data:
                for data in dict_of_data.values():
                    sorting_string += data + '. '
            else:
                continue
            un_individuals['last_day_updated'] = sorting_string

            list_of_data = value.get('individual_alias')
            sorting_string = ''
            for dict_of_data in list_of_data:
                for key, data in dict_of_data.items():
                    if data:
                        sorting_string += key + ': ' + data + '. '
                    else:
                        continue
            un_individuals['individual_alias'] = sorting_string

            dict_of_data = value.get('individual_address')
            sorting_string = ''
            for key, data in dict_of_data.items():
                if data:
                    sorting_string += key + ': ' + data + '. '
                else:
                    continue
            un_individuals['individual_address'] = sorting_string

            dict_of_data = value.get('individual_date_of_birth')
            sorting_string = ''
            for key, data in dict_of_data.items():
                if data:
                    sorting_string += key + ': ' + data + '. '
                else:
                    continue
            un_individuals['individual_date_of_birth'] = sorting_string

            list_of_data = value.get('individual_place_of_birth')
            sorting_string = ''
            if list_of_data:
                for dict_of_data in list_of_data:
                    for key, data in dict_of_data.items():
                        if data:
                            sorting_string += key + ': ' + data + '. '
                        else:
                            continue
            un_individuals['individual_place_of_birth'] = sorting_string

            list_of_data = value.get('individual_document')
            sorting_string = ''
            if list_of_data:
                for dict_of_data in list_of_data:
                    for key, data in dict_of_data.items():
                        if data:
                            sorting_string += key + ': ' + data + '. '
                        else:
                            continue
            un_individuals['individual_document'] = sorting_string

            array_individuals.append(un_individuals)
        return array_individuals

    def get_un_entities(self):
        """
        Возвращает список террористических группировок ООН
        :return:
        """
        text = get('https://scsanctions.un.org/resources/xml/en/consolidated.xml').text
        xml = BeautifulSoup(text, 'lxml')

        repeated_tags = ['entity_address', 'entity_alias']
        entities = xml.find_all('entity')

        array_entities = []
        sort_data_ent = []

        for e in entities:
            tags = list(e.childGenerator())
            params = dict()

            for tag in tags:

                name = tag.name
                child_tags = [child for child in tag.findChildren()]

                if name not in params.keys() and len(child_tags) == 0:
                    params[name] = tag.getText()
                elif name not in repeated_tags:
                    params[name] = {child.name: child.getText() for child in
                                    child_tags}
                else:
                    value = params.get(name) or []
                    tags_values = {child.name: child.getText() for child in
                                   child_tags}
                    value.append(tags_values)
                    params[name] = value
            sort_data_ent.append(params)

        for value in sort_data_ent:
            un_entities = {'dataid': value.get('dataid'),
                           'versionnum': value.get('versionnum'),
                           'first_name': value.get('first_name'),
                           'un_list_type': value.get('un_list_type'),
                           'reference_number': value.get('reference_number'),
                           'comments1': value.get('comments1'),
                           'listed_on': value.get('listed_on'),
                           'name_original_script': value.get('name_original_script')}

            for data in value.get('list_type').values():
                un_entities['list_type'] = data
            for data in value.get('last_day_updated').values():
                un_entities['last_day_updated'] = data

            list_of_data = value.get('entity_alias')
            sorting_string = ''
            if list_of_data:
                for dict_of_data in list_of_data:
                    for key, data in dict_of_data.items():
                        if data:
                            sorting_string += key + ': ' + data + '. '
                        else:
                            continue
            else:
                continue
            un_entities['entity_alias'] = sorting_string

            list_of_data = value.get('entity_address')
            sorting_string = ''
            if list_of_data:
                for dict_of_data in list_of_data:
                    for key, data in dict_of_data.items():
                        if data:
                            sorting_string += key + ': ' + data + '. '
                        else:
                            continue
            else:
                continue
            un_entities['entity_address'] = sorting_string

            array_entities.append(un_entities)

        return array_entities
