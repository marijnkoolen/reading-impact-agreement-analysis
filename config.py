
config = {
    # The judgements file contains human rater judgements on impact for 2743 sentences
    'ratings_file': 'data/impact_judgements-2019-06-27.json',
    # The sentences_file contains 2743 json files, each with an Alpino parsed sentence from the questionnaire data
    'alpino_sentences_file': 'data/reading_impact_questionnaire_sentences.tar.gz',
    # impact_model.pcl contains the impact rules
    'impact_model_file': 'data/impact_model.pcl',
    # impact scales
    'impact_scales': ['emotional_scale', 'style_scale', 'reflection_scale', 'narrative_scale'],
    'spreadsheet_file': 'reading_impact_questionnaire_data.xlsx',
    # directory for generated images
    'image_dir': 'images/'
}

