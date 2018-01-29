from zipfile import ZipFile, ZipInfo

from tempfile import TemporaryFile

from .ftp_walk import FTPWalk

import ftplib

import re


class FtpParser:
    """
    FTP parser
    """
    def __init__(self, host, login, password):
        self.ftp = ftplib.FTP(host, user=login, passwd=password)

    @staticmethod
    def ns():
        # XML namespace
        return {
            's': 'http://zakupki.gov.ru/oos/types/1',
            's2': 'http://zakupki.gov.ru/oos/export/1',
            's3': 'http://zakupki.gov.ru/223fz/reference/1'
        }

    def retr(self, path, retry=3):
        """
        Извлечение файла во временный
        :param path:
        :param retry:
        :return:
        """
        tmp = TemporaryFile()
        try:
            size = self.ftp.size(path)
            self.ftp.retrbinary('RETR ' + path, tmp.write)
        except Exception:
            if retry > 0:
                tmp.close()
                # Рекурсивно вызываем retry попыток
                return self.retr(path, retry - 1)
            else:
                tmp.close()
                return None

        # Сравниваем размер созданного временного файла с размером оригинального файла
        if size != tmp.tell():
            if retry > 0:
                tmp.close()
                return self.retr(path, retry - 1)
            else:
                tmp.close()
                return None
        return tmp

    def retrieve(self, xml, xpath, fun=lambda x: x):
        try:
            return fun(xml.xpath(xpath, namespaces=self.ns(), smart_strings=False)[0])
        except Exception:
            return None

    @staticmethod
    def unzip(zip_file):
        """
        Разархиварование файла
        """
        zf = ZipFile(zip_file)
        zip_infos = zf.infolist()
        unzipped = []

        for zip_info in zip_infos:
            if not zip_info.filename.endswith('.xml'):
                continue
            unzipped.append(zf.open(zip_info))
        zf.close()

        return unzipped

    def extract_xml(self, path, file):
        """
        Создаем временный файл и разархивируем содержимое
        :param path:
        :param file:
        :return:
        """
        path = '{}{}'.format(path, file)

        try:
            zip_file = self.retr(path, retry=5)
            xml_files = self.unzip(zip_file)
        except Exception:
            return None

        return xml_files

    def transform_data(self, xml):
        raise NotImplementedError

    def extract_data(self):
        raise NotImplementedError

    def walk(self, path, regexp_pattern=None):
        """
        Рекурсивная выборка всех файлов из директории
        :param path: Директория
        :param regexp_pattern: Регулярное выражение для фильтрации файлов
        :return:
        """
        regexp = None
        if regexp_pattern:
            regexp = re.compile(regexp_pattern)

        ftp_walker = FTPWalk(self.ftp)

        for directory in ftp_walker.walk(path):
            for file in directory[2]:
                file_path = "{}/{}".format(directory[0], file)

                if regexp_pattern:
                    if regexp.match(file_path):
                        yield file_path
                else:
                    yield file_path

    def __del__(self):
        self.ftp.quit()
