from sklearn.neighbors.nearest_centroid import NearestCentroid
import pickle
import os


class Evaluation:

    def __init__(self, source_table, source_column):
        self.source_table = source_table
        self.source_column = source_column
        self.model_name = '00_Nearest_centroid_table_model.sav'
        self.list_criterion_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'adressen', 'adresstabelle',
                                     'ahkabzinv', 'ahkabzugsart', 'arbeitstabelle', 'b', 'belege', 'belegverknuepfung',
                                     'bereichsuebersicht', 'buchungen', 'buchungssatzprotokoll', 'buchungsstapelliste',
                                     'c', 'd', 'daten', 'debitor', 'debitoren', 'debitoren', 'e', 'f', 'fibu',
                                     'firmenstamm', 'foerderungsart', 'foerdinv', 'g', 'gemeinsame', 'geschaeftsjahre',
                                     'h', 'i', 'inventarbewegung', 'inventarentwicklung', 'inventarstamm',
                                     'investabzug', 'investitionszuordnungabzugsbetrag', 'j', 'journal', 'k', 'konten',
                                     'kontennachweis', 'kontennachweisebilanz', 'kontenplan', 'kontenstamm',
                                     'kontoblatt', 'kontobuchungen', 'kore', 'kostenstelenstamm', 'kostenstellen',
                                     'kreditor', 'kreditoren', 'kreditoren', 'kreditorenstammdaten', 'kunde', 'l',
                                     'lieferant', 'm', 'mandantendaten', 'mandantenstamm', 'monatsverkehrszahlen', 'n',
                                     'o', 'offene', 'ohne', 'p', 'personenkonten', 'posten', 'q', 'r', 'ruecklagen',
                                     's', 'sach', 'sachkonten', 'sachkontenplan', 'salden', 'saldenliste',
                                     'sammelnachweis', 't', 'u', 'unternehmensstamm', 'ustberichtigung', 'ustsollist',
                                     'uststamm', 'v', 'w', 'x', 'y', 'z']
        self.list_importancy_one = ['buchungen_ohne_kore', 'inventarbewegung', 'inventarentwicklung', 'inventarstamm',
                                    'offene_posten']
        self.list_importancy_zero = ['ahkabzinv', 'ahkabzugsart', 'belege', 'belegverknuepfung', 'bereichsuebersicht',
                                     'buchungssatzprotokoll', 'buchungsstapelliste', 'foerderungsart', 'foerdinv',
                                     'investabzug', 'investitionszuordnungabzugsbetrag', 'kontennachweis',
                                     'kontennachweisebilanz', 'kostenstelenstamm_kore', 'monatsverkehrszahlen',
                                     'ruecklagen', 'salden', 'saldenliste', 'ustberichtigung', 'ustsollist', 'uststamm']
        self.list_importance_rest = ['adressen', 'bfi001_arbeitstabelle_konten', 'bfi100_buchungen',
                                     'bfi105_sammelnachweis', 'debitoren', 'debitoren_buchungen_fibu',
                                     'debitoren_kreditorenstammdaten', 'firmenstamm_fibu', 'journal', 'kontenplan',
                                     'kontenstamm', 'kontoblatt', 'kontobuchungen', 'kostenstellen_buchungen_fibu',
                                     'kreditoren', 'kreditoren_buchungen_fibu', 'mandantendaten', 'mandantenstamm',
                                     'offene_posten_fibu', 'personenkonten_fibu', 'sach_buchungen_fibu',
                                     'sachkonten_fibu', 'sachkontenplan', 'sal120_adresstabelle',
                                     'sal501_geschaeftsjahre', 'sde100_debitoren',
                                     'skd121_kunde_debitor_gemeinsame_daten', 'skr100_kreditoren',
                                     'slf121_lieferant_kreditor_gemeinsame_daten_slf1', 'ssk100_sachkonten',
                                     'unternehmensstamm']
        self.dictionary_column_coding_pre_processing = {
            'adressen': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'debitor', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'kreditor', 'l', 'land', 'm', 'n', 'name1', 'name2', 'name3', 'nummer',
                         'o', 'ort', 'p', 'plz', 'q', 'r', 's', 'strasse', 't', 'u', 'v', 'vorname', 'w', 'x', 'y', 'z']
            ,
            'bfi001_arbeitstabelle_konten': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c',
                                             'countermask', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'konto', 'ktoart',
                                             'l', 'm', 'n', 'nrdeb', 'nrkred', 'nrkto', 'o', 'p', 'q', 'r', 's', 't',
                                             'u', 'v', 'w', 'x', 'y', 'z']
            ,
            'bfi100_buchungen': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'ausbuchungsgrund', 'b',
                                 'basiswhrg', 'belegdat', 'belegnr', 'betrag', 'betragausb', 'betragausbwhrg',
                                 'betragnetto', 'betragnettowhrg', 'betragskto', 'betragsktowhrg', 'betragsteuer',
                                 'betragsteuerwhrg', 'betragwhrg', 'bezug', 'bkreis', 'buchcode', 'buchdat', 'buchnr',
                                 'buchpos', 'buchtext', 'c', 'd', 'did', 'e', 'ea', 'eurokurs', 'eurokursbasiswhrg',
                                 'f', 'fremdbelegnr', 'g', 'gegktoart', 'h', 'i', 'j', 'k', 'konto', 'ktoart', 'ktodid',
                                 'kurs', 'kzsteuerangaben', 'kzwu', 'l', 'laendercode', 'leistungsdatum', 'lexport',
                                 'link', 'ltzteditdat', 'ltzteditid', 'm', 'menge', 'n', 'nrbelegre', 'nrbs',
                                 'nrbuchart', 'nrgegkto', 'nrgeldbeleg', 'nrgeschjahr', 'nrjournaldruck',
                                 'nrjournalseite', 'nrkontendruck', 'nrme', 'nrperiode', 'nrprog', 'nrseitereliste',
                                 'nrsession', 'nrstschl', 'o', 'p', 'paginiernr', 'q', 'r', 'referenznr', 's',
                                 'session', 'sollhaben', 'statusflag', 'steuerart', 'steuerproz', 'sto', 't',
                                 'typbuchart', 'typsv', 'u', 'v', 'w', 'whrg', 'x', 'y', 'z']
            ,
            'bfi105_sammelnachweis': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'betragnetto',
                                      'betragnettowhrg', 'betragsteuer', 'betragsteuerwhrg', 'buchnr', 'buchnrbfi100',
                                      'buchpos', 'buchposbfi100', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                                      'ltzteditdat', 'ltzteditid', 'm', 'n', 'nrkto', 'nrsammbuch', 'nrsession',
                                      'nrstschl', 'o', 'p', 'q', 'r', 's', 'samkz', 'sollhaben', 'steuerart', 't', 'u',
                                      'v', 'w', 'whrg', 'x', 'y', 'z', 'zaehler', 'zaehlerbfi107']
            ,
            'debitoren': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'art', 'at', 'auren', 'b', 'bez', 'c',
                          'd', 'e', 'f', 'g', 'h', 'i', 'insert', 'j', 'k', 'konto', 'l', 'land', 'm', 'n', 'nr', 'o',
                          'ort', 'p', 'plz', 'q', 'r', 's', 'stamm', 'strasse', 't', 'u', 'ustid', 'v', 'w', 'x', 'y',
                          'z', 'zus']
            ,
            'debitoren_buchungen_fibu': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8', '9',
                                         'a', 'at', 'auren', 'b', 'belegnr', 'betrag', 'buch', 'buchungsdatum',
                                         'buchungstext', 'c', 'd', 'e', 'eigenwaehrung', 'einheit', 'entgelbetrag',
                                         'entgeltbetr1', 'entgeltbetr2', 'entgeltbetr3', 'entgeltbetr4', 'entgeltbetr5',
                                         'erfassungsdatum', 'ew', 'f', 'fw', 'g', 'gegenkonto', 'geschaeftsjahr', 'h',
                                         'haben', 'i', 'insert', 'j', 'k', 'kurs', 'l', 'land', 'm', 'menge',
                                         'mengeneinheit', 'n', 'name', 'o', 'p', 'pbelegdatum', 'pbelegnummer', 'pbuch',
                                         'periode', 'periodenart', 'perskto', 'pfirma', 'pjournalnummer',
                                         'pjournalzeile', 'pkontonummer', 'pwaehrung', 'q', 'r', 's', 'sammelkonto',
                                         'sammelkto', 'schluessel', 'skontobetr', 'soll', 'steuerart', 'steuerbetr',
                                         'steuerbetrag1', 'steuerbetrag2', 'steuerbetrag3', 'steuerbetrag4',
                                         'steuerbetrag5', 'steuerbezeichn1', 'steuerbezeichn2', 'steuerbezeichn3',
                                         'steuerbezeichn4', 'steuerbezeichn5', 'steuerkonto', 'steuerprozent1',
                                         'steuerprozent2', 'steuerprozent3', 'steuerprozent4', 'steuerprozent5',
                                         'storno', 't', 'transaktionsnummer', 'u', 'v', 'valutadatum', 'verrech', 'w',
                                         'waehr', 'x', 'y', 'z']
            ,
            'debitoren_kreditorenstammdaten': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8',
                                               '9', 'a', 'abwkontoinhaber', 'adressart', 'adressegueltig', 'adresstyp',
                                               'b', 'bankbezeichnung', 'bankkontonr', 'bankv1', 'bankv2', 'bankv3',
                                               'bankv4', 'bankv5', 'bic', 'bis', 'blz', 'c', 'd', 'e', 'eu', 'f', 'g',
                                               'geschaeftspartner', 'gueltig', 'h', 'i', 'iban', 'j', 'k',
                                               'kzgeschaeftspbank', 'l', 'laenderkz', 'land', 'm', 'n', 'nachname',
                                               'name', 'nation', 'o', 'ort', 'p', 'pkktonr', 'plz', 'postfach', 'q',
                                               'r', 's', 'steuernummer', 'strasse', 't', 'typ', 'u', 'unternehmen',
                                               'unternehmensgegenst', 'ustid', 'v', 'von', 'vorname', 'w', 'x', 'y',
                                               'z']
            ,
            'firmenstamm_fibu': ['0', '1', '1', '2', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'alte',
                                 'anmeldezeitraum', 'at', 'auren', 'b', 'bundesland', 'c', 'd', 'e', 'eigenwaehr',
                                 'eigenwaehrung', 'erste', 'f', 'finanzamt', 'g', 'h', 'i', 'id', 'insert', 'j', 'k',
                                 'kalenderjahr', 'kurzanschrift', 'l', 'land', 'letzte', 'm', 'n', 'name', 'name1',
                                 'name2', 'nr', 'o', 'ort', 'p', 'periode', 'pfirma', 'pgeschaeftjahr', 'postf',
                                 'postleitzahl', 'q', 'r', 'region', 's', 'steuernr', 'str', 'strasse', 't', 'u', 'ust',
                                 'uva', 'v', 'w', 'x', 'y', 'z']
            ,
            'journal': ['0', '1', '13b', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'art', 'at', 'auren', 'b',
                        'belegdatum', 'belegnummer', 'betrag', 'bez', 'bu', 'buchungsbetrag', 'buchungsnummer',
                        'buchungstext', 'buja', 'c', 'd', 'dat', 'e', 'erf', 'f', 'fest', 'g', 'gkto', 'h', 'haben',
                        'habenbetrag', 'habenkonto', 'hbk', 'i', 'id', 'ige', 'insert', 'j', 'k', 'konto', 'l', 'm',
                        'n', 'o', 'p', 'periode', 'q', 'r', 's', 'schl', 'soll', 'sollbetrag', 'sollkonto', 'st',
                        'steuerprozentsatz', 't', 'u', 'ust', 'v', 'vaz', 'w', 'x', 'y', 'z']
            ,
            'kontenplan': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'art', 'at', 'auren', 'b', 'bez',
                           'c', 'd', 'e', 'f', 'g', 'grp', 'h', 'haben', 'i', 'insert', 'j', 'k', 'konto', 'kto', 'l',
                           'm', 'n', 'nr', 'o', 'p', 'q', 'r', 's', 'soll', 't', 'typ', 'u', 'v', 'w', 'x', 'y', 'z',
                           'zus']
            ,
            'kontenstamm': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'bankkontonr', 'bankleitzahl',
                            'banknr', 'bezeichnung', 'bezeichnung2', 'c', 'd', 'dvkontonummer', 'e', 'f', 'g', 'h', 'i',
                            'j', 'k', 'klasse', 'kontonummer', 'l', 'm', 'matchcode', 'n', 'o', 'p', 'q', 'r', 's',
                            'steuernummer', 't', 'u', 'ustidentnr', 'v', 'w', 'x', 'y', 'z']
            ,
            'kontoblatt': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'at', 'auren', 'b', 'belegdatum',
                           'belegnummer', 'buchungsnummer', 'buchungstext', 'c', 'd', 'e', 'f', 'g', 'gegenkonto',
                           'gkto', 'h', 'habenbetrag', 'hbk', 'i', 'insert', 'j', 'k', 'konto', 'kontobezeichnung',
                           'kontonummer', 'l', 'm', 'n', 'o', 'p', 'periode', 'proz', 'q', 'r', 's', 'sollbetrag', 't',
                           'u', 'ust', 'v', 'vst', 'w', 'x', 'y', 'z']
            ,
            'kontobuchungen': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'abwbesteuerungsart', 'b',
                               'basiswaehrung', 'bearbeitungsstatus', 'belegdatum', 'belegfeld2', 'belegidentifikator',
                               'beleglink', 'belegnummer', 'belegpruefungsstatus', 'bereichsid', 'beteiligtennummer',
                               'bsnr', 'bu', 'buchungstext', 'buchungstyp', 'c', 'd', 'datumzuordsteuerperiode', 'e',
                               'eb', 'eingeg', 'eingegumsatz', 'eustsatz', 'f', 'faelligkeit', 'fktergschl49',
                               'folgebuchungszaehler', 'funktionserglul', 'g', 'gesellschaftername', 'gewicht',
                               'gktonr', 'h', 'haben', 'hauptfktnrschl49', 'hauptfkttypschl49', 'herkunftskz', 'i',
                               'identifikationsnummer', 'j', 'k', 'kennung', 'kontobewegungstyp', 'kontorolle',
                               'kost1', 'kost2', 'ktonr', 'kurs', 'l', 'leistungsdatum', 'm', 'menge1wert', 'n', 'o',
                               'p', 'q', 'r', 's', 'sachverhaltlul', 'schl', 'shkz', 'soll', 'stapelidentifikator',
                               'stapelnummer', 'steuersatz', 'stueck', 't', 'u', 'umsatz', 'v', 'w', 'wjmonat', 'wkz',
                               'x', 'y', 'z', 'zeichnernummer']
            ,
            'kostenstellen_buchungen_fibu': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'at', 'auren', 'b',
                                             'belegnr', 'betrag', 'buch', 'buchungsdatum', 'buchungstext', 'c', 'd',
                                             'e', 'erfassungsdatum', 'ew', 'f', 'g', 'geschaeftsjahr', 'h', 'haben',
                                             'i', 'insert', 'j', 'k', 'kostenart', 'l', 'm', 'menge', 'mengeneinheit',
                                             'n', 'o', 'p', 'pbelegdatum', 'pbelegnummer', 'pbuch', 'periode',
                                             'periodenart', 'pfirma', 'pjournalnummer', 'pjournalzeile',
                                             'pkostenstelle1', 'pkostenstelle2', 'pwaehrung', 'q', 'r', 's',
                                             'schluessel', 'soll', 't', 'transaktionsnummer', 'u', 'v', 'verrech', 'w',
                                             'x', 'y', 'z']
            ,
            'kreditoren': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'art', 'at', 'auren', 'b', 'bez',
                           'c', 'd', 'e', 'f', 'g', 'h', 'i', 'insert', 'j', 'k', 'konto', 'l', 'land', 'm', 'n', 'nr',
                           'o', 'ort', 'p', 'plz', 'q', 'r', 's', 'stamm', 'strasse', 't', 'u', 'ustid', 'v', 'w', 'x',
                           'y', 'z', 'zus']
            ,
            'kreditoren_buchungen_fibu': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8', '9',
                                          'a', 'at', 'auren', 'b', 'belegnr', 'betrag', 'buch', 'buchungsdatum',
                                          'buchungstext', 'c', 'd', 'e', 'eigenwaehrung', 'einheit', 'entgelbetrag',
                                          'entgeltbetr1', 'entgeltbetr2', 'entgeltbetr3', 'entgeltbetr4',
                                          'entgeltbetr5', 'erfassungsdatum', 'ew', 'f', 'fw', 'g', 'gegenkonto',
                                          'geschaeftsjahr', 'h', 'haben', 'i', 'insert', 'j', 'k', 'kurs', 'l', 'land',
                                          'm', 'menge', 'mengeneinheit', 'n', 'name', 'o', 'p', 'pbelegdatum',
                                          'pbelegnummer', 'pbuch', 'periode', 'periodenart', 'perskto', 'pfirma',
                                          'pjournalnummer', 'pjournalzeile', 'pkontonummer', 'pwaehrung', 'q', 'r',
                                          's', 'sammelkonto', 'sammelkto', 'schluessel', 'skontobetr', 'soll',
                                          'steuerart', 'steuerbetr', 'steuerbetrag1', 'steuerbetrag2', 'steuerbetrag3',
                                          'steuerbetrag4', 'steuerbetrag5', 'steuerbezeichn1', 'steuerbezeichn2',
                                          'steuerbezeichn3', 'steuerbezeichn4', 'steuerbezeichn5', 'steuerkonto',
                                          'steuerprozent1', 'steuerprozent2', 'steuerprozent3', 'steuerprozent4',
                                          'steuerprozent5', 'storno', 't', 'transaktionsnummer', 'u', 'v',
                                          'valutadatum', 'verrech', 'w', 'waehr', 'x', 'y', 'z']
            ,
            'mandantendaten': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'anlagenspiegel', 'anrede', 'b',
                               'basiswaehrung', 'beginn', 'besteuerungsart', 'bis', 'bnr', 'c', 'd', 'datum', 'e',
                               'email', 'ende', 'erw2', 'erw3', 'eu', 'euland', 'f', 'fax', 'festschreibung',
                               'finanzamtsnummer', 'g', 'gebucht', 'h', 'i', 'indiv', 'individ', 'internet', 'j',
                               'jahr', 'k', 'k', 'kanz', 'kanzlei', 'ktobeschr', 'ktofkt', 'l', 'laengesachkontonr',
                               'm', 'mnr', 'mobiltelefon', 'n', 'nationales', 'o', 'ort', 'p', 'plz', 'postfach', 'q',
                               'r', 'recht', 's', 'skr', 'std', 'steuernummer', 'strasse', 't', 'telefon', 'u',
                               'unternehmensform', 'unternehmensgegenst', 'unternehmensn', 'unternehmensname',
                               'unternehmensnerw1', 'ustid', 'v', 'vkz', 'vollhgesellschanzahl', 'voranmeldungszeitr',
                               'w', 'wj', 'x', 'y', 'z']
            ,
            'mandantenstamm': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'ab', 'at', 'auren', 'auto', 'b',
                               'bez', 'bis', 'c', 'd', 'e', 'f', 'festschreibung', 'firma', 'g', 'h', 'i', 'id',
                               'insert', 'j', 'jahr', 'k', 'l', 'm', 'monat', 'n', 'nr', 'nummer', 'o', 'p', 'periode',
                               'q', 'r', 's', 'steuer', 't', 'u', 'v', 'von', 'w', 'waehrung', 'wj', 'x', 'y', 'z',
                               'zus']
            ,
            'offene_posten_fibu': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8', '9', 'a',
                                   'art', 'at', 'auren', 'b', 'belegdatum', 'belegnr', 'betrag', 'buch',
                                   'buchungsperiode', 'c', 'd', 'e', 'eigenwaehrung', 'einheit', 'entgelbetrag',
                                   'entgeltbetr1', 'entgeltbetr2', 'entgeltbetr3', 'entgeltbetr4', 'entgeltbetr5',
                                   'ew', 'f', 'faelligkeitsdat', 'fremdbeleg', 'fw', 'g', 'h', 'i', 'insert', 'j', 'k',
                                   'kurs', 'l', 'm', 'mahnstufe', 'n', 'name', 'o', 'p', 'pbelegnummer', 'pfirma',
                                   'pkontonummer', 'plfd', 'pop', 'q', 'r', 's', 'sammelkonto', 'sammelkto',
                                   'schluessel', 'status', 'steuerart', 'steuerbetr', 'steuerbetrag1', 'steuerbetrag2',
                                   'steuerbetrag3', 'steuerbetrag4', 'steuerbetrag5', 'steuerbezeichn1',
                                   'steuerbezeichn2', 'steuerbezeichn3', 'steuerbezeichn4', 'steuerbezeichn5',
                                   'steuerkonto', 'steuerprozent1', 'steuerprozent2', 'steuerprozent3',
                                   'steuerprozent4', 'steuerprozent5', 't', 'text', 'u', 'v', 'valutadatum', 'verrech',
                                   'w', 'waehr', 'waehrung', 'x', 'y', 'z']
            ,
            'personenkonten_fibu': ['0', '1', '1', '2', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'at', 'auren',
                                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'id', 'insert', 'j', 'k', 'kontoart',
                                    'kurzanschrift', 'l', 'land', 'm', 'n', 'name', 'nr', 'o', 'ort', 'p', 'pfirma',
                                    'pkontonummer', 'postf', 'postleitzahl', 'q', 'r', 'region', 's', 'strasse', 't',
                                    'u', 'ust', 'v', 'w', 'x', 'y', 'z']
            ,
            'sach_buchungen_fibu': ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8', '9', 'a',
                                    'at', 'auren', 'b', 'belegnr', 'betrag', 'buch', 'buchungsdatum', 'buchungstext',
                                    'c', 'd', 'e', 'eigenwaehrung', 'einheit', 'entgelbetrag', 'entgeltbetr1',
                                    'entgeltbetr2', 'entgeltbetr3', 'entgeltbetr4', 'entgeltbetr5', 'erfassungsdatum',
                                    'ew', 'f', 'fw', 'g', 'gegenkonto', 'geschaeftsjahr', 'h', 'haben', 'i', 'insert',
                                    'j', 'k', 'kurs', 'l', 'land', 'm', 'menge', 'mengeneinheit', 'n', 'name', 'o',
                                    'p', 'pbelegdatum', 'pbelegnummer', 'pbuch', 'periode', 'periodenart', 'perskto',
                                    'pfirma', 'pjournalnummer', 'pjournalzeile', 'pkontonummer', 'pwaehrung', 'q', 'r',
                                    's', 'sammelkonto', 'sammelkto', 'schluessel', 'skontobetr', 'soll', 'steuerart',
                                    'steuerbetr', 'steuerbetrag1', 'steuerbetrag2', 'steuerbetrag3', 'steuerbetrag4',
                                    'steuerbetrag5', 'steuerbezeichn1', 'steuerbezeichn2', 'steuerbezeichn3',
                                    'steuerbezeichn4', 'steuerbezeichn5', 'steuerkonto', 'steuerprozent1',
                                    'steuerprozent2', 'steuerprozent3', 'steuerprozent4', 'steuerprozent5', 'storno',
                                    't', 'transaktionsnummer', 'u', 'v', 'valutadatum', 'verrech', 'w', 'waehr', 'x',
                                    'y', 'z']
            ,
            'sachkonten_fibu': ['0', '1', '1', '2', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'art', 'at', 'auren',
                                'b', 'bezeichnung', 'brutto', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'insert', 'j', 'k',
                                'kontenart', 'kto', 'l', 'm', 'n', 'netto', 'o', 'p', 'pfirma', 'pkontonummer', 'q',
                                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'zusatzbezeich']
            ,
            'sachkontenplan': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'anspfkt', 'b', 'c', 'd', 'e',
                               'f', 'f2kto1', 'f2kto2', 'f2proz', 'fkterg', 'g', 'h', 'hfnr', 'hktyp', 'i',
                               'ifktbeschr', 'j', 'k', 'ktonr', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'text',
                               'u', 'v', 'w', 'x', 'y', 'z', 'zusfkt']
            ,
            'sal120_adresstabelle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'adrtyp', 'adrzu',
                                     'anrede', 'b', 'briefanrede', 'c', 'd', 'e', 'ersteditdat', 'ersteditid', 'f',
                                     'fmna', 'g', 'h', 'hausnr', 'i', 'j', 'k', 'l', 'land', 'landkz', 'lkzplzort',
                                     'ltzteditdat', 'ltzteditid', 'm', 'n', 'name1', 'name2', 'name3', 'nazu',
                                     'normcode', 'nradr', 'nrbundesland', 'o', 'ort', 'p', 'plz', 'postfach',
                                     'postfachplz', 'q', 'r', 's', 'satzdid', 'str', 'strasse', 'suchname', 't',
                                     'titel', 'u', 'v', 'vona', 'vosa', 'w', 'x', 'xkoord', 'y', 'ykoord', 'z',
                                     'zusatz1', 'zusatz2']
            ,
            'sal501_geschaeftsjahre': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'abgeschlossen',
                                       'abschlussdat', 'b', 'bez', 'c', 'd', 'e', 'ebkdeb', 'ebkkred', 'ebksk',
                                       'eroeffnet', 'ersteditdat', 'ersteditid', 'f', 'folgejahr', 'g', 'h', 'i', 'j',
                                       'k', 'l', 'ltzteditdat', 'ltzteditid', 'm', 'n', 'nrgeschjahr', 'o', 'p', 'q',
                                       'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            ,
            'sde100_debitoren': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'datltzteinzug',
                                 'datltztra', 'e', 'ersteditdat', 'ersteditid', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                                 'ltzteditdat', 'ltzteditid', 'm', 'n', 'nrbank', 'nrdeb', 'nrsal121', 'nrskd121',
                                 'nrzr', 'o', 'p', 'q', 'r', 's', 'satzdid', 'satzstatus', 'sepaidentifier', 't', 'u',
                                 'v', 'w', 'x', 'y', 'z']
            ,
            'skd121_kunde_debitor_gemeinsame_daten': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'aktzei',
                                                      'autoinkasso', 'automahn', 'b', 'bondatpruefung',
                                                      'bonkennziffer', 'c', 'code1', 'code2', 'code3', 'code4', 'd',
                                                      'diverse', 'e', 'einzgueltigbis', 'einzgueltigvon', 'ersteditdat',
                                                      'ersteditid', 'eust', 'f', 'facbank', 'facbanknr', 'fordgruppe',
                                                      'g', 'h', 'i', 'j', 'k', 'kreditextern', 'kreditintern',
                                                      'kredvers', 'kredversnr', 'l', 'ltzteditdat', 'ltzteditid', 'm',
                                                      'mahnadrabw', 'mahngruppe', 'mahnsperrdat', 'mahnsperrtext',
                                                      'mwst', 'n', 'nrabc', 'nradr', 'nrauto', 'nrksttrg', 'nrprojekt',
                                                      'nrzahlart', 'o', 'p', 'prov1', 'prov2', 'prov3', 'q', 'r',
                                                      'refnr', 's', 'steuernummer', 't', 'typsperrung', 'u', 'ustcode',
                                                      'ustermittlung', 'v', 'valuta', 'verbkdnr', 'verbnr',
                                                      'verktokred', 'vertr1', 'vertr2', 'vertr3', 'w', 'whrg', 'x',
                                                      'y', 'z', 'zahlkond', 'zustfinanz', 'zustservice', 'zusttechnik',
                                                      'zustvertrieb']
            ,
            'skr100_kreditoren': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'datltztre',
                                  'e', 'ersteditdat', 'ersteditid', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ltzteditdat',
                                  'ltzteditid', 'm', 'n', 'nrbank', 'nrkred', 'nrslf121', 'o', 'p', 'q', 'r', 's',
                                  'satzdid', 'satzstatus', 'sepaidentifier', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            ,
            'slf121_lieferant_kreditor_gemeinsame_daten_slf1': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
                                                                'aktzei', 'automahn', 'autozahl', 'autozahlbis',
                                                                'autozahlvon', 'b', 'c', 'code1', 'code2', 'code3',
                                                                'code4', 'd', 'diverse', 'e', 'einzgueltigbis',
                                                                'einzgueltigvon', 'eust', 'f', 'facbank', 'facbanknr',
                                                                'g', 'h', 'i', 'j', 'k', 'kredit', 'l', 'ltzteditdat',
                                                                'ltzteditid', 'm', 'mahnadrabw', 'mahngruppe',
                                                                'mahnsperrdat', 'mahnsperrtext', 'n', 'nrabc', 'nradr',
                                                                'nrauto', 'o', 'p', 'q', 'r', 'refnr', 's', 't',
                                                                'typsperrung', 'u', 'v', 'valuta', 'verbgruppe',
                                                                'verkto', 'vstcode', 'vstermittlung', 'w', 'whrg', 'x',
                                                                'y', 'z', 'zahlart', 'zahlkond', 'zusteinkauf',
                                                                'zustfinanz', 'zustservice', 'zusttechnik']
            ,
            'ssk100_sachkonten': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'automsaldovortrag', 'b',
                                  'bez', 'bez1', 'buchen', 'c', 'd', 'e', 'ebksk', 'ersteditdat', 'ersteditid', 'f',
                                  'fremdwhrg', 'g', 'gltgbis', 'gltgvon', 'h', 'i', 'isskf', 'j', 'k', 'kostenarten',
                                  'kstrgplanung', 'kststl', 'ksttrg', 'ktoart', 'ktokl', 'l', 'ltzteditdat',
                                  'ltzteditid', 'm', 'mengeneingabe', 'mengeneinheit', 'n', 'nrdatev', 'nrkstart',
                                  'nrkto', 'nrktr', 'nrprojekt', 'nrstschl', 'o', 'opverdichtung', 'p', 'projekt', 'q',
                                  'r', 's', 'sammelbuch', 'sammeln', 'satzdid', 'satzstatus', 'skontoktodid',
                                  'sperrgrund', 'steuerart', 't', 'txtnr', 'u', 'v', 'w', 'whrg', 'x', 'y', 'z']
            ,
            'unternehmensstamm': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'additiv', 'at', 'aufwand',
                                  'auren', 'ausgabe', 'b', 'bezeichnung', 'c', 'c13b', 'd', 'dreieck', 'e', 'f',
                                  'faellig', 'g', 'gr', 'gruppe', 'h', 'i', 'ig', 'insert', 'j', 'k', 'konto',
                                  'kurzbez', 'l', 'leist', 'm', 'n', 'o', 'ohne', 'p', 'pagat', 'q', 'r', 's', 'schl',
                                  'skontoaufwand', 'skontoertrag', 'sons', 'st', 'steuersatz', 't', 'u', 'ust', 'v',
                                  'vst', 'w', 'x', 'y', 'z', 'zeile', 'zeilen', 'zm']
        }
        self.list_table_vector = []
        self.list_importance_results = []

    def table_pre_processing(self):
        for item in self.source_table:
            temp = []
            for i in self.list_criterion_table:
                num = item.count(i)
                num_weight = num * (len(i))
                temp.append(num_weight)
            self.list_table_vector.append(temp)

    def table_predict(self):
        self.table_pre_processing()
        path = 'importance_evaluation'
        load_file = os.path.join(path, self.model_name)
        classifier = pickle.load(open(load_file, 'rb'))
        table_analysis_result = classifier.predict(self.list_table_vector)
        return table_analysis_result

    def column_coding(self, table_name, column_name):
        column_model_coding_method = self.dictionary_column_coding_pre_processing[table_name]
        column_coding = []
        for i in column_model_coding_method:
            num = column_name.count(i)
            num_weight = num * (len(i))
            column_coding.append(num_weight)
        return column_coding

    def importance_predict(self, table_result):

        for item in range(len(table_result)):
            if table_result[item] in self.list_importancy_one:
                self.list_importance_results.append('1')
            if table_result[item] in self.list_importancy_zero:
                self.list_importance_results.append('0')
            if table_result[item] in self.list_importance_rest:
                column_model = table_result[item] + '.sav'
                path = 'importance_evaluation'
                load_file = os.path.join(path, column_model)
                classifier = pickle.load(open(load_file, 'rb'))
                column_coding_vector = self.column_coding(table_result[item], self.source_column[item])
                result_group = classifier.predict_proba([column_coding_vector])
                self.list_importance_results.append(result_group[0][1])
        return self.list_importance_results

"""
if __name__ == '__main__':
    Start = Evaluation(['debitoren_buchungen_fibu_qdf', 'debitoren_kreditorenstammdaten', 'inventarstamm',
                        'inventarbewegung', 'investitionszuordnungabzugsbetrag'], ['valutadatum_rer9t', 'Ort',
                         'AfaArtText', 'IntNrBeweg', 'RueckBez'])
    print(Start.importance_predict(Start.table_predict()))
"""

