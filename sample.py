from negima import MorphemeMerger
mm = MorphemeMerger()
# csv
mm.set_rule_from_csv('rules/1_noun.csv')
# tsv
# mm.set_rule_from_csv('rules/1_noun.tsv', sep='\t')
# # excel
# mm.set_rule_from_excel('rules/rules.xlsx', sheet_name='1_noun')

words, _ = mm.get_rule_pattern('今日はいい天気')
print(words)