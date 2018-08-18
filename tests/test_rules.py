import pytest
import os
from negima import MorphemeMerger

root = os.path.abspath(os.path.dirname(__file__))
rule_path = os.path.join(root, '..', 'rules')

noun_phrases = [
    "約5000人が国立競技場に駆けつけた",
    "場所がわかりにくいのでたどり着けなかった",
]

independent_phrases = [
    "新人研修のレベルは高い",
    "あのサイトはホテルの比較がしやすくないので好きではない",
]


def get_mm(rule_name):
    filepath = os.path.join(rule_path, rule_name + '.csv')
    mm = MorphemeMerger()
    mm.set_rule_from_csv(filepath)
    return mm


def test_noun():
    mm = get_mm('1_noun')
    corrects = [
        ["5000", "人", "国立", "競技", "場"],
        ["場所"]
    ]

    for phrase, correct in zip(noun_phrases, corrects):
        target, poss = mm.get_rule_pattern(phrase)
        assert target == correct


def test_nouns():
    mm = get_mm('2_nouns')
    corrects = [
        ['約5000人', '国立競技場'],
        ["場所"]
    ]

    for phrase, correct in zip(noun_phrases, corrects):
        target, poss = mm.get_rule_pattern(phrase)
        assert target == correct


def test_independent_phrases():
    mm = get_mm('3_independent_phrase')
    corrects = [
        ['新人研修', 'レベルは高い'],
        ['サイト', 'ホテル', '比較がしやすくない', '好きではない'],
    ]
    for phrase, correct in zip(independent_phrases, corrects):
        target, poss = mm.get_rule_pattern(phrase)
        assert target == correct
