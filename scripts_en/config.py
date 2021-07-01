
config = {
    # The judgements file contains human rater judgements on impact for 2743 sentences
    'ratings_file': '../data_en/sentences_done.json',
    # impact_model.pcl contains the impact rules
    'impact_model_file': '../data_en/impact_model.pcl',
    # impact scales
    'spreadsheet_file': '../data_en/reading_impact_questionnaire_data.xlsx',
    # directory for data files
    'data_dir': '../data_en/',
    # directory for generated images
    'image_dir': '../images_en/',
    # aggregated impact per review for a selection of novels
    'aggr_impact_file': '../data_en/top_268-review_sentences_100000-impact-per-review.csv',
    'impact_scales': [
        'emotional_scale', 'style_scale', 'reflection_scale', 'narrative_scale',
        'surprise_scale', 'attention_scale', 'negative_scale', 'humor_scale'
    ]
}

