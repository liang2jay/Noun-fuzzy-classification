from sklearn.neighbors.nearest_centroid import NearestCentroid
import numpy as np
import pickle


class Classify:

    def __init__(self):
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

        self.list_table = ['adressen', 'ahkabzinv', 'ahkabzugsart', 'belege', 'belegverknuepfung', 'bereichsuebersicht',
                           'bfi001_arbeitstabelle_konten', 'bfi100_buchungen', 'bfi105_sammelnachweis',
                           'buchungen_ohne_kore', 'buchungssatzprotokoll', 'buchungsstapelliste', 'debitoren',
                           'debitoren_buchungen_fibu', 'debitoren_kreditorenstammdaten', 'firmenstamm_fibu',
                           'foerderungsart', 'foerdinv', 'inventarbewegung', 'inventarentwicklung', 'inventarstamm',
                           'investabzug', 'investitionszuordnungabzugsbetrag', 'journal', 'kontennachweis',
                           'kontennachweisebilanz', 'kontenplan', 'kontenstamm', 'kontoblatt', 'kontobuchungen',
                           'kostenstelenstamm_kore', 'kostenstellen_buchungen_fibu', 'kreditoren',
                           'kreditoren_buchungen_fibu', 'mandantendaten', 'mandantenstamm', 'monatsverkehrszahlen',
                           'offene_posten', 'offene_posten_fibu', 'personenkonten_fibu', 'ruecklagen',
                           'sach_buchungen_fibu', 'sachkonten_fibu', 'sachkontenplan', 'sal120_adresstabelle',
                           'sal501_geschaeftsjahre', 'salden', 'saldenliste', 'sde100_debitoren',
                           'skd121_kunde_debitor_gemeinsame_daten', 'skr100_kreditoren',
                           'slf121_lieferant_kreditor_gemeinsame_daten_slf1', 'ssk100_sachkonten', 'unternehmensstamm',
                           'ustberichtigung', 'ustsollist', 'uststamm']

        self.list_table_vector = []
        self.model_name = '00_Nearest_centroid_table_model.sav'
        self.X_test = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1, 0, 0, 0, 1]]

    def pre_processing(self):
        for item in self.list_table:
            temp = []
            for i in self.list_criterion_table:
                num = item.count(i)
                num_weight = num * (len(i))
                temp.append(num_weight)
            self.list_table_vector.append(temp)

    def training(self):

        list_table_vector = self.list_table_vector
        list_table = self.list_table
        for num in range(1, 200):
            self.list_table_vector = self.list_table_vector + list_table_vector
            self.list_table = self.list_table + list_table

        X = np.array(self.list_table_vector)
        y = np.array(self.list_table)
        classify = NearestCentroid()
        classify.fit(X, y)
        pickle.dump(classify, open(self.model_name, 'wb'))

    def evaluate(self):
        classifier = pickle.load(open(self.model_name, 'rb'))
        print(classifier.predict(self.X_test))


if __name__ == '__main__':
    KNN_classify = Classify()
    KNN_classify.pre_processing()
    KNN_classify.training()
    KNN_classify.evaluate()


















