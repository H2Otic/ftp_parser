FTP PARSER
==========

Pyhton класс для парсинга xml с FTP сервера.

Requirements
------------

- python (2.7, 3.4, 3.5)
- zipfile
- lxml

Использование
-------------

    from parser.zg_parser import ZakupkiGovCompanyParser


    parser = ZakupkiGovCompanyParser(host='host', login='login', password='pass')

    parser.extract_data():
