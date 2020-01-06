from typing import Dict, List
from collections import Counter, defaultdict
import human_rater_analysis


def make_mwu_test_samples(sentence_ratings: list, ira_threshold: float) -> Dict[str, List[dict]]:
    samples = defaultdict(list)
    impact_scales = ["emotional_scale", "style_scale", "reflection_scale", "narrative_scale", "emotional_valence"]
    for sentence in sentence_ratings:
        for impact_scale in impact_scales:
            scores = human_rater_analysis.get_rater_scores(sentence, impact_scale)
            # skip sentences with only a single rating (and the rest NAs) or with only NAs
            if len(scores) < 2:
                continue
            ira_score = human_rater_analysis.calculcate_inter_rater_agreement(scores)
            # skip sentences where the IRA is below a given threshold
            if ira_score < ira_threshold:
                continue
            model_score = sentence["model_impact_score"][impact_scale]
            if model_score > 1:
                model_score = 1
            rater_score = human_rater_analysis.calculate_avg_rater_score(impact_scale, sentence, avg_type="median")
            samples[impact_scale] += [{"impact_model": model_score, "human_rater": float(rater_score)}]
    return samples


def rank_samples(samples):
    sorted_samples = sorted(samples, key=lambda x: x["human_rater"], reverse=True)
    for item_index, item in enumerate(sorted_samples):
        item_rank = item_index + 1
        item["rank"] = item_rank
    avg_rank = get_avg_rank_samples(samples)
    for item in sorted_samples:
        item["avg_rank"] = avg_rank[item["human_rater"]]
    return sorted_samples


def get_avg_rank_samples(samples):
    rater_values = set([item["human_rater"] for item in samples])
    avg_rank = {}
    for rater_value in rater_values:
        sum_rank = sum([item["rank"] for item in samples if item["human_rater"] == rater_value])
        num_rank = len([item["rank"] for item in samples if item["human_rater"] == rater_value])
        avg_rank[rater_value] = sum_rank / num_rank
    return avg_rank


def test_samples(samples):
    ranked_samples = rank_samples(samples)
    R_model_0 = sum([item["avg_rank"] for item in ranked_samples if item["impact_model"] == 0])
    R_model_1 = sum([item["avg_rank"] for item in ranked_samples if item["impact_model"] == 1])
    N_model_0 = len([item for item in ranked_samples if item["impact_model"] == 0])
    N_model_1 = len([item for item in ranked_samples if item["impact_model"] == 1])
    U_model_0 = R_model_0 - N_model_0 * (N_model_0 + 1) / 2
    U_model_1 = R_model_1 - N_model_1 * (N_model_1 + 1) / 2
    print("R model X = 0:", R_model_0, "\tR model X > 0:", R_model_1)
    print("N model X = 0:", N_model_0, "\tN model X > 0:", N_model_1)
    print("U model X = 0:", U_model_0, "\tU model X > 0:", U_model_1)
    print()


