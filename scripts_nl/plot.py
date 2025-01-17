from typing import Dict
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

import impact_model_analysis
from config import config


def plot_num_annotations_distribution(sentence_ratings: list) -> None:
    annotator_freq = Counter()
    for sentence in sentence_ratings:
        if sentence["annotation_status"] == "todo":
            continue
        if sentence["annotation_status"] == "in_progress":
            continue
        elif sentence["annotation_status"] == "done":
            for annotation in sentence["annotations"]:
                annotator_freq.update([annotation["annotator"]])
    print("\tNumber of annotators:", len(annotator_freq.items()))
    num_sentences_dist = Counter()
    for annotator, freq in annotator_freq.most_common():
        num_sentences_dist.update([freq])
    num_sentences_values, num_sentences_freq = [], []
    for num_sentences, freq in sorted(num_sentences_dist.items(), key=lambda item: item[0]):
        num_sentences_values += [num_sentences]
        num_sentences_freq += [freq]
    plt.style.use('grayscale')
    plt.bar(num_sentences_values, num_sentences_freq, color='#555555')
    plt.xlabel("Number of ratings per rater")
    plt.ylabel("Number of raters")
    plt.title("Distribution of raters over number of ratings provided")
    plt.savefig(os.path.join(config['image_dir'], "impact_ratings_distribution.eps"))
    plt.clf()


def plot_agreement_model_bubble(impact_scale: str, model_agreement: Dict[str, Counter],
                                ira_filter: str) -> None:
    x, y, s = [], [], []
    for rater_score in range(0, 5):
        for model_score in range(0, 2):
            num_sentences = 0
            score_pair = (rater_score, model_score)
            if score_pair in model_agreement[impact_scale]:
                num_sentences = model_agreement[impact_scale][score_pair]
            x += [rater_score]
            y += [model_score]
            s += [num_sentences]
    plt.style.use('grayscale')
    plt.scatter(x, y, s=s, c="green", alpha=0.4, linewidth=6)
    # Add titles (main and on axis)
    plt.xlabel("Rater score")
    plt.ylabel("Model score")
    title = f"{impact_scale}, {ira_filter}"
    plot_file = os.path.join(config['image_dir'], f"plot_agreement_model-{impact_scale}-IRA-{ira_filter}.eps")
    plot_file = plot_file.replace(" >= ", "-above-").replace(" < ", "-below-")
    plt.title(title, loc="left")
    plt.savefig(plot_file)
    plt.clf()


# function for setting the colors of the box plots pairs
def setBoxColors(bp, color1, color2):
    plt.setp(bp['boxes'][0], color=color1)
    plt.setp(bp['caps'][0], color=color1)
    plt.setp(bp['caps'][1], color=color1)
    plt.setp(bp['whiskers'][0], color=color1)
    plt.setp(bp['whiskers'][1], color=color1)
    if 'fliers' in bp:
        try:
            plt.setp(bp['fliers'][0], color=color1)
            plt.setp(bp['fliers'][1], color=color1)
        except IndexError:
            pass
    plt.setp(bp['medians'][0], color=color1)

    plt.setp(bp['boxes'][1], color=color2)
    plt.setp(bp['caps'][2], color=color2)
    plt.setp(bp['caps'][3], color=color2)
    plt.setp(bp['whiskers'][2], color=color2)
    plt.setp(bp['whiskers'][3], color=color2)
    if 'fliers' in bp:
        try:
            plt.setp(bp['fliers'][2], color=color2)
            plt.setp(bp['fliers'][3], color=color2)
        except IndexError:
            pass
    plt.setp(bp['medians'][1], color=color2)


def get_data_for_boxplot(sentence_ratings: list, ira_threshold: float, config: dict):
    data_to_plot = {}
    impact_scales = ["emotional_scale", "style_scale", "reflection_scale", "narrative_scale"]
    for impact_scale in impact_scales:
        sample_model_0, sample_model_1 = impact_model_analysis.sample_model_scores(sentence_ratings,
                                                                                   impact_scale,
                                                                                   ira_threshold, config)
        data_to_plot[impact_scale] = [sample_model_0, sample_model_1]
    return data_to_plot


def do_model_box_plot(sentences_done: list, ira_threshold: float, config: dict):
    data_to_plot = get_data_for_boxplot(sentences_done, ira_threshold, config)
    plt.style.use('grayscale')
    ax = plt.axes()
    scales = ["emotional_scale", "narrative_scale", "style_scale", "reflection_scale"]
    for pos, impact_scale in enumerate(scales):
        # first boxplot pair
        positions = [pos * 3 + 1, pos * 3 + 2]
        #plt.style.use('grayscale')
        bp = plt.boxplot(data_to_plot[impact_scale], positions=positions, widths=0.6)
        setBoxColors(bp, '#111111', '#AAAAAA')
    # set axes limits and labels
    plt.xlim(0, 12)
    plt.ylim(-1, 6)
    plt.ylabel('Human rating')
    ax.set_xticklabels(['Emotional', 'Narrative', 'Aesthetic', 'Reflection'])
    ax.set_xticks([1.5, 4.5, 7.5, 10.5])
    ax.set_yticks([0, 1, 2, 3, 4])
    # plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='#111111', label='Model = 0')
    plt.plot([], c='#AAAAAA', label='Model >= 1')
    plt.legend()
    plt.tight_layout()
    out_file = os.path.join(config['image_dir'], f'model-comparison-boxplot-IRA-{ira_threshold}.eps')
    print(f'\twriting box plot to file {out_file}')
    plt.savefig(out_file)
    plt.close()


def plot_rating_probability(rating_freq: Counter) -> None:
    outfile = os.path.join(config['image_dir'], 'rating_probability.eps')

    total = sum(rating_freq.values())
    observed = [freq / total for _rating, freq in sorted(rating_freq.items(), key=lambda x: x[0])]

    # data to plot
    n_groups = 5

    # create plot
    plt.style.use('grayscale')
    plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.5
    opacity = 0.8

    _ = plt.bar(index, observed, bar_width, alpha=opacity, color='#555555', label='Rating distribution')

    plt.xlabel('Rating')
    plt.ylabel('Probability')
    plt.title('Observed Rating Probability')
    plt.xticks(index, (0, 1, 2, 3, 4))
    plt.legend()

    plt.tight_layout()
    print(f'\n\twriting rating probability distribution to file {outfile}')
    plt.savefig(outfile)
    plt.close()

    outfile = os.path.join(config['image_dir'], 'rating_probability-null_distributions.eps')
    inv_tri = [0.2727, 0.1818, 0.0909, 0.1818, 0.2727]
    uniform = [0.2, 0.2, 0.2, 0.2, 0.2]

    # create plot
    plt.style.use('grayscale')
    plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25

    _ = plt.bar(index, uniform, bar_width, alpha=opacity, color='#2C7BB6', label='Uniform')

    _ = plt.bar(index + bar_width, inv_tri, bar_width, alpha=opacity, color='#D7191C', label='Inverse Triangular')

    _ = plt.bar(index + 2*bar_width, observed, bar_width, alpha=opacity, color='#19B77C', label='Rating distribution')

    plt.xlabel('Rating')
    plt.ylabel('Probability')
    plt.title('Null distributions and observed rating probability')
    plt.xticks(index + bar_width, (0, 1, 2, 3, 4))
    plt.legend()

    plt.tight_layout()
    print(f'\n\twriting rating probability distribution to file {outfile}')
    plt.savefig(outfile)
    plt.close()


def plot_per_sentence_ira_dist(ira_dist: Dict[str, Counter]) -> None:
    n_groups = 8
    plt.style.use('grayscale')
    plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.20
    opacity = 0.8

    ira_ranges = [
        '-0.70 -- -0.51',
        '-0.50 -- -0.31',
        '-0.30 -- 0.00',
        '0.00 -- +0.30',
        '+0.31 -- +0.50',
        '+0.51 -- +0.70',
        '+0.71 -- +0.90',
        '+0.91 -- +1.00'
    ]

    scale_label = {
        'emotional_scale':  'Emotional impact',
        'narrative_scale':  'Narrative feeling',
        'style_scale':      'Aesthetic feeling',
        'reflection_scale': 'Reflection'
    }

    for si, scale in enumerate(scale_label.keys()):
        scale_values = [ira_dist[scale][ira_range] for ira_range in ira_ranges]
        _ = plt.bar(index + si * bar_width, scale_values, bar_width, alpha=opacity, label=scale_label[scale])

    plt.xlabel('Per sentence IRA')
    plt.ylabel('# sentences')
    plt.title('Distribution of per sentence IRA scores')
    plt.xticks(index + 1 * bar_width, [ira_range.replace("--", "--\n") for ira_range in ira_ranges])
    plt.tick_params(axis='x', labelsize=8)
    plt.legend()

    outfile = os.path.join(config['image_dir'], 'per_sentence_ira_distribution.eps')
    plt.tight_layout()
    print(f'\n\twriting per sentence IRA score distribution to file {outfile}')
    plt.savefig(outfile)
    plt.close()


def plot_rule_coverage():
    impact_columns = ['Emotional_impact', 'Aesthetic_feeling', 'Reflection', 'Narrative_feeling', 'All']
    df = pd.read_csv(config['aggr_impact_file'], sep='\t')
    linestyles = ['-', '--', '-.', ':']
    for ci, column in enumerate(impact_columns):
        sorted_counts = sorted([(value, count) for value, count in df[column].value_counts().iteritems()])
        values, counts = zip(*sorted_counts)
        count_probs = [count / sum(counts) for count in counts]
        x_values, y_values = values, count_probs
        if ci < 4:
            linestyle = linestyles[ci]
            color = '#111111'
        else:
            linestyle = linestyles[0]
            color = '#AAAAAA'
        plt.plot(x_values, y_values, label=column, c=color, linestyle=linestyle)
    plt.legend()
    plt.xlim(0, 10)
    plt.xlabel('Number of matching rules per review')
    plt.ylabel('Fraction of reviews')
    outfile = os.path.join(config['image_dir'], 'impact_rule_coverage.eps')
    plt.savefig(outfile)
    plt.close()
