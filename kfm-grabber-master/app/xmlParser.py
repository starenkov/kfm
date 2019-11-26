# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


class Parser:
    def __init__(self, xmldoc):
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

    def get_organisationscis(self):
        """
        Возвращает лист словарей с данными террористических организаций запрещённых в странах СНГ
        :return:
        """
        tree_index = 0
        for i, item in enumerate(self.tree):
            tree_index = i
            if self.tree[tree_index].tag == 'organisationscis':
                break

        array_orgcis = []
        for element in self.tree[tree_index]:
            orgcis = {}
            orgcis['num'] = self._cleaner(element.find('num').text)
            orgcis['org_name'] = self._cleaner(element.find('org_name').text)
            orgcis['org_name_en'] = self._cleaner(element.find('org_name_en').text)
            orgcis['note'] = self._cleaner(element.find('note').text)
            array_orgcis.append(orgcis)
        return array_orgcis
    
    def get_ogranisationsun(self):
        
        array_individuals = []
        for element in self.tree.findall('.//INDIVIDUAL'):
            dict_individuals = dict()
            dict_individuals['id'] = element.findtext('DATAID')
            dict_individuals['lname'] = element.findtext('FIRST_NAME')
            dict_individuals['fname'] = element.findtext('SECOND_NAME')
            dict_individuals['mname'] = element.findtext('THIRD_NAME')
            dict_individuals['note'] = element.findtext('COMMENTS1')
            dict_individuals['org_name'] = element.findtext('.//ALIAS_NAME')

            array_individuals.append(dict_individuals)