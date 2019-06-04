import pickle
import openpyxl
from openpyxl import Workbook
import argparse
import re


class ForeTeller:

    def __init__(self):
        self.table_filename = 'table_mapping_model.sav'

        self.list_table_vector_criterion_new = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'journal',
                                                'unternehmen', 'sstamm', 'sammeln', 'nachweis', 'kostenstellen',
                                                'buchungen', 'fibu', 'kosten', 'offene', 'posten', 'gemeinsame',
                                                'daten', 'itor', 'mandanten', 'stamm', 'itoren', 'personen', 'konten',
                                                'mandanten', 'sach', 'kred', 'deb', 'konto', 'adressen',
                                                'adresstabelle', 'adressen', 'adresstabelle', 'adressen',
                                                'adresstabelle']

        self.predict_result_sorted = ['a_account', 'a_account_detail', 'a_address', 'a_collective_statement',
                                      'a_costcenter_records', 'a_fiscal', 'a_inventory', 'a_journal', 'a_open_item',
                                      'a_organisation', 'a_posting_record']

        self.dict_table_column = {'a_inventory': 'column_02_a_fiscal_model.sav',
                                  'a_fiscal': 'column_02_a_fiscal_model.sav',
                                  'a_account': 'column_03_a_account_model.sav',
                                  'a_address': 'column_04_a_address_model.sav',
                                  'a_collective_statement': 'column_05_a_collective_statement_model.sav',
                                  'a_organisation': 'column_06_a_organisation_model.sav',
                                  'a_account_detail': 'column_07_a_account_detail_model.sav',
                                  'a_costcenter_records': 'column_08_a_costcenter_records_model.sav',
                                  'a_journal': 'column_09_a_journal_model.sav',
                                  'a_open_item': 'column_10_a_open_item_model.sav',
                                  'a_posting_record': 'column_11_a_posting_record_model.sav'}

        self.dic_column_pre_processing = {
                             'column_02_a_fiscal_model.sav': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
                                                              'abgeschlossen', 'b', 'beginn', 'bis', 'c', 'd', 'e',
                                                              'ende', 'eroeffnet', 'erste', 'f', 'g', 'h', 'i', 'j',
                                                              'jahr', 'k', 'kalenderjahr', 'l', 'letzte', 'm', 'monat',
                                                              'n', 'nrgeschjahr', 'o', 'p', 'periode', 'pgeschaeftjahr',
                                                              'q', 'r', 's', 't', 'u', 'v', 'von', 'w', 'wj', 'x', 'y',
                                                              'z'],

                             'column_03_a_account_model.sav': ['0', '1', '1', '2', '2', '3', '4', '5', '6', '7', '8',
                                                               '9', 'a', 'art', 'b', 'bez', 'bez1', 'bezeichnung',
                                                               'bezeichnung2', 'c', 'd', 'e', 'f', 'g',
                                                               'geschaeftspartner', 'h', 'i', 'ifktbeschr', 'j', 'k',
                                                               'klasse', 'konto', 'kontoart', 'kontonummer', 'ktoart',
                                                               'ktonr', 'l', 'm', 'n', 'name', 'nr', 'nrdeb', 'nrkred',
                                                               'nrkto', 'o', 'p', 'pkktonr', 'pkontonummer', 'q', 'r',
                                                               's', 't', 'text', 'typ', 'u', 'unternehmen', 'v', 'w',
                                                               'x', 'y', 'z', 'zus', 'zusatzbezeich'],

                             'column_04_a_address_model.sav': ['0', '1', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                               'a', 'anrede', 'b', 'c', 'd', 'debitor', 'e', 'f',
                                                               'fmna', 'g', 'h', 'hausnr', 'i', 'j', 'k', 'kreditor',
                                                               'l', 'land', 'landkz', 'm', 'n', 'nachname', 'name',
                                                               'name1', 'name2', 'name3', 'nation', 'nradr',
                                                               'nrbundesland', 'o', 'ort', 'p', 'plz', 'postf',
                                                               'postfach', 'postleitzahl', 'q', 'r', 'region', 's',
                                                               'strasse', 't', 'u', 'v', 'vona', 'vorname', 'w', 'x',
                                                               'y', 'z'],

                             'column_05_a_collective_statement_model.sav': ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                            '9', 'a', 'b', 'betragnetto',
                                                                            'betragnettowhrg', 'betragsteuer',
                                                                            'betragsteuerwhrg', 'buchnr', 'buchpos',
                                                                            'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                                                                            'l', 'm', 'n', 'nrkto', 'nrsammbuch',
                                                                            'nrstschl', 'o', 'p', 'q', 'r', 's',
                                                                            'sollhaben', 'steuerart', 't', 'u', 'v',
                                                                            'w', 'whrg', 'x', 'y', 'z'],

                             'column_06_a_organisation_model.sav': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                                    'a', 'additiv', 'b', 'bezeichnung', 'c', 'c13b',
                                                                    'd', 'e', 'f', 'g', 'gr', 'gruppe', 'h', 'i', 'ig',
                                                                    'j', 'k', 'konto', 'kurzbez', 'l', 'm', 'n', 'o',
                                                                    'ohne', 'p', 'q', 'r', 's', 'schl', 'skontoaufwand',
                                                                    'skontoertrag', 'st', 'steuersatz', 't', 'u', 'ust',
                                                                    'v', 'vst', 'w', 'x', 'y', 'z', 'zeile', 'zeilen'],

                             'column_07_a_account_detail_model.sav': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                                      'a', 'automahn', 'autozahl', 'b', 'basiswaehrung',
                                                                      'c', 'd', 'e', 'f', 'fordgruppe', 'g', 'h', 'i',
                                                                      'j', 'k', 'kredit', 'kreditextern',
                                                                      'kreditintern', 'l', 'm', 'mahnadrabw',
                                                                      'mahngruppe', 'n', 'nradr', 'nrauto', 'nrskd121',
                                                                      'nrslf121', 'nrzahlart', 'o', 'p', 'q', 'r', 's',
                                                                      't', 'u', 'ustcode', 'ustermittlung', 'v',
                                                                      'verbgruppe', 'verbnr', 'vstcode',
                                                                      'vstermittlung', 'w', 'whrg', 'x', 'y', 'z',
                                                                      'zahlart', 'zahlkond'],

                             'column_08_a_costcenter_records_model.sav': ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                          '9', 'a', 'b', 'belegnr', 'betrag', 'buch',
                                                                          'buchungsdatum', 'buchungstext', 'c', 'd',
                                                                          'e', 'erfassungsdatum', 'ew', 'f', 'g',
                                                                          'geschaeftsjahr', 'h', 'haben', 'i', 'j',
                                                                          'k', 'kostenart', 'l', 'm', 'menge',
                                                                          'mengeneinheit', 'n', 'o', 'p', 'pbelegdatum',
                                                                          'pbelegnummer', 'pbuch', 'periode',
                                                                          'periodenart', 'pjournalnummer',
                                                                          'pjournalzeile', 'pkostenstelle1',
                                                                          'pkostenstelle2', 'pwaehrung', 'q', 'r', 's',
                                                                          'schluessel', 'soll', 't',
                                                                          'transaktionsnummer', 'u', 'v', 'verrech',
                                                                          'w', 'x', 'y', 'z'],

                             'column_09_a_journal_model.sav': ['0', '1', '13b', '2', '3', '4', '5', '6', '7', '8', '9',
                                                               'a', 'art', 'b', 'belegdatum', 'belegnummer', 'betrag',
                                                               'bez', 'bu', 'buchungsbetrag', 'buchungsnummer',
                                                               'buchungstext', 'buja', 'c', 'd', 'dat', 'e', 'erf',
                                                               'f', 'fest', 'g', 'gkto', 'h', 'haben', 'habenbetrag',
                                                               'habenkonto', 'hbk', 'i', 'id', 'ige', 'j', 'k',
                                                               'konto', 'l', 'm', 'n', 'o', 'p', 'periode', 'q', 'r',
                                                               's', 'schl', 'soll', 'sollbetrag', 'sollkonto', 'st',
                                                               'steuerprozentsatz', 't', 'u', 'ust', 'v', 'vaz', 'w',
                                                               'x', 'y', 'z'],

                             'column_10_a_open_item_model.sav': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5',
                                                                 '6', '7', '8', '9', 'a', 'art', 'ausz', 'b',
                                                                 'belegdatum', 'belegnr', 'belegnummer', 'betrag',
                                                                 'betraghausw', 'buch', 'buchungsperiode', 'c', 'd',
                                                                 'dvbelegnummer', 'dvbuchungsnummer', 'dvkontonummer',
                                                                 'e', 'eigenwaehrung', 'einheit', 'entgelbetrag',
                                                                 'entgeltbetr1', 'entgeltbetr2', 'entgeltbetr3',
                                                                 'entgeltbetr4', 'entgeltbetr5', 'erfassungam', 'ew',
                                                                 'f', 'faellig', 'faelligkeitsdat', 'fremdbeleg', 'fw',
                                                                 'fwhaben', 'fwsoll', 'g', 'h', 'haben', 'i',
                                                                 'infogegenkonto', 'internebelegnummer', 'j',
                                                                 'journalnummer', 'k', 'klasse', 'kontonummer', 'kurs',
                                                                 'l', 'm', 'mahnstufe', 'n', 'name', 'o', 'p',
                                                                 'pbelegnummer', 'pkontonummer', 'plfd', 'pop', 'q',
                                                                 'r', 's', 'sammelkonto', 'sammelkto', 'schluessel',
                                                                 'skonto1bis', 'skonto1prozent', 'skonto2bis',
                                                                 'skonto2prozent', 'soll', 'status', 'steuerart',
                                                                 'steuerbetr', 'steuerbetrag1', 'steuerbetrag2',
                                                                 'steuerbetrag3', 'steuerbetrag4', 'steuerbetrag5',
                                                                 'steuerbezeichn1', 'steuerbezeichn2',
                                                                 'steuerbezeichn3', 'steuerbezeichn4',
                                                                 'steuerbezeichn5', 'steuerkonto', 'steuerprozent1',
                                                                 'steuerprozent2', 'steuerprozent3', 'steuerprozent4',
                                                                 'steuerprozent5', 't', 'text', 'u', 'v', 'valuta',
                                                                 'valutadatum', 'verrech', 'w', 'waehr', 'waehrung',
                                                                 'x', 'y', 'z'],

                             'column_11_a_posting_record_model.sav': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5',
                                                                      '5', '6', '7', '8', '9', 'Interne', 'Interne',
                                                                      'Interne', 'Interne', 'Interne', 'Interne',
                                                                      'Interne', 'Interne', 'Interne', 'Interne',
                                                                      'a', 'ausbuchungsgrund', 'b', 'basiswaehrung',
                                                                      'basiswhrg', 'belegdat', 'belegdatum', 'belegnr',
                                                                      'belegnummer', 'betrag', 'betragausb',
                                                                      'betragausbwhrg', 'betragnetto',
                                                                      'betragnettowhrg', 'betragskto', 'betragsktowhrg',
                                                                      'betragsteuer', 'betragsteuerwhrg', 'betragwhrg',
                                                                      'bsnr', 'buch', 'buchcode', 'buchdat', 'buchnr',
                                                                      'buchpos', 'buchtext', 'buchungam',
                                                                      'buchungnettowert', 'buchungsdatum',
                                                                      'buchungsnummer', 'buchungsperiode',
                                                                      'buchungstext', 'c', 'd', 'dvbelegnummer',
                                                                      'dvbuchungsnummer', 'dvkontonummer', 'e',
                                                                      'eigenwaehrung', 'eingeg', 'einheit',
                                                                      'entgelbetrag', 'entgeltbetr1', 'entgeltbetr2',
                                                                      'entgeltbetr3', 'entgeltbetr4', 'entgeltbetr5',
                                                                      'erfassungam', 'erfassungsdatum', 'ew', 'f',
                                                                      'fremdbelegnr', 'fw', 'fwhaben', 'fwsoll', 'g',
                                                                      'gegenkonto', 'geschaeftsjahr', 'gkto', 'gktonr',
                                                                      'h', 'haben', 'habenbetrag', 'hbk',
                                                                      'herkunftskz', 'i', 'infogegenkonto',
                                                                      'internebelegnummer', 'j', 'journalnummer', 'k',
                                                                      'konto', 'kontonummer', 'kost1', 'ktonr', 'kurs',
                                                                      'l', 'laendercode', 'laenderkennz', 'land',
                                                                      'leistungsdatum', 'link', 'm', 'menge',
                                                                      'mengeneinheit', 'n', 'name', 'nrbs', 'nrgegkto',
                                                                      'nrgeschjahr', 'nrjournaldruck', 'nrjournalseite',
                                                                      'nrperiode', 'nrstschl', 'o', 'p', 'pbelegdatum',
                                                                      'pbelegnummer', 'pbuch', 'periode', 'periodenart',
                                                                      'perskto', 'pjournalnummer', 'pjournalzeile',
                                                                      'pkontonummer', 'proz', 'prozentsatz',
                                                                      'pwaehrung', 'q', 'r', 's', 'sammelkonto',
                                                                      'sammelkto', 'schluessel', 'skontobetr', 'soll',
                                                                      'sollbetrag', 'sollhaben', 'steuerart',
                                                                      'steuerbetr', 'steuerbetrag1', 'steuerbetrag2',
                                                                      'steuerbetrag3', 'steuerbetrag4',
                                                                      'steuerbetrag5', 'steuerbezeichn1',
                                                                      'steuerbezeichn2', 'steuerbezeichn3',
                                                                      'steuerbezeichn4', 'steuerbezeichn5',
                                                                      'steuerkonto', 'steuerproz', 'steuerprozent1',
                                                                      'steuerprozent2', 'steuerprozent3',
                                                                      'steuerprozent4', 'steuerprozent5', 'steuersatz',
                                                                      'steuerschluessel', 'sto', 'storno', 'stueck',
                                                                      't', 'text', 'transaktionsnummer', 'u', 'umsatz',
                                                                      'ust', 'v', 'valutadatum', 'verrech',
                                                                      'verrech_belegnr', 'verrech_belegnr',
                                                                      'verrech_belegnr', 'verrech_belegnr',
                                                                      'verrech_belegnr', 'verrech_belegnr',
                                                                      'verrech_belegnr', 'verrech_belegnr',
                                                                      'verrech_belegnr', 'verrech_belegnr',
                                                                      'vst', 'w', 'waehr', 'waehrung', 'whrg',
                                                                      'wjmonat', 'wkz', 'x', 'y', 'z']
        }

        self.dict_column_items = {'a_inventory': ['quantity'],
                                  'a_fiscal': ['period_end', 'period_start', 'year'],
                                  'a_account': ['acde_id', 'currency', 'desc1', 'desc2', 'name', 'no', 'nointernal',
                                                'type'],
                                  'a_address': ['city', 'country', 'firstname', 'lastname', 'name1', 'name2',
                                                'name3', 'no', 'pob', 'region', 'salutation', 'street', 'zipcode'],
                                  'a_collective_statement': ['account', 'amount', 'amountnet', 'credit', 'currency',
                                                             'id', 'postingid', 'postingpos', 'tax', 'taxexchange',
                                                             'taxkey', 'taxtype'],
                                  'a_organisation': ['c13b', 'desc', 'desc-short', 'discountexpense', 'discountincome',
                                                     'group', 'groupadd', 'grouprow', 'inputvataccount',
                                                     'intracommunityrow', 'taxkey', 'taxpercentage', 'vat',
                                                     'vataccount'],
                                  'a_account_detail': ['addr_dunning', 'addr_id', 'association', 'creditexternal',
                                                       'creditinternal', 'currency', 'dunning', 'dunninggroup',
                                                       'group', 'id', 'payment', 'paymentterms', 'paymenttype',
                                                       'vatcode', 'vatdetermination'],
                                  'a_costcenter_records': ['amount', 'costcenter1', 'costtype', 'currency', 'debit',
                                                           'documentdate', 'documentnumber', 'documentnumberoffset',
                                                           'entrydate', 'fisc_id', 'journal', 'journalrow', 'period',
                                                           'periodtype', 'postingdate', 'postingkey', 'postingtext',
                                                           'quantity',  'quantityunit', 'tan'],
                                  'a_journal': ['balanceaccount', 'balanceoffsetaccount', 'creditaccount',
                                                'creditamount', 'debitaccount', 'debitamount', 'documentdate',
                                                'documentnumber', 'entrydate', 'lockingdate', 'name', 'offsetaccount',
                                                'orga_id', 'period', 'periodprepayment', 'postingamount', 'postingdate',
                                                'postingid', 'postingtext', 'taxpercentage', 'vat', 'vat13b',
                                                'vataccountcredit', 'vataccountdebit', 'vatamount', 'vatcredit',
                                                'vatdebit', 'vatintracommunity', 'vattype', 'year'],
                                      'a_open_item': ['account', 'accountinternal', 'accountno', 'amount', 'amountclearing',
                                                  'amountexchange', 'credit', 'currency', 'currencyunit',
                                                  'discountdate1',  'discountdate2',  'discountpercentage1',
                                                  'discountpercentage2', 'documentdate',  'documentnumber',
                                                  'documentnumberinternal', 'documentnumberoffset', 'duedate',
                                                  'dunning', 'entrydate', 'exchangedate', 'exchangerate',
                                                  'externaldocuments', 'journal', 'offsetaccount', 'owncurrency',
                                                  'payment1', 'payment2', 'payment3', 'payment4', 'payment5',
                                                  'payment6', 'period', 'periodclearing', 'postingid', 'postingkey',
                                                  'postingtext',  'runningnumber',  'state',  'summaryaccount',
                                                  'summaryname', 'tax', 'taxaccount1', 'taxaccount2', 'taxaccount3',
                                                  'taxaccount4', 'taxaccount5', 'taxdescription1', 'taxdescription2',
                                                  'taxdescription3', 'taxdescription4', 'taxdescription5',
                                                  'taxexchange', 'taxpayment1', 'taxpayment2', 'taxpayment3',
                                                  'taxpayment4', 'taxpayment5', 'taxpercentage1', 'taxpercentage2',
                                                  'taxpercentage3', 'taxpercentage4', 'taxpercentage5', 'taxtype',
                                                  'type', 'valuedate'],
                                  'a_posting_record': ['account', 'accountcountry', 'accountname', 'amount',
                                                       'amountexchange', 'amountnet', 'amountnetexchange',
                                                       'balanceaccount', 'balanceoffsetaccount', 'cancellation',
                                                       'chargeoff', 'chargeoffexchange', 'chargeoffreason',
                                                       'core_costcenter1', 'country', 'credit', 'currency',
                                                       'currencyunit', 'debit', 'discount', 'discountexchange',
                                                       'documentdate', 'documentnumber', 'documentnumberinternal',
                                                       'documentnumberoffset', 'documentnumberoriginal', 'entrydate',
                                                       'exchangedate', 'exchangerate', 'externaldocuments', 'fisc_id',
                                                       'inputvataccount', 'journal', 'journalrow', 'offsetaccount',
                                                       'operatingsite', 'owncurrency', 'payment1', 'payment2',
                                                       'payment3', 'payment4', 'payment5', 'payment6', 'period',
                                                       'periodtype', 'postingId', 'postingcode', 'postingdate',
                                                       'postingid', 'postingkey', 'postingpos', 'postingtext',
                                                       'quantity', 'quantityunit', 'summaryaccount', 'summaryname',
                                                       'tan', 'tax', 'taxaccount1', 'taxaccount2', 'taxaccount3',
                                                       'taxaccount4', 'taxaccount5', 'taxdescription1',
                                                       'taxdescription2', 'taxdescription3', 'taxdescription4',
                                                       'taxdescription5', 'taxexchange', 'taxkey', 'taxpayment1',
                                                       'taxpayment2', 'taxpayment3', 'taxpayment4', 'taxpayment5',
                                                       'taxpercentage', 'taxpercentage1', 'taxpercentage2',
                                                       'taxpercentage3', 'taxpercentage4', 'taxpercentage5',
                                                       'taxpoint', 'taxtype', 'unit', 'vataccount', 'vatpercentage']}
        input_dataset = DataFlow()
        self.list_table_input, self.list_column_input = input_dataset.read_data_commandline()
        self.list_table_vector = []

    def predict_table(self):

        for i_pre in range(len(self.list_table_input)):
            self.list_table_input[i_pre] = self.list_table_input[i_pre].lower()

        for item in self.list_table_input:
            temp = []
            for i in self.list_table_vector_criterion_new:
                num = item.count(i)
                num_weight = num * (len(i))
                temp.append(num_weight)
            self.list_table_vector.append(temp)

        classifier_table = pickle.load(open(self.table_filename, 'rb'))
        t_predict_possibility = classifier_table.predict_proba(self.list_table_vector)
        list_proba_result = []
        for i_predict in t_predict_possibility:
            list_proba_result.append(dict(sorted(zip(self.predict_result_sorted, i_predict),
                                                 key=lambda x: x[1], reverse=True)))

        return list_proba_result

    def predict_table_top_N(self, list_result, number):

        list_result_top_n = []
        for i_dict in list_result:
            list_result_top_n.append({key: value for key, value in i_dict.items() if value in
                                      sorted(set(i_dict.values()), reverse=True)[:number]})

        return list_result_top_n

    def predict_column_improve(self, list_result_top_n):

        for i_pre_c in range(len(self.list_column_input)):
            self.list_column_input[i_pre_c] = self.list_column_input[i_pre_c].lower()

        c_predict = []
        for i_diction in range(len(list_result_top_n)):
            c_predict_sub = []
            for i_key in list_result_top_n[i_diction].keys():

                column_algorithm_filename = self.dict_table_column[i_key]
                column_to_vector_criterion = self.dic_column_pre_processing[column_algorithm_filename]

                column_to_vector = []
                for i_c in column_to_vector_criterion:
                    num_c = self.list_column_input[i_diction].count(i_c)
                    num_weight_c = num_c * (len(i_c))
                    column_to_vector.append(num_weight_c)

                classifier_column = pickle.load(open(column_algorithm_filename, 'rb'))
                column_to_vector_predict_result = classifier_column.predict_proba([column_to_vector])
                list_preba_result_column = []
                for i_predict in column_to_vector_predict_result:
                    list_preba_result_column.append(dict(sorted(zip(self.dict_column_items[i_key], i_predict),
                                                         key=lambda x: x[1], reverse=True)))
                list_result_top_n_column = []
                for i_dict in list_preba_result_column:
                    list_result_top_n_column.append({key: value for key, value in i_dict.items() if value in
                                                     sorted(set(i_dict.values()), reverse=True)[:3]})
                    # you can change the number column output result by change the number: 3

                c_predict_sub.append([i_key, list_result_top_n_column, list_result_top_n[i_diction][i_key]])
            c_predict.append(c_predict_sub)
        return c_predict

    def start(self):
        from importance_evaluation import aa_importance_evaluate_plus

        table_result_all = self.predict_table()
        predict_result_top_n_table = self.predict_table_top_N(table_result_all, 4)
        # you can change the number table output result by change the number: 4
        predict_result_top_n_pre = self.predict_column_improve(predict_result_top_n_table)

        importance_calculate = aa_importance_evaluate_plus.Evaluation(self.list_table_input, self.list_column_input)
        list_importance = importance_calculate.importance_predict(importance_calculate.table_predict())
        for i_final_index in range(len(predict_result_top_n_pre)):
            predict_result_top_n_pre[i_final_index].append({"The importance value : ":list_importance[i_final_index]})

        for i_final in predict_result_top_n_pre:
            print(i_final)
            print('--------------------------------------------------------------------------------------------')


class DataFlow:

    def read_data_commandline(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", '--table', type=str)

        parser.add_argument("-c", '--column', type=str,
                            help="Please input tables name without space.The comma as separator. "
                                 "The table and column name must be written in a pair and at the same order."
                                 "Both the table name and column name should have at least one character."
                                 "eg: python code.py --table=table01,table02 --column=column01,column02")

        args = parser.parse_args()
        if (args.table is None) or (args.column is None):
            exit(parser.format_help())

        list_table = str(args.table).split(",")
        list_column = str(args.column).split(",")

        if len(list_table) != len(list_column):
            exit(parser.format_help())

        for word in list_table:
            if (re.search('[a-zA-Z äöüß]', word)) is None:
                exit(parser.format_help())

        for word in list_column:
            if (re.search('[a-zA-Z äöüß]', word)) is None:
                exit(parser.format_help())

        return list_table, list_column


if __name__ == "__main__":
    print('--------------------------------------------------------------------------------------------')
    ActiveForecast = ForeTeller()
    ActiveForecast.start()



