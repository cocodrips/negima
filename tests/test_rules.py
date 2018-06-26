# import pytest
# import os
# from negima import MorphemeMerger
# 
# root = os.path.abspath(os.path.dirname(__file__))
# 
# phases = [
#     
# ]
# 
# def test_noun(src, dest):
#     """
#     :rtype: MorphemeMerger 
#     """
#     filepath = os.path.join(root, '1_noun.xlsx')
#     mm = MorphemeMerger()
#     mm.set_rule_from_excel(filepath, 'test')
#     return mm
# 
# @pytest.mark.parametrize("src, dest", [
#     ('唖然と', ['唖然と']),
#     ('申し訳ないです', ['申し訳ない']),
#     ('見る影もない', ['見る影もない']),
#     ('扱うことはできる', ['扱うことはできる']),
#     ('ご飯とはなんですか', ['ご飯'])
# ])
# def test_duplicate_rule_pattern(src, dest):
#     mm = morpheme_merger()
#     target, posses = mm.get_rule_pattern(src)
#     print(target, posses)
#     assert target == dest
