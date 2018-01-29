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


    SETTINGS = {
        'HOST': '...',
        'LOGIN': '...',
        'PASSWORD': '...'        
    }

    parser = ZakupkiGovCompanyParser(
        SETTINGS['HOST'],
        SETTINGS['LOGIN'],
        SETTINGS['PASSWORD']
    )

    parser.extract_data():
