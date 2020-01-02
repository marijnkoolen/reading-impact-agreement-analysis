import tarfile
import json
import sys
from elasticsearch import Elasticsearch
from alpino_matcher import AlpinoMatcher
from collections import defaultdict
import pickle


def get_sentence_id(member):
    sent_info = member.name.split(".")[1]
    return sent_info.replace("sentence-", "")


def get_sentence_json(tar, member):
    f = tar.extractfile(member)
    content = f.read()
    return json.loads(content)


def get_tar_members(sentences_file):
    tar = tarfile.open(sentences_file, 'r:gz')
    for member in tar.getmembers():
        yield member


def read_tarred_sentences(sentences_file):
    sentence_data = {}
    tar = tarfile.open(sentences_file, 'r:gz')
    for member in tar.getmembers():
        if ".json" not in member.name:
            continue
        sentence_id = get_sentence_id(member)
        sentence_json = get_sentence_json(tar, member)
        sentence_data[sentence_id] = sentence_json
    return sentence_data


def score_sentence_impact(sentence, alpino_matcher):
    alpino_ds = json.loads(sentence["alpino_ds"])
    matches = alpino_matcher.match_rules(alpino_sentence=alpino_ds)
    impact_score = defaultdict(int)
    for match in matches:
        if match["impact_type"]:
            impact_score[match["impact_type"]] += 1
        # print(match)
    return impact_score


def map_impact(impact_score):
    return {
        "emotional_scale": impact_score["Affect"] + impact_score["Style"] + impact_score["Narrative"],
        "style_scale": impact_score["Style"],
        "reflection_scale": impact_score["Reflection"],
        "narrative_scale": impact_score["Narrative"]
    }


def load_impact_model(impact_model_file):
    with open(impact_model_file, 'rb') as fh:
        return pickle.load(fh)


def score_impact_sentences(sentence_ratings, sentence_alpino_data, config):
    impact_model = load_impact_model(config.impact_model_file)
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

