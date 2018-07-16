import pytest
import os
from negima import MorphemeMerger

root = os.path.abspath(os.path.dirname(__file__))


def morpheme_merger():
    """
    :rtype: MorphemeMergercd 
    """
    filepath = os.path.join(root, 'test_rules.xlsx')
    _mm = MorphemeMerger()
    _mm.set_rule_from_excel(filepath, 'test')
    return _mm


def test_set_rule_tree_from_excel():
    filepath = os.path.join(root, 'test_rules.xlsx')
    mm = MorphemeMerger()
    mm.set_rule_from_excel(filepath, 'test')
    print(mm.rule.keys())
    assert len(mm.rule.keys()) == 5


def test_set_rule_tree_from_csv():
    filepath = os.path.join(root, 'test_rules.tsv')
    mm = MorphemeMerger()
    mm.set_rule_from_csv(filepath, sep='\t')
    assert len(mm.rule.keys()) == 6


def test_get_rule_pattern():
    mm = morpheme_merger()
    words, posses = mm.get_rule_pattern('今日は職場についた時点で満点')
    print(words, posses)
    assert len(words) == 4
    assert words[0] == '今日は'
    assert words[1] == '職場'
    assert posses[0] == [['名詞', '副詞可能', 'nan', 'nan', 'nan'],
                         ['助詞', '係助詞', 'nan', 'nan', 'nan']]


@pytest.mark.parametrize("src, dest", [
    ('唖然と', ['唖然と']),
    ('申し訳ないです', ['申し訳ない']),
    ('見る影もない', ['見る影もない']),
    ('扱うことはできる', ['扱うことはできる']),
    ('ご飯とはなんですか', ['ご飯'])
])
def test_duplicate_rule_pattern(src, dest):
    mm = morpheme_merger()
    target, posses = mm.get_rule_pattern(src)
    print(target, posses)
    assert target == dest
