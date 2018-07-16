Negima
======


Installing
----------

Install and update using `setup.py`:

.. code-block:: text

    $ python setup.py install


Dependencies
--------------
- `mecab`: http://taku910.github.io/mecab/


A Simple Example
----------------

hello.py

.. code-block:: python

    from negima import MorphemeMerger
    mm = MorphemeMerger()
    mm.set_rule_from_csv('rules/1_noun.csv')
    
    words, posses = mm.get_rule_pattern('今日はいい天気')
    print (words)


.. code-block:: text

    $ python hello.py
      ['今日', '天気']


Rule samples
-------------


`rule/1_noun.csv`

`rule/2_nouns.csv`

`rule/3_independence_phase.csv`



test
------
.. code-block:: text

    $ pytest
