import column_classifier
# the file name, no number for first letter


if __name__ == "__main__":
    a_fiscal_classifier = column_classifier.Classifier("a_collective_statement",
                                                       "column_05_a_collective_statement_model.sav")
    a_fiscal_classifier.corpus_extract()
    a_fiscal_classifier.data_processing_training(a_fiscal_classifier.list_vector_base)
    a_fiscal_classifier.model_test()
