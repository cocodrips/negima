from negima import Parser


def test_parse_test():
    text = '今日は職場についた時点で満点。'
    parser = Parser()
    target = parser.parse(text)

    assert len(target) == 10
    assert target[4].base == 'つく'
    assert target[4].poss == ['動詞', '自立', '*', '*', '五段・カ行イ音便']
