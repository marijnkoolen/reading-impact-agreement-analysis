from typing import Dict
from collections import Counter
import matplotlib.pyplot as plt
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
    plt.bar(num_sentences_values, num_sentences_freq)
    plt.xlabel("Number of ratings per rater")
    plt.ylabel("Number of raters")
    plt.title("Distribution of raters over number of ratings provided")
    plt.savefig(os.path.join(config['image_dir'], "impact_ratings_distribution.png"))
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
    plt.scatter(x, y, s=s, c="green", alpha=0.4, linewidth=6)
    # Add titles (main and on axis)
    plt.xlabel("Rater score")
    plt.ylabel("Model score")
    title = f"{impact_scale}, {ira_filter}"
    plot_file = os.path.join(config['image_dir'], f"plot_agreement_model-{impact_scale}-IRA-{ira_filter}.png")
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


def get_data_for_boxplot(sentence_ratings: list, ira_threshold: float):
    data_to_plot = {}
    impact_scales = ["emotional_scale", "style_scale", "reflection_scale", "narrative_scale"]
    for impact_scale in impact_scales:
        sample_model_0, sample_model_1 = impact_model_analysis.sample_model_scores(sentence_ratings,
                                                                                   impact_scale, ira_threshold)
        data_to_plot[impact_scale] = [sample_model_0, sample_model_1]
    return data_to_plot


def do_model_box_plot(sentences_done: list, ira_threshold=0.5):
    data_to_plot = get_data_for_boxplot(sentences_done, ira_threshold=ira_threshold)
    #fig = figure()
    ax = plt.axes()
    scales = ["emotional_scale", "narrative_scale", "style_scale", "reflection_scale"]
    for pos, impact_scale in enumerate(scales):
        # first boxplot pair
        positions = [pos * 3 + 1, pos * 3 + 2]
        bp = plt.boxplot(data_to_plot[impact_scale], positions=positions, widths=0.6)
        setBoxColors(bp, '#D7191C', '#2C7BB6')
    # set axes limits and labels
    plt.xlim(0, 12)
    plt.ylim(-1, 6)
    ax.set_xticklabels(['Emotional', 'Narrative', 'Aesthetic', 'Reflection'])
    ax.set_xticks([1.5, 4.5, 7.5, 10.5])
    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='#D7191C', label='Model = 0')
    plt.plot([], c='#2C7BB6', label='Model >= 1')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(config['image_dir'], f'model-comparison-boxplot-IRA-{ira_threshold}.png'))
    return None

