import column_classifier
# the file name, no number for first letter


if __name__ == "__main__":
    a_fiscal_classifier = column_classifier.Classifier("a_fiscal", "column_02_a_fiscal_model.sav")
    a_fiscal_classifier.corpus_extract()
    a_fiscal_classifier.data_processing_training(a_fiscal_classifier.list_vector_base)
    a_fiscal_classifier.model_test()
