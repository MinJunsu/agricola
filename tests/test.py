import json

from deepdiff import DeepDiff


def test():
    test1 = json.load(open('./tests/test1.json', 'r'))
    test2 = json.load(open('./tests/test2.json', 'r'))

    d = DeepDiff(test1, test2, ignore_order=False)
    print(list(d['values_changed'].items()))


if __name__ == '__main__':
    test()
