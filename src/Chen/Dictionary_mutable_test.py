import unittest
from operator import itemgetter
import functools as ft

from Dictionary_mutable import Dictionary
from hypothesis import given, example
import hypothesis.strategies as st


class DictionaryTest(unittest.TestCase):
    # unit test for add()
    def test_add(self):
        dictionary = Dictionary()
        lst = []
        dictionary.add("score", 89)
        lst.append(("score", 89))
        self.assertEqual(dictionary.to_list(), [("score", 89)])
        dictionary.add("score", 78)
        lst.append(("score", 78))
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))
        dictionary.add("gender", "male")
        lst.append(("gender", "male"))
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

        dictionary2 = Dictionary()
        temp1 = (23, 34)
        temp2 = (23, 34)
        dictionary2.add(temp1, 'test_value_1')
        dictionary2.add(temp2, 'value2')
        lst1 = [(temp2, 'value2'), (temp1, 'test_value_1')]
        self.assertEqual(dictionary2.to_list(), sorted(lst1, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

        # Exception test
        # 1. Add repeated key-value.
        dictionary.add("score", 78)
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))
        # 2. Add invalid key
        dictionary.add({'key1': 2, "key2": 3}, "dict_key_test")
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))
        # 2. Add None value
        dictionary.add("score", None)
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

    # unit test for remove_by_key()
    def test_remove_by_key(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("score", 10)
        dictionary.add("score", 100)
        dictionary.remove_by_key("gender")
        lst = [("age", 23), ("name", "Nick"), ("score", 10), ("score", 100)]
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))
        dictionary.remove_by_key("score")
        lst = [("age", 23), ("name", "Nick")]
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

        # Exception test
        # 1. Remove elements that do not exist. It's going to have log output on the console.
        dictionary.remove_by_key(23)
        # 2. Remove None key. It's going to have log output on the console.
        dictionary.remove_by_key(None)

    # unit test for size()
    def test_size(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        self.assertEqual(dictionary.size(), [4, 5])
        dictionary.remove_by_key("others")
        self.assertEqual(dictionary.size(), [3, 3])

    # unit test for to_list()
    def test_to_list(self):
        dictionary = Dictionary()
        self.assertEqual(dictionary.to_list(), [])
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        lst = [("age", 23), ("gender", "male"), ("name", "Nick"), ("others", 10), ("others", 100)]
        self.assertEqual(dictionary.to_list(), sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

    # unit test for from_list()
    def test_from_list(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        lst_2 = [('name', 'Nick'), ('age', None), (None, 'male'), ('others', [10, 100, 200])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key('gender'), 'male')
        self.assertEqual(dictionary.to_list(),
                         sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

        # Existing dictionary object with some elements
        dictionary.from_list(lst_2)
        lst_3 = [('age', 23), ('gender', 'male'), ('name', 'Nick'), ('others', [10, 100]), ('others', [10, 100, 200])]
        self.assertEqual(dictionary.to_list(),
                         sorted(lst_3, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))
        # Exception test
        # There are invalid key or value in the list.
        dictionary2 = Dictionary()
        dictionary2.from_list(lst_2)
        lst_4 = [('name', 'Nick'), ('others', [10, 100, 200])]
        self.assertEqual(dictionary2.to_list(),
                         sorted(lst_4, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

    # unit test for get_by_key()
    def test_get_by_key(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key("others"), [10, 100])

        # Exception test
        # 1. Get by the invalid key. It's going to have log output on the console.
        self.assertEqual(dictionary.get_by_key(None), None)
        # 2. Get by the not existing key. It's going to have log output on the console.
        self.assertEqual(dictionary.get_by_key("color"), None)

    # unit test for filter()
    def test_filter(self):
        # the operation object of the self-defined function should be a key-value pair.
        # pair = (key, value)
        def single_key_filter(pair):
            # filter the key-value pairs that the key consists of single word.
            if not (type(pair[0]) is tuple):
                return pair
            elif (type(pair[0]) is tuple) and (len(pair[0]) == 1):
                return pair
            else:
                return None

        lst = [((2, 4), 'Nick'), ('age', 23), ('gender', 'male')]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        tmp = sorted(dictionary.filter(single_key_filter), key=itemgetter(0, 1))
        self.assertEqual(tmp, [('age', 23), ('gender', 'male')])

    # unit test for map_my()
    def test_map_my(self):
        lst = [('score', [98, {99, 100}]), ('age', 23), ('length', 50)]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        dictionary.map_my(lambda x: x + 1)
        result = [('age', 24), ('length', 51), ('score', [99, [100, 101]])]
        self.assertEqual(dictionary.to_list(), sorted(result, key=ft.cmp_to_key(dictionary.compare_for_list_key_value)))

    # unit test for reduce_my()
    def test_reduce_my(self):
        lst = [('age', [23, 22, 22]), ('score', [101, 100, 99])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        result = dictionary.reduce_my(lambda y, x: x + y, "score", 1)
        self.assertEqual(result, 301)

    # unit test for iter() and next()
    def test_iter_and_next(self):
        lst = [('score', [98, 99]), ('age', 23), ('length', 50), ('length', 60)]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        tmp = []
        for key, value in dictionary:
            tmp.append((key, value))
        sorted_tmp = sorted(tmp, key=ft.cmp_to_key(dictionary.compare_for_list_key_value))
        t = dictionary.to_list()
        self.assertEqual(t, sorted_tmp)

        it = iter(Dictionary())
        self.assertRaises(StopIteration, lambda: next(it))

    # property-based test
    # Implement Associativity. For all a, b and c in S, the equation (ab)c = a(bc) holds.
    # S is dictionary objects set.
    def test_mconcat(self):
        list_1 = [('age', 23), ('score', 99)]
        list_2 = [('length', 100)]
        list_3 = [("length", 200), ("color", "red")]

        dictionary_1 = Dictionary()
        dictionary_1.from_list(list_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(list_2)
        dictionary_3 = Dictionary()
        dictionary_3.from_list(list_3)

        # It equals to "(ab)c".
        dictionary_2.mconcat(dictionary_3)
        dictionary_1.mconcat(dictionary_2)
        temp1 = dictionary_1

        dictionary_1 = Dictionary()
        dictionary_1.from_list(list_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(list_2)

        # It equals to "a(bc)".
        dictionary_2.mconcat(dictionary_1)
        dictionary_3.mconcat(dictionary_2)
        temp2 = dictionary_3

        # To determine if "(ab)c" and "a(bc)" are equal
        self.assertEqual(temp1.to_list(), temp2.to_list())

    # property-based test
    # Implement Identity element There exists an element e (mempty) in S such that for every element a in S,
    # the equations ea = ae = a hold.
    # "e" is Corresponding to the return of mempty() function in the code.
    def test_mempty(self):
        dictionary_1 = Dictionary()
        dictionary_2 = Dictionary()
        dictionary_3 = Dictionary().mempty()
        list_1 = [('age', 23), ('score', 99)]
        dictionary_1.from_list(list_1)
        dictionary_2.from_list(list_1)
        dictionary_4 = dictionary_1

        # It equals to "ae".
        dictionary_1.mconcat(dictionary_3)
        # It equals to "ea".
        dictionary_3.mconcat(dictionary_2)
        # To determine if "ae" and "ea" are equal
        self.assertEqual(dictionary_1.to_list(), dictionary_3.to_list())
        # To determine if "ae" and "a" are equal
        self.assertEqual(dictionary_1.to_list(), dictionary_4.to_list())

    @given(lst=st.lists(st.tuples(st.integers(), st.text())))
    def test_from_list_to_list_equality(self, lst):
        dictionary = Dictionary()

        # To pick out and remove all key-value pairs with invalid 'key' or 'value'
        indexes = []
        for index in range(len(lst)):
            if not dictionary.validate(lst[index][0], lst[index][1]):
                indexes.append(index)
        indexes.reverse()
        for index in indexes:
            lst.pop(index)
        lst = list(set(lst))
        temp = sorted(lst, key=ft.cmp_to_key(dictionary.compare_for_list_key_value))
        dictionary.from_list(lst)
        self.assertEqual(dictionary.to_list(), temp)

    # property-based test
    def test_python_len_and_dictionary_size_equality(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(len(dictionary.to_list()), dictionary.size()[1])


if __name__ == '__main__':
    unittest.main()

