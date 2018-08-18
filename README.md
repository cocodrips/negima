# Negima

Negima is a Python package to extract phases in Japanese text using rules.

*Negimaは日本語の文章の中から定義したルールにあてはまるフェーズを抽出するPythonパッケージです。*


## Installing

Install and update using pip:

```bash
$ pip install -U negima
```

Install using `setup.py`:

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
# csv
mm.set_rule_from_csv('rules/1_noun.csv')
# tsv
# mm.set_rule_from_csv('rules/1_noun.tsv', sep='\t')
# # excel
# mm.set_rule_from_excel('rules/rules.xlsx', sheet_name='1_noun')

words, posses = mm.get_rule_pattern('今日はいい天気')
print(words)
```

```bash
$ python sample.py
  ['今日', '天気']
```

## Rule

You can define　rules in a csv, tsv or excel format.  
A rule file requires following 9 columns.

*ルールはcsv, tsv, excelファイルの形式で定義することができます。  
ルールには以下の9種のカラムが必要になります。*  


- id
    - A rule starts with non-empty id column.  
        *idが空でなければ、ルールのスタートを示す*
    - id has to be unique.  
        *idはユニークである必要がある*
    - Rules are applied in ascendings order of id (ids are compared as UTF-8 strings, not as byte arrays).  
      ex: id:000_XXX has priority over id:999_ZZZ  
        *idは文字列としてsortされて小さい順にそのルールの優先度が定義される    
        例: id:000_XXXのルールはid:999_ZZZのルールよりも優先度が高い*
- min
    - Minimum repeat number. 0 means that morpheme is optional.  
        *形態素の最小繰り返し回数。0に設定するとそのパーツはあってもなくても良い*
    - default=1
- max
    - Maximum repeat number  
        *形態素の最大繰り返し回数*
    - default=1
- pos0, pos1, pos2, pos3, pos4, pos5
    - Part of speeches of morphemes parsed by mecab.  
        *mecabでparseされた形態素の品詞や活用の名前*
        - pos0: 表層  (ex: 名詞)
        - pos1: 品詞1 (ex: 副詞可能)
        - pos2: 品詞2
        - pos3: 品詞3
        - pos4: 活用1
        - pos5: 活用2
    - To represent OR condition, concatenate part-of-speeches with `|` as a separator.  
        `|`で品詞を接続することでOR条件の定義が可能である


You can add arbitrary columns to your rule file. other columns are just ignored.
An example is available at `rule/3_independence_phase.csv`, which has a row example that describes an example sentence for the rule.

*上記以外にも任意の列の追加が可能です。  
`rule/3_independence_phase.csv`では`example`という列を追加し、ルールにあてはまるサンプルを記述しています。*



### Simple rule (csv)

A rule to extract compound noun.
*このようなルールを定義することで、複合名詞を抽出できます*

|id|min|max|pos0|pos1|pos2|pos3|pos4|pos5|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|1|0|2|接頭詞|||||
| |1|4|名詞|一般&#124;サ変接続&#124;数||||
| |0|2|名詞|接尾||||


**Caution**
*Don't insert empty row between rules.*


**注意**
*ルール同士の間に空行をはさまないようにすること*

### Rule samples

#### rule/1_noun.csv
Extract nouns.  
*名詞の抽出*  

- `約5000人が国立競技場に駆けつけた` -> `5000` `人` `国立` `競技` `場`
- `場所がわかりにくいのでたどり着けなかった` -> `場所`

#### rule/2_nouns.csv
Extract compound nouns.  
*複合名詞の抽出* 

- `約5000人が国立競技場に駆けつけた` -> `約5000人` `国立競技場` 
- `場所がわかりにくいのでたどり着けなかった` -> `場所`


#### rule/3_independent_phase.csv
Extract a little complex phase.   
*形容詞や否定の「ない」を含んだ少し複雑なルールのフェーズの抽出*  

- `新人研修のレベルは高い` -> `新人研修` `レベルは高い`
- `あのサイトはホテルの比較がしやすくないので好きではない` -> `サイト` `ホテル` `比較がしやすくない` `好きではない`



