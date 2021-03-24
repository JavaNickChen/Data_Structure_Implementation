import unittest
from src.Chen.hash_map_based_dictionary_mutable.Dicationary import *


class TestMutableDictionary(unittest.TestCase):

    def test_add(self):
        dictionary = Dictionary()
        self.assertEqual(dictionary.to_list(), [[], []])
        dictionary.add("score", 89)
        self.assertEqual(dictionary.get_by_key("score"), [89])
        self.assertEqual(dictionary.to_list(), [["score"], [[89]]])
        dictionary.add("score", 78)
        self.assertEqual(dictionary.to_list(), [["score"], [[89, 78]]])
        dictionary.add("gender", "male")
        self.assertEqual(dictionary.to_list(), [["gender", "score"], [["male"], [89, 78]]])

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
                         [["age", "gender", "name", "others"], [[23], ["male"], ["Nick"], [10, 100]]])

    def test_from_list(self):
        list_keys = ["name", "age", "gender", "others"]
        list_values = ["Nick", 23, "male", [10, 100]]
        dictionary = Dictionary()
        dictionary.from_list(list_keys, list_values)
        self.assertEqual(dictionary.to_list(), [["age", "gender", "name", "others"], [[23], ["male"], ["Nick"], [10, 100]]])

    def test_get_by_key(self):
        list_keys = ["name", "age", "gender", "others"]
        list_values = ["Nick", 23, "male", [10, 100]]
        dictionary = Dictionary()
        dictionary.from_list(list_keys, list_values)
        self.assertEqual(dictionary.get_by_key("others"), [10, 100])

    def test_filter(self):
        list_keys = ["name", "age", "gender", "others"]
        list_values = ["Nick", 23, "male", [10, 100]]
        dictionary = Dictionary()
        dictionary.from_list(list_keys, list_values)
        result_even = dictionary.filter("even_value")
        self.assertEqual(result_even, ["others"])
        result_odd = dictionary.filter("odd_value")
        self.assertEqual(result_odd, ["age", "gender", "name"])

    def test_map_my(self):
        list_keys = ["age", "score", "length"]
        list_values = [23, 99, 78]
        dictionary = Dictionary()
        dictionary.from_list(list_keys, list_values)
        dictionary.map_my(lambda x: x + 1)
        self.assertEqual(dictionary.to_list(), [["age", "length", "score"], [[24], [79], [100]]])

    def test_reduce_my(self):
        list_keys = ["age", "score"]
        list_values = [[23, 22, 22], [101, 100, 99]]
        dictionary = Dictionary()
        dictionary.from_list(list_keys, list_values)
        result = dictionary.reduce_my(lambda y, x: x + y, "score", 1)
        self.assertEqual(result, 301)

    def test_iter(self):
        dictionary = Dictionary()
        i = iter(dictionary)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_mconcat(self):
        list_keys_1 = ["age", "score"]
        list_values_1 = [23, 99]
        list_keys_2 = ["length"]
        list_values_2 = [100]
        dictionary_1 = Dictionary()
        dictionary_1.from_list(list_keys_1, list_values_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(list_keys_2, list_values_2)
        dictionary_1.mconcat(dictionary_2)
        [keys, values] = dictionary_1.to_list()
        self.assertEqual([keys, values], [["age", "length", "score"], [[23], [100], [99]]])


if __name__ == '__main__':
    unittest.main()

