import pytest
import os
from negima import MorphemeMerger

root = os.path.abspath(os.path.dirname(__file__))
rule_path = os.path.join(root, '..', 'rules')

noun_phases = [
    "約5000人が国立競技場に駆けつけた",
    "場所がわかりにくいのでたどり着けなかった",
]

independent_phases = [
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

    for phase, correct in zip(noun_phases, corrects):
        target, posses = mm.get_rule_pattern(phase)
        assert target == correct


def test_nouns():
    mm = get_mm('2_nouns')
    corrects = [
        ['約5000人', '国立競技場'],
        ["場所"]
    ]

    for phase, correct in zip(noun_phases, corrects):
        target, posses = mm.get_rule_pattern(phase)
        assert target == correct


def test_independent_phases():
    mm = get_mm('3_independence_phase')
    corrects = [
        ['新人研修', 'レベルは高い'],
        ['サイト', 'ホテル', '比較がしやすくない', '好きではない'],
    ]
    for phase, correct in zip(independent_phases, corrects):
        target, posses = mm.get_rule_pattern(phase)
        assert target == correct
