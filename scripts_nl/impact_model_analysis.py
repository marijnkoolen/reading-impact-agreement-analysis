from typing import Dict, List, Tuple
from collections import defaultdict
import os
import tarfile
import json
import pickle
from collections import Counter
import csv

from alpino_matcher import AlpinoMatcher
import human_rater_analysis


def get_sentence_id(member) -> str:
    sent_info = member.name.split(".")[1]
    return sent_info.replace("sentence-", "")


def get_sentence_json(tar, member) -> dict:
    f = tar.extractfile(member)
    content = f.read()
    return json.loads(content)


def get_tar_members(sentences_file: str) -> iter:
    tar = tarfile.open(sentences_file, 'r:gz')
    for member in tar.getmembers():
        yield member


def read_tarred_sentences(sentences_file: str) -> dict:
    sentence_data = {}
    tar = tarfile.open(sentences_file, 'r:gz')
    for member in tar.getmembers():
        if ".json" not in member.name:
            continue
        sentence_id = get_sentence_id(member)
        sentence_json = get_sentence_json(tar, member)
        sentence_data[sentence_id] = sentence_json
    return sentence_data


def score_sentence_impact(sentence: dict, alpino_matcher: AlpinoMatcher) -> Dict[str, int]:
    alpino_ds = json.loads(sentence["alpino_ds"])
    matches = alpino_matcher.match_rules(alpino_sentence=alpino_ds)
    impact_score = defaultdict(int)
    for match in matches:
        if match["impact_type"]:
            impact_score[match["impact_type"]] += 1
        # print(match)
    return impact_score


def map_impact(impact_score: dict) -> Dict[str, int]:
    return {
        "emotional_scale": impact_score["Affect"] + impact_score["Style"] + impact_score["Narrative"],
        "style_scale": impact_score["Style"],
        "reflection_scale": impact_score["Reflection"],
        "narrative_scale": impact_score["Narrative"]
    }


def load_impact_model(impact_model_file: str) -> dict:
    with open(impact_model_file, 'rb') as fh:
        return pickle.load(fh)


def score_impact_sentences(sentence_ratings: List[dict], sentence_alpino_data: dict, config) -> None:
    impact_model = load_impact_model(config['impact_model_file'])
    alpino_matcher = AlpinoMatcher(impact_model)
    #print("Number of sentences:", len(sentence_ratings))
    for sentence in sentence_ratings:
        sentence_id = sentence["sentence_id"]
        #print(sentence_id)
        impact_score = score_sentence_impact(sentence_alpino_data[sentence_id], alpino_matcher)
        sentence["model_impact_score"] = map_impact(impact_score)
        #print(impact_score)
        #print(sentence["model_impact_score"])
        # break


def sample_model_scores(sentence_ratings: list, impact_scale: str,
                        ira_threshold: float, config: dict) -> Tuple[List[float], List[float]]:
    sample_0 = []
    sample_1 = []
    for sentence in sentence_ratings:
        scores = human_rater_analysis.get_rater_scores(sentence, impact_scale)
        # skip sentences with only a single rating (and the rest NAs) or with only NAs
        if len(scores) < 2:
            continue
        ira_score = human_rater_analysis.calculate_sentence_interrater_agreement(scores, config['null_dist'])
        # skip sentences where the IRA is below a given threshold
        if ira_score < ira_threshold:
            continue
        model_score = sentence["model_impact_score"][impact_scale]
        rater_score = human_rater_analysis.calculate_avg_rater_score(impact_scale, sentence, avg_type="median")
        if model_score >= 1:
            sample_1 += [float(rater_score)]
        else:
            sample_0 += [float(rater_score)]
    return sample_0, sample_1


def get_model_agreement(sentences: list, impact_scale: str) -> Counter:
    model_agreement = Counter()
    for sentence in sentences:
        model_score = sentence["model_impact_score"][impact_scale]
        if model_score > 0:
            model_score = 1
        rater_score = human_rater_analysis.calculate_avg_rater_score(impact_scale, sentence, avg_type="median")
        model_agreement.update([(rater_score, model_score)])
    return model_agreement


def write_model_agreement_table(agreement_high: Dict[str, Counter], agreement_low: Dict[str, Counter],
                                ira_threshold: float, config: dict):
    output_file = os.path.join(config['data_dir'], f'model_agreement.IRA_treshold-{ira_threshold}.csv')
    with open(output_file, 'wt') as fh:
        csv_writer = csv.writer(fh, delimiter="\t")
        for impact_scale in config['impact_scales']:
            headers = ["", "model"] + [str(hr / 2) for hr in range(0, 9)] + ["total"]
            csv_writer.writerow([f"IRA >= {ira_threshold}", impact_scale, "human rating"])
            csv_writer.writerow(headers)
            for model_rating in [0, 1]:
                counts = []
                for human_rating in range(0, 9):
                    human_rating = human_rating / 2
                    counts += [agreement_high[impact_scale][(human_rating, model_rating)]]
                total_counts = sum(counts)
                percentages = [round(count/total_counts, 2) for count in counts]
                count_str = [f"{count} ({percentages[ci]})" for ci, count in enumerate(counts)]
                csv_writer.writerow(["", model_rating] + count_str + [total_counts])
            csv_writer.writerow([f"IRA < {ira_threshold}", impact_scale, "human rating"])
            csv_writer.writerow(headers)
            for model_rating in [0, 1]:
                counts = []
                for human_rating in range(0, 9):
                    human_rating = human_rating / 2
                    counts += [agreement_low[impact_scale][(human_rating, model_rating)]]
                total_counts = sum(counts)
                percentages = [round(count/total_counts, 2) for count in counts]
                count_str = [f"{count} ({percentages[ci]})" for ci, count in enumerate(counts)]
            csv_writer.writerow(["", model_rating] + count_str + [total_counts])

