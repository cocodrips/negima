import MeCab


class Morpheme:
    def __init__(self, word, poss, base, yomi):
        """
        :param word: 元の単語
        :param poss: 
        :param base: 単語の原型 
        :param yomi: 単語の読み
        """
        self.word = word
        self.poss = poss
        self.base = base
        self.yomi = yomi

        if self.base == '*':
            self.base = self.word

    def __hash__(self):
        return hash(self.base + self.poss[0])

    def __eq__(self, other):
        return (self.word == other.word
                and self.poss[0] == other.poss[0]
                and self.base == other.base)

    def __repr__(self):
        return "{}({}:{})".format(
            self.word, self.base, ','.join(self.poss))


class Parser:
    def __init__(self, mecab_args=''):
        self.mecab = MeCab.Tagger(mecab_args)

    def parse(self, text):
        '''テキストを単語ごとにMorphemeオブジェクトにして返す

        :param str text
        :rtype: list[Morpheme]
        '''
        m = self.mecab.parse(text)
        tokens = []
        for mecab_token in m.split('\n'):
            token = self.get_token(mecab_token)
            if token:
                tokens.append(token)
        return tokens

    def get_token(self, mecab_token):
        """
        MeCabの出力結果をMorphemeオブジェクトに
        :rtype Morpheme
        """
        splited = mecab_token.split('\t')
        if len(splited) < 2:
            return None

        word, info = splited
        infomations = info.split(',')
        poss = infomations[0:5]
        word_base = infomations[6]
        yomi = word if len(infomations) < 8 else infomations[7]
        return Morpheme(word, poss, word_base, yomi)
