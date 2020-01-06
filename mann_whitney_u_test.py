from typing import Dict, List
from collections import Counter, defaultdict
import human_rater_analysis


def make_mwu_test_samples(sentence_ratings: list, ira_threshold: float) -> Dict[str, List[dict]]:
    impact_scales = ["emotional_scale", "style_scale", "reflection_scale", "narrative_scale", "emotional_valence"]
    samples = defaultdict(list)
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


def rank_samples(sample_model_0, sample_model_1):
    sample_0 = [{"model": 0, "score": score} for score in sample_model_0]
    sample_1 = [{"model": 1, "score": score} for score in sample_model_1]
    samples = sample_0 + sample_1
    sorted_samples = sorted(samples, key=lambda x: x["score"], reverse=True)
    for item_index, item in enumerate(sorted_samples):
        item_rank = item_index + 1
        item["rank"] = item_rank
    avg_rank = get_avg_rank_samples(samples)
    for item in sorted_samples:
        item["avg_rank"] = avg_rank[item["score"]]
    return sorted_samples


def get_avg_rank_samples(samples):
    rater_values = set([item["score"] for item in samples])
    avg_rank = {}
    for rater_value in rater_values:
        sum_rank = sum([item["rank"] for item in samples if item["score"] == rater_value])
        num_rank = len([item["rank"] for item in samples if item["score"] == rater_value])
        avg_rank[rater_value] = sum_rank / num_rank
    return avg_rank


def test_samples(sample_model_0: List[float], sample_model_1: List[float]):
    ranked_samples = rank_samples(sample_model_0, sample_model_1)
    R_model_0 = sum([item["avg_rank"] for item in ranked_samples if item["model"] == 0])
    R_model_1 = sum([item["avg_rank"] for item in ranked_samples if item["model"] == 1])
    N_model_0 = len([item for item in ranked_samples if item["model"] == 0])
    N_model_1 = len([item for item in ranked_samples if item["model"] == 1])
    U_model_0 = R_model_0 - N_model_0 * (N_model_0 + 1) / 2
    U_model_1 = R_model_1 - N_model_1 * (N_model_1 + 1) / 2
    test_0 = {
        "model": 0,
        "N": N_model_0,
        "R": R_model_0,
        "U": U_model_0
    }
    test_1 = {
        "model": 1,
        "N": N_model_1,
        "R": R_model_1,
        "U": U_model_1
    }
    return test_0, test_1


