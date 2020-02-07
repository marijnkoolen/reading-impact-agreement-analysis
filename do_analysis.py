import impact_model_analysis
import human_rater_analysis
import mann_whitney_u_test
import plot
from config import config


def do_model_agreement_analysis(sentence_ratings: list, ira_threshold: float, config: dict):
    model_agreement_high = {}
    model_agreement_low = {}
    for impact_scale in config['impact_scales']:
        sentences_high_ira = human_rater_analysis.get_sentences_high_ira(sentence_ratings, impact_scale, ira_threshold)
        sentences_low_ira = human_rater_analysis.get_sentences_low_ira(sentence_ratings, impact_scale, ira_threshold)
        model_agreement_high[impact_scale] = impact_model_analysis.get_model_agreement(sentences_high_ira, impact_scale)
        model_agreement_low[impact_scale] = impact_model_analysis.get_model_agreement(sentences_low_ira, impact_scale)
        ignored = len(sentence_ratings) - len(sentences_high_ira) - len(sentences_low_ira)
        print("  Total sentences:",len(sentence_ratings),
              f"\tIRA >= ({ira_threshold}):", len(sentences_high_ira),
              f"\tIRA < ({ira_threshold}):", len(sentences_low_ira),
              f"\tIgnored (1 or 0 non-NA ratings):", ignored)
        plot.plot_agreement_model_bubble(impact_scale, model_agreement_high, f"IRA >= {ira_threshold}")
        plot.plot_agreement_model_bubble(impact_scale, model_agreement_low, f"IRA < {ira_threshold}")
    impact_model_analysis.write_model_agreement_table(model_agreement_high, model_agreement_low,
                                                      ira_threshold, config)


def do_analysis():
    print("Reading human ratings")
    sentence_ratings = human_rater_analysis.get_sentence_ratings(config['ratings_file'])
    print("Plotting rating distribution")
    plot.plot_num_annotations_distribution(sentence_ratings)
    print("Filtering sentences with at least 3 raters")
    sentences_done = [sentence for sentence in sentence_ratings if sentence["annotation_status"] == "done"]
    print("Reading alpino parses of sentences")
    sentence_alpino_data = impact_model_analysis.read_tarred_sentences(config['alpino_sentences_file'])
    print("Scoring sentences on reading impact")
    impact_model_analysis.score_impact_sentences(sentences_done, sentence_alpino_data, config)
    print("Writing human and model ratings to spreadsheet")
    human_rater_analysis.write_rating_spreadsheet(sentences_done, config)
    for ira_threshold in [0.5, 0.7]:
        print(f"Plotting human model rating agreement for IRA >= {ira_threshold}")
        do_model_agreement_analysis(sentences_done, ira_threshold, config)
        print(f"Performing Mann-Whitney U test for IRA >= {ira_threshold}")
        mann_whitney_u_test.do_mann_whitney_u_test(sentences_done, ira_threshold=ira_threshold)
        print(f"Making model boxplots for IRA>= {ira_threshold}")
        plot.do_model_box_plot(sentences_done, ira_threshold=ira_threshold)


if __name__ == "__main__":
    do_analysis()
