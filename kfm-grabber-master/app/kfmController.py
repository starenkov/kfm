import requests
from app.creds import KFM


class KfmWorker:
    def __init__(self):
        self.s = requests.Session()

    def login(self):
        """
        Авторизация на сайте kfm.gov.kz
        """
        self.s.get(KFM.Root.url, verify=False)
        self.s.post(
            KFM.Authorisation.url,
            data={
                'action': KFM.Authorisation.action,
                'username': KFM.Authorisation.username,
                'password': KFM.Authorisation.password,
                'return': '',
                'pageId': 790
            }
        )

    def get_active(self):
        """
        Возвращает список действующих террористов и террористических организаций

        :return: xml
        """
        xml = self.s.get(KFM.Active.url, verify=False)
        return xml.text

    def get_included(self):
        """
        Возвращает список включённых террористов и террористических организаций

        :return: xml
        """
        # self.s.cookies['browser'] = 'standard'
        xml = self.s.get(KFM.Included.url, verify=False)
        return xml.text

    def get_excluded(self):
        """
        Возвращает список исключённых террористов и террористических организаций

        :return: xml
        """
        xml = self.s.get(KFM.Excluded.url, verify=False)
        return xml.text

    def get_consolidated(self):
        """
        Возвращает список действующих террористов и террористических организаций ООН

        :return: xml
        """
        xml = self.s.get(KFM.Consolidated.url, verify=False)
        return xml.text
