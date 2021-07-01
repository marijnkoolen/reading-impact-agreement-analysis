
config = {
    # The judgements file contains human rater judgements on impact for 2743 sentences
    'ratings_file': '../data_nl/impact_judgements-2019-06-27.json',
    # The sentences_file contains 2743 json files, each with an Alpino parsed sentence from the questionnaire data
    'alpino_sentences_file': '../data_nl/reading_impact_questionnaire_sentences.tar.gz',
    # impact_model.pcl contains the impact rules
    'impact_model_file': '../data_nl/impact_model.pcl',
    # impact scales
    'impact_scales': ['emotional_scale', 'style_scale', 'reflection_scale', 'narrative_scale'],
    'spreadsheet_file': '../data_nl/reading_impact_questionnaire_data.xlsx',
    # directory for data files
    'data_dir': '../data_nl/',
    # directory for generated images
    'image_dir': '../images_nl/',
    # aggregated impact per review for a selection of novels
    'aggr_impact_file': '../data_nl/top_268-review_sentences_100000-impact-per-review.csv'
}

