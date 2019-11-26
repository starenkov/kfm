class KFM:
    class Authorisation:
        url = 'http://kfm.gov.kz/assets/components/office/action.php'
        action = 'auth/formLogin'
        username = ''
        password = ''

    class Included:
        url = 'http://kfm.gov.kz/blacklist/export/included/xml'  # Включенные. Через 3 дня попадёт в Active

    class Excluded:
        url = 'http://kfm.gov.kz/blacklist/export/excluded/xml'  # Исключенные

    class Active:
        url = 'http://kfm.gov.kz/blacklist/export/active/xml'  # Действующие

    class Consolidated:
        url = 'https://scsanctions.un.org/resources/xml/en/consolidated.xml'  # Список террирористов и организаций ООН

class DB:
    class Cortigiana:
        host = 'localhost'
        sessionname = 'postgres'
        user = 'postgres'
        password = 'postgres'
        port = 5432
        timezone = 'Asia/Almaty'
        logfile = 'session.log'

class AppSetting:
    logfile = 'app.log'
    server_timezone = 'UTC'