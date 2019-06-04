import column_classifier
# the file name, no number for first letter


if __name__ == "__main__":
    a_fiscal_classifier = column_classifier.Classifier("a_posting_record",
                                                       "column_11_a_posting_record_model.sav")
    a_fiscal_classifier.corpus_extract()
    a_fiscal_classifier.data_processing_training(a_fiscal_classifier.list_vector_base02)
    a_fiscal_classifier.model_test()
