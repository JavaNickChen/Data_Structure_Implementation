import unittest
from Dictionary import Dictionary
# import Dictionary


class DictionaryTest(unittest.TestCase):

    def test_add(self):
        dictionary = Dictionary()
        self.assertEqual(dictionary.to_list(), [])
        dictionary.add("score", 89)
        self.assertEqual(dictionary.get_by_key("score"), 89)
        self.assertEqual(dictionary.to_list(), [("score", [89])])
        dictionary.add("score", 78)
        self.assertEqual(dictionary.to_list(), [("score", [89, 78])])
        dictionary.add("gender", "male")
        self.assertEqual(dictionary.to_list(), [("gender", ["male"]), ("score", [89, 78])])

        dictionary2 = Dictionary()
        temp1 = [23, 34]
        temp2 = [23, 34]
        dictionary2.add(temp1, 'test_value_1')
        dictionary2.add(temp2, 'value2')
        self.assertEqual(dictionary2.to_list(), [([23, 34], ['test_value_1', 'value2'])])

    def test_remove_by_key(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        dictionary.remove_by_key("gender")
        self.assertEqual(dictionary.to_list(), [["age", "name", "others"], [[23], ["Nick"], [10, 100]]])
        dictionary.remove_by_key("others")
        self.assertEqual(dictionary.to_list(), [["age", "name"], [[23], ["Nick"]]])

    def test_size(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        self.assertEqual(dictionary.size(), [4, 5])

    def test_to_list(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        self.assertEqual(dictionary.to_list(),
                         [("age", [23]), ("gender",["male"]), ("name", ["Nick"]), ("others", [10, 100])])

    def test_from_list(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key('gender'), 'male')
        self.assertEqual(dictionary.to_list(), [('age', 23), ('gender', 'male'), ('name', 'Nick'), ('others', [10, 100])])

    def test_get_by_key(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key("others"), [10, 100])

    def test_filter(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        result_even = dictionary.filter("even_value")
        self.assertEqual(result_even, ["others"])
        result_odd = dictionary.filter("odd_value")
        self.assertEqual(result_odd, ["age", "gender", "name"])

    def test_map_my(self):
        lst = [('score', [98, 99]), ('age', 23), ('length', 50)]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        dictionary.map_my(lambda x: x + 1)
        self.assertEqual(dictionary.to_list(), [('age', 24), ('length', 51), ('score', [99, 100])])

    def test_reduce_my(self):
        lst = [('age', [23, 22, 22]), ('score', [101, 100, 99])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        result = dictionary.reduce_my(lambda y, x: x + y, "score", 1)
        self.assertEqual(result, 301)

    def test_iter(self):
        dictionary = Dictionary()
        i = iter(dictionary)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_mconcat(self):
        list_1 = [('age', 23), ('score', 99)]
        list_2 = [('length', 100)]
        dictionary_1 = Dictionary()
        dictionary_1.from_list(list_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(list_2)

        dictionary_1.mconcat(dictionary_2)
        self.assertEqual(dictionary_1.to_list(), [('age', 23), ('length', 100), ('score', 99)])


if __name__ == '__main__':
    unittest.main()

