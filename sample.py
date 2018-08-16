from negima import MorphemeMerger
mm = MorphemeMerger()
mm.set_rule_from_csv('rules/1_noun.csv')

words, posses = mm.get_rule_pattern('今日はいい天気')
print(words)

