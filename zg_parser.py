from .ftp_parser import FtpParser

from lxml import etree


class ZakupkiGovCompanyParser(FtpParser):
    """
    Парсер организаций zakupki.gov
    """
    def transform_data(self, xml):
        data = {
            'reg_number': self.retrieve(xml, './s:regNumber/text()', int),
            'cons_registry_num': self.retrieve(xml, './s:consRegistryNum/text()'),
            'short_name': self.retrieve(xml, './s:shortName/text()'),
            'full_name': self.retrieve(xml, './s:fullName/text()'),
            'factual_address': {
                'building': self.retrieve(xml, './s:factualAddress/s:building/text()', int),
                'country_code': self.retrieve(xml, './s:factualAddress/s:country/s:countryCode/text()', int),
                'country_full_name': self.retrieve(xml, './s:factualAddress/s:country/s:countryFullName/text()'),
                'filled_manually':
                    True if self.retrieve(xml, './s:factualAddress/s:filledManually/text()') == 'true' else False,
                'region_kladr_type': self.retrieve(xml, './s:factualAddress/s:region/s:kladrType/text()'),
                'region_kladr_code': self.retrieve(xml, './s:factualAddress/s:region/s:kladrCode/text()'),
                'region_full_name': self.retrieve(xml, './s:factualAddress/s:region/s:fullName/text()'),
                'city_kladr_type': self.retrieve(xml, './s:factualAddress/s:city/s:kladrType/text()'),
                'city_kladr_code': self.retrieve(xml, './s:factualAddress/s:city/s:kladrCode/text()'),
                'city_full_name': self.retrieve(xml, './s:factualAddress/s:city/s:fullName/text()'),
                'short_street': self.retrieve(xml, './s:factualAddress/s:shortStreet/text()'),
                'zip': self.retrieve(xml, './s:factualAddress/s:zip/text()', int),
            },
            'postal_address': self.retrieve(xml, './s:postalAddress/text()'),
            'email': self.retrieve(xml, './s:email/text()'),
            'phone': self.retrieve(xml, './s:phone/text()'),
            'fax': self.retrieve(xml, './s:fax/text()'),
            'contact_person': {
                'last_name': self.retrieve(xml, './s:contactPerson/s:lastName/text()'),
                'first_name': self.retrieve(xml, './s:contactPerson/s:firstName/text()'),
                'middle_name': self.retrieve(xml, './s:contactPerson/s:middleName/text()')
            },
            'accounts': [],
            'budgets': [],
            'ordering_agency_reg_num': self.retrieve(xml, './s:orderingAgency/regNum/text()', int),
            'ordering_agency_full_name': self.retrieve(xml, './s:orderingAgency/fullName/text()'),
            'inn': self.retrieve(xml, './s:INN/text()', int),
            'kpp': self.retrieve(xml, './s:KPP/text()', int),
            'registration_date': self.retrieve(xml, './s:registrationDate/text()'),
            'iku': self.retrieve(xml, './s:IKUInfo/IKU/text()', int),
            'date_st_iku': self.retrieve(xml, './s:IKUInfo/dateStIKU/text()'),
            'ogrn': self.retrieve(xml, './s:OGRN/text()', int),
            'okopf_code': self.retrieve(xml, './s:OKOPF/code/text()', int),
            'okopf_full_name': self.retrieve(xml, './s:OKOPF/fullName/text()'),
            'okpo': self.retrieve(xml, './s:OKPO/text()', int),
            'okved': self.retrieve(xml, './s:OKVED/text()'),
            'organization_role': self.retrieve(xml, './s:organizationRole/text()'),
            'organization_type_code': self.retrieve(xml, './s:organizationType/code/text()'),
            'organization_type_name': self.retrieve(xml, './s:organizationType/name/text()'),
            'oktmo_code': self.retrieve(xml, './s:OKTMO/code/text()'),
            'subordination_type': self.retrieve(xml, './s:subordinationType/text()'),
            'url': self.retrieve(xml, './s:url/text()'),
            'time_zone': self.retrieve(xml, './s:timeZone/text()'),
            'time_zone_utc_offset': self.retrieve(xml, './s:timeZoneUtcOffset/text()'),
            'time_zone_olson': self.retrieve(xml, './s:timeZoneOlson/text()'),
            'actual': True if self.retrieve(xml, './s:actual/text()') == 'true' else False,
            'register': True if self.retrieve(xml, './s:register/text()') == 'true' else False
        }

        for account_xml in xml.xpath('./s:accounts/s:account', namespaces=self.ns()):
            data['accounts'].append({
                'bank_address': self.retrieve(account_xml, './s:bankAddress/text()'),
                'bank_name': self.retrieve(account_xml, './s:bankName/text()'),
                'bik': self.retrieve(account_xml, './s:bik/text()', int),
                'payment_account': self.retrieve(account_xml, './s:paymentAccount/text()'),
                'personal_account': self.retrieve(account_xml, './s:personalAccount/text()')

            })

        for budget_xml in xml.xpath('./s:budgets/s:budget', namespaces=self.ns()):
            data['budgets'].append({
                'code': self.retrieve(budget_xml, './s:code/text()', int),
                'name': self.retrieve(budget_xml, './s:name/text()')
            })

        return data

    def extract_data(self):
        path = r'/fcs_nsi/nsiOrganization/'

        self.ftp.cwd(path)
        file_list = self.ftp.nlst('nsiOrganization_all_*.xml.zip')

        for file in file_list:
            company_list = []
            # Создаем временный файл и разархивируем содержимое
            xml_file = self.extract_xml(path, file)[0]

            # Обрабатываем xml с помощью lxml etree iterparse
            if xml_file:
                for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/types/1}nsiOrganization'):
                    if event == 'end':
                        company_list.append(self.transform_data(xml))
                        xml.clear()

            yield company_list
