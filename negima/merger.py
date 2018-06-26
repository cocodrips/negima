# -*- coding: utf-8 -*-
import enum
import pandas as pd
import copy

from . import Parser
from .rule import Rule


class NormType(enum.Enum):
    RAW = 0
    NORM = 1
    BASE = 2


class Path:
    def __init__(self, word, base, rule):
        self.word = word
        self.base = base
        self.rule = rule


class MorphemeMerger:
    def __init__(self, mecab_args=''):
        self.rule = None
        self.mecab_args = mecab_args

    def get_rule_pattern(self, text, norm=NormType.NORM,
                         skip=True):
        """
        :param str          text: Target text 
        :param NormType     norm: 
        :return: (word, posses)
        """
        parser = Parser(mecab_args=self.mecab_args)
        morphemes = parser.parse(text)

        i = 0
        words = []
        posses = []
        n = len(morphemes)
        while i < n:
            paths, _i = self._rec_tree_check(morphemes, i, norm=norm)
            if paths is not None:
                if skip:
                    i = _i
                else:
                    i += 1

                words.append(''.join([path.word for path in paths]))
                posses.append([path.rule.poss for path in paths])
            else:
                i += 1

        return words, posses

    def _default_noun_rule(self):
        root = {}
        rule = Rule(['名詞', 'nan', 'nan', 'nan', 'nan'])
        root[rule] = {rule: {rule: {None: None}}}
        return root

    def set_rule_from_csv(self, rule_file_path, sep=','):
        """Create rule tree from csv file.
        
        :param rule_file_path: Rule file path
        :param str sep: default=','
        :return: None
        """
        rules = pd.read_csv(rule_file_path, sep=sep)
        self._set_rule_tree(rules)

    def set_rule_from_excel(self, rule_file_path, sheet_name):
        """Create rule tree from excel file.
        
        :param str rule_file_path: Rule file path
        :param str sheet_name: Default is 0 (means read first sheet) 
        :return: None 
        """
        rules = pd.read_excel(rule_file_path,
                              sheet_name=sheet_name)
        self._set_rule_tree(rules)

    def _set_rule_tree(self, rules):
        """Create rule tree.
        
        :param pandas.DataFrame rules: DataFrame object from rule file.
        :return: None
        """
        poss_keys = ['pos0', 'pos1', 'pos2', 'pos3', 'pos4']

        # Set default value
        rules['min'] = pd.to_numeric(rules['min']).fillna(1)
        rules['max'] = pd.to_numeric(rules['max']).fillna(1)
        rules[poss_keys] = rules[poss_keys].astype(str)
        rules['id'] = rules['id'].astype(str)

        # Create tree
        root = dict()
        prev_branches = [root]

        prev_id = None
        _id = None
        for i, rule in rules.iterrows():
            word = rule['id']
            if word != 'nan':
                prev_id = _id
                _id = word
            repeat_min = int(rule['min'])
            repeat_max = int(rule['max'])
            poss = rule[poss_keys]

            r = Rule(list(poss.values))
            current_branches = []

            # ルールの区切り列の処理
            if word != 'nan':
                for prev_branch in prev_branches:
                    # 木の構成が終了するならNoneを入れておく
                    if prev_branch is not root:
                        prev_branch[None] = prev_id
                prev_branches = [root]

            for prev_branch in prev_branches:
                branch = prev_branch
                for i in range(0, repeat_max + 1):
                    if i == 0:
                        if repeat_min == 0:
                            current_branches.append(branch)
                        continue

                    if r not in branch:
                        # 現在のブランチにnodeがなければ追加
                        branch[r] = dict()
                    branch = branch[r]
                    if i >= repeat_min:
                        current_branches.append(branch)
            prev_branches = current_branches

        # 最後の行だった場合、最後にNoneをkeyにいれておく
        for prev_branch in prev_branches:
            if prev_branch is not root:
                prev_branch[None] = _id
        self.rule = root

    def _rec_tree_check(self, morphemes, index, norm=NormType.NORM):
        """
        :param [Token]  tokens 
        :param int      index: tokensの 
        :param NormType norm 
        
        :return: (取り出されたフェーズ, 
                  フェーズに適用されたRuleのリスト, 
                  どこのindexまで進んだか)
        """
        paths, i, _ = self._rec_check(self.rule, morphemes[index:], index, [])

        if paths is not None:
            if norm == NormType.NORM:
                if paths[-1].base != '*':
                    paths[-1].word = paths[-1].base
            if norm == NormType.BASE:
                for path in paths:
                    if path.base != '*':
                        path.word = path.base

        return (paths, i)

    def _rec_check(self, rules, morphemes, i, paths):
        '''
        :param rules: 
        :param morphemes: 
        :param paths: 
        :rtype: [Path], index, priority
        '''
        '''最後の文字の場合'''
        if not morphemes:
            # Match rule
            if None in rules:
                return paths, i, rules[None]

            # No match
            return None, None, None

        '''最後の文字ではない場合'''
        best_result = None
        best_score = None
        best_i = 0
        for rule, branch in rules.items():
            if rule is None:
                if best_result is None or branch < best_score:
                    best_score = branch
                    best_result = paths
                    best_i = i
                continue

            if rule.is_match(morphemes[0]):
                path = Path(morphemes[0].word, morphemes[0].base, rule)
                _paths = copy.deepcopy(paths)
                _paths.append(path)

                # if rule.poss is None:
                #     return _paths
                result, _i, priority = self._rec_check(branch, morphemes[1:],
                                                       i + 1, _paths)
                if result is not None:
                    if best_result is None or priority < best_score:
                        best_score = priority
                        best_result = result
                        best_i = _i

        if best_result is not None:
            return best_result, best_i, best_score

        '''最後までマッチ失敗'''
        return None, None, None
