import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class PageParams(object):
    login_page_lnk = "https://www.ipko.pl"


class LoginParams(object):

    username = os.environ.get('IpkoUser')
    password = os.environ.get('IpkoPass')


class DateParams(object):
    start_dt = datetime.date(year=2019, month=1, day=1)
    current_dt = datetime.date.today()
    current_dttm = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


class FileParams(object):
    files_dir = f"{basedir}/csv_files/"
    logs_dir = f"{basedir}/logs/"
    file_format = "'CSV'"
