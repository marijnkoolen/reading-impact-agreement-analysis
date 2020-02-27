from collections import Counter, defaultdict
import statistics as stats

import impact_model_analysis
import human_rater_analysis
import mann_whitney_u_test
import plot
from config import config


def do_model_agreement_analysis(sentence_ratings: list, ira_threshold: float, config: dict):
    model_agreement_high = {}
    model_agreement_low = {}
    print(f'\n\tImpact scale    \tTotal sentences\tIRA >= {ira_threshold}\tIRA < {ira_threshold}'
          + '\tIgnored (1 or 0 non-NA ratings)')
    for impact_scale in config['impact_scales']:
        sentences_high_ira = human_rater_analysis.get_sentences_high_ira(sentence_ratings, impact_scale,
                                                                         ira_threshold, config['null_dist'])
        sentences_low_ira = human_rater_analysis.get_sentences_low_ira(sentence_ratings, impact_scale,
                                                                       ira_threshold, config['null_dist'])
        model_agreement_high[impact_scale] = impact_model_analysis.get_model_agreement(sentences_high_ira, impact_scale)
        model_agreement_low[impact_scale] = impact_model_analysis.get_model_agreement(sentences_low_ira, impact_scale)
        ignored = len(sentence_ratings) - len(sentences_high_ira) - len(sentences_low_ira)
        print(f'\t{impact_scale: <20}\t{len(sentence_ratings)}\t\t{len(sentences_high_ira)}\t\t{len(sentences_low_ira)}\t\t{ignored}')
    impact_model_analysis.write_model_agreement_table(model_agreement_high, model_agreement_low,
                                                      ira_threshold, config)


def show_rating_distribution(sentence_ratings: list):
    freq = defaultdict(Counter)
    scale_ratings = defaultdict(list)
    for sentence in sentence_ratings:
        impact_scales = ['emotional_scale', 'style_scale', 'reflection_scale', 'narrative_scale']
        for impact_scale in impact_scales:
            ratings = [int(annotation[impact_scale]) for annotation in sentence['annotations'] if impact_scale in annotation and annotation[impact_scale].isdigit()]
            if len(ratings) < 2:
                continue
            scale_ratings[impact_scale] += ratings
            scale_ratings['all'] += ratings
            freq[impact_scale].update(ratings)
            freq['all'].update(ratings)
    impact_scales = ['emotional_scale', 'style_scale', 'reflection_scale', 'narrative_scale']
    for impact_scale in impact_scales + ['all']:
        total = len(scale_ratings[impact_scale])
        print(f'\n\t{impact_scale}')
        for rating in range(0,5):
            ratio = round(freq[impact_scale][rating] / total, 2)
            print('\t\trating:', rating, '\tfreq:', freq[impact_scale][rating], '\tratio:', ratio)
        print('\t\tmean:', stats.mean(scale_ratings[impact_scale]), 'variance:', stats.pvariance(scale_ratings[impact_scale]))
    plot.plot_rating_probability(freq['all'])


def do_analysis():
    print("Reading human ratings")
    sentence_ratings = human_rater_analysis.get_sentence_ratings(config['ratings_file'])
    print("Plotting rating distribution")
    plot.plot_num_annotations_distribution(sentence_ratings)
    print("\nRemoving sentences with fewer than 3 raters")
    sentences_done = [sentence for sentence in sentence_ratings if sentence["annotation_status"] == "done"]
    print('\nAnalyzing null distributions')
    show_rating_distribution(sentences_done)
    print("\nReading alpino parses of sentences")
    sentence_alpino_data = impact_model_analysis.read_tarred_sentences(config['alpino_sentences_file'])
    print("Scoring sentences on reading impact")
    impact_model_analysis.score_impact_sentences(sentences_done, sentence_alpino_data, config)
    print("Writing human and model ratings to spreadsheet")
    human_rater_analysis.write_rating_spreadsheet(sentences_done, config)
    print('\nCalculating interrater agreement using the inverse triangular null-distribution')
    ira_dist = human_rater_analysis.get_ira_dist(sentences_done, 'inverse_triangular')
    plot.plot_per_sentence_ira_dist(ira_dist)
    config['null_dist'] = 'inverse_triangular'
    for ira_threshold in [0.5]: #, 0.7]:
        print(f"\nPlotting human model rating agreement for IRA >= {ira_threshold}")
        do_model_agreement_analysis(sentences_done, ira_threshold, config)
        print(f"\nPerforming Mann-Whitney U test for IRA >= {ira_threshold}")
        mann_whitney_u_test.do_mann_whitney_u_test(sentences_done, ira_threshold, config)
        print(f"\nMaking model boxplots for IRA>= {ira_threshold}")
        plot.do_model_box_plot(sentences_done, ira_threshold, config)
        print()


if __name__ == "__main__":
    do_analysis()
