# Negima
Extract phases in Japanese text using rules.

## Installing


Install and update using `setup.py`:

```bash
$ python setup.py install
```




## Dependencies

- `mecab`: http://taku910.github.io/mecab/


## A Simple Example


sample.py

```python
from negima import MorphemeMerger
mm = MorphemeMerger()
mm.set_rule_from_csv('rules/1_noun.csv')

words, posses = mm.get_rule_pattern('今日はいい天気')
print(words)
```

```bash
$ python sample.py
  ['今日', '天気']
```

## Rule samples



### rule/1_noun.csv
Extract nouns.

- `約5000人が国立競技場に駆けつけた` -> `5000` `人` `国立` `競技` `場`
- `場所がわかりにくいのでたどり着けなかった` -> `場所`

### rule/2_nouns.csv
Extract compound nouns.

- `約5000人が国立競技場に駆けつけた` -> `約5000人` `国立競技場` 
- `場所がわかりにくいのでたどり着けなかった` -> `場所`


### rule/3_independence_phase.csv

- `新人研修のレベルは高い` -> `新人研修` `レベルは高い`
- `あのサイトはホテルの比較がしやすくないので好きではない` -> `サイト` `ホテル` `比較がしやすくない` `好きではない`



## test

```bash
$ pytest
```


