from collections import Counter
import impact_model_analysis
import human_rater_analysis
import config
import matplotlib.pyplot as plt
import seaborn as sns


def plot_agreement_model_bubble(impact_scale: str, model_agreement: Counter, ira_filter: str) -> None:
    x, y, s = [], [], []
    for rater_score in range(0, 5):
        for model_score in range(0, 2):
            num_sentences = 0
            score_pair = (rater_score, model_score)
            if score_pair in model_agreement:
                num_sentences = model_agreement[score_pair]
            x += [rater_score]
            y += [model_score]
            s += [num_sentences]
    plt.scatter(x, y, s=s, c="green", alpha=0.4, linewidth=6)
    # Add titles (main and on axis)
    plt.xlabel("Rater score")
    plt.ylabel("Model score")
    title = f"{impact_scale}, {ira_filter}"
    plot_file = f"plot_agreement_model-{impact_scale}-IRA-{ira_filter}.png"
    plot_file = plot_file.replace(" >= ", "-above-").replace(" < ", "-below-")
    plt.title(title, loc="left")
    plt.savefig(plot_file)
    plt.clf()


def plot_num_annotations_distribution(sentence_ratings: list) -> None:
    annotator_freq = Counter()
    for sentence in sentence_ratings:
        if sentence["annotation_status"] == "todo":
            continue
        if sentence["annotation_status"] == "in_progress":
            continue
        elif sentence["annotation_status"] == "done":
            #if len(sentence["annotations"]) != 3:
            #    print(sentence["sentence_id"], len(sentence["annotations"]))
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
    plt.savefig("impact_ratings_distribution.png")
    plt.clf()


def get_model_agreement(sentences: list, impact_scale: str) -> Counter:
    model_agreement = Counter()
    for sentence in sentences:
        model_score = sentence["model_impact_score"][impact_scale]
        if model_score > 0:
            model_score = 1
        rater_scores = human_rater_analysis.get_rater_scores(sentence, impact_scale)
        for rater_score in rater_scores:
            model_agreement.update([(rater_score, model_score)])
    return model_agreement


def do_model_agreement_analysis(sentence_ratings: list, ira_threshold: float):
    for impact_scale in config.impact_scales:
        sentences_high_ira = human_rater_analysis.get_sentences_high_ira(sentence_ratings, impact_scale, ira_threshold)
        sentences_low_ira = human_rater_analysis.get_sentences_low_ira(sentence_ratings, impact_scale, ira_threshold)
        model_agreement_high_ira = get_model_agreement(sentences_high_ira, impact_scale)
        model_agreement_low_ira = get_model_agreement(sentences_low_ira, impact_scale)
        print("  Total sentences:",len(sentence_ratings),
              f"\tIRA >= ({ira_threshold}):", len(sentences_high_ira),
              f"\tIRA < ({ira_threshold}):", len(sentences_low_ira),
              f"\tIgnored (1 or 0 non-NA ratings):", len(sentence_ratings) - len(sentences_high_ira) - len(sentences_low_ira))
        plot_agreement_model_bubble(impact_scale, model_agreement_high_ira, f"IRA >= {ira_threshold}")
        plot_agreement_model_bubble(impact_scale, model_agreement_low_ira, f"IRA < {ira_threshold}")


def do_analysis():
    print("Reading human ratings")
    sentence_ratings = human_rater_analysis.get_sentence_ratings(config.ratings_file)
    print("Plotting rating distribution")
    plot_num_annotations_distribution(sentence_ratings)
    print("Filtering sentences with at least 3 raters")
    sentences_done = [sentence for sentence in sentence_ratings if sentence["annotation_status"] == "done"]
    print("Reading alpino parses of sentences")
    sentence_alpino_data = impact_model_analysis.read_tarred_sentences(config.alpino_sentences_file)
    print("Scoring sentences on reading impact")
    impact_model_analysis.score_impact_sentences(sentences_done, sentence_alpino_data, config)
    print("Writing human and model ratings to spreadsheet")
    human_rater_analysis.write_rating_spreadsheet(sentences_done)
    print("Plotting human model rating agreement")
    do_model_agreement_analysis(sentences_done, ira_threshold=0.5)


if __name__ == "__main__":
    do_analysis()