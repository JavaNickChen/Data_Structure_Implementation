import copy
import unittest
from operator import itemgetter

import hypothesis.strategies as st
from hypothesis import given

import TestUtils
from Dictionary_mutable import Dictionary


class DictionaryTest(unittest.TestCase):
    def test_add(self):
        dictionary = Dictionary()
        lst = []
        dictionary.add("score", 89)
        lst.append(("score", 89))
        self.assertEqual(dictionary.to_list(), [("score", 89)])
        dictionary.add("score", 78)
        lst.append(("score", 78))
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))
        dictionary.add("gender", "male")
        lst.append(("gender", "male"))
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

        dictionary2 = Dictionary()
        temp1 = (23, 34)
        temp2 = (23, 34)
        dictionary2.add(temp1, 'test_value_1')
        dictionary2.add(temp2, 'value2')
        lst1 = [(temp2, 'value2'), (temp1, 'test_value_1')]
        self.assertEqual(dictionary2.to_list(), TestUtils.sort(lst1))

        # Exception test
        # 1. Add repeated key-value.
        dictionary.add("score", 78)
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))
        # 2. Add invalid key
        self.assertRaises(Exception, dictionary.add, {'key1': 2, "key2": 3}, "dict_key_test")
        # 2. Add None value
        self.assertRaises(Exception, dictionary.add, "score", None)

    def test_set_value(self):
        dictionary = Dictionary()
        dictionary.add("age", 23)
        dictionary.set_value("age", 100)
        self.assertEqual(dictionary.get_by_key("age"), 100)

        # Set a value to a key which not exist.
        dictionary.set_value("color", "blue")
        self.assertEqual(dictionary.to_list(), TestUtils.sort([("age", 100), ("color", "blue")]))

    def test_remove_value(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("age", 34)
        self.assertEqual(dictionary.get_by_key("age"), [23, 34])
        dictionary.remove_value("age", 23)
        self.assertEqual(dictionary.get_by_key("age"), 34)

        # Exception test
        # Remove elements that do not exist.
        self.assertRaises(Exception, dictionary.remove_value, "age", 100)

    def test_remove_key(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("score", 10)
        dictionary.add("score", 100)
        dictionary.remove_key("gender")
        lst = [("age", 23), ("name", "Nick"), ("score", 10), ("score", 100)]
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))
        dictionary.remove_key("score")
        lst = [("age", 23), ("name", "Nick")]
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

        # Exception test
        # 1. Remove elements that do not exist.
        self.assertRaises(Exception, dictionary.remove_key, 23)
        # 2. Remove None key.
        self.assertRaises(Exception, dictionary.remove_key, None)

    def test_size(self):
        dictionary = Dictionary()
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        self.assertEqual(dictionary.size(), [4, 5])
        dictionary.remove_key("others")
        self.assertEqual(dictionary.size(), [3, 3])

    def test_to_list(self):
        dictionary = Dictionary()
        self.assertEqual(dictionary.to_list(), [])
        dictionary.add("name", "Nick")
        dictionary.add("age", 23)
        dictionary.add("gender", "male")
        dictionary.add("others", 10)
        dictionary.add("others", 100)
        lst = [("age", 23), ("gender", "male"), ("name", "Nick"), ("others", 10), ("others", 100)]
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

    def test_from_list(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        lst_2 = [('name', 'Nick'), ('others', [10, 100, 200])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key('gender'), 'male')
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

        # Existing dictionary object calls from_lst().
        dictionary.from_list(lst_2)
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst_2))

        # Exception test
        # There are invalid key or value in the list.
        lst_3 = [('name', None), ('others', [10, 100, 200]), (None, '10')]
        self.assertRaises(Exception, dictionary.from_list, lst_3)

    def test_get_by_key(self):
        lst = [('name', 'Nick'), ('age', 23), ('gender', 'male'), ('others', [10, 100])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        self.assertEqual(dictionary.get_by_key("others"), [10, 100])

        # Exception test
        # 1. Get by the invalid key.
        self.assertRaises(Exception, dictionary.get_by_key, None)
        # 2. Get by the not existing key.
        self.assertRaises(Exception, dictionary.get_by_key, 'color')

    def test_filter(self):
        # pair is an object like (key, value).
        def single_key_filter(pair):
            # Filter the key-value pairs that the key consists of single word.
            if not (type(pair[0]) is tuple):
                return pair
            elif (type(pair[0]) is tuple) and (len(pair[0]) == 1):
                return pair
        lst = [((2, 4), 'Nick'), ('age', 23), ('gender', 'male')]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        tmp2 = dictionary.filter(single_key_filter)
        tmp = sorted(tmp2, key=itemgetter(0, 1))
        self.assertEqual(tmp, [('age', 23), ('gender', 'male')])

    def test_map_my(self):
        lst = [('score', [98, {99, 100}]), ('age', 23), ('length', 50)]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        dictionary.map_my(lambda x: x + 1)
        result = [('age', 24), ('length', 51), ('score', [99, [100, 101]])]
        self.assertEqual(dictionary.to_list(), TestUtils.sort(result))

    def test_reduce_my(self):
        lst = [('age', [23, 22, 22]), ('score', [101, 100, 99])]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        result = dictionary.reduce_my(lambda y, x: x + y, "score", 1)
        self.assertEqual(result, 301)

    def test_iter_and_next(self):
        lst = [('age', 23), ('score', 95), ('color', 'blue')]
        dictionary = Dictionary()
        dictionary.from_list(lst)
        tmp_1 = []
        for key, value in dictionary:
            tmp_1.append((key, value))
        sorted_tmp = TestUtils.sort(tmp_1)
        t = dictionary.to_list()
        self.assertEqual(t, sorted_tmp)

        # Test for two iterators on one data structure working in parallel.
        tmp_2 = []
        tmp_3 = [('age', 'age'), ('age', 'score'), ('age', 'color'), ('score', 'age'), ('score', 'score'),
                 ('score', 'color'), ('color', 'age'), ('color', 'score'), ('color', 'color')]
        for iterator_1 in dictionary:
            for iterator_2 in dictionary:
                tmp_2.append((iterator_1[0], iterator_2[0]))
        tmp_2 = TestUtils.sort(tmp_2)
        tmp_3 = TestUtils.sort(tmp_3)
        self.assertEqual(tmp_2, tmp_3)

        it = iter(Dictionary())
        self.assertRaises(StopIteration, lambda: next(it))

    @given(lst=st.lists(st.tuples(st.tuples(), st.text())))
    def test_monoid_identity(self, lst):
        lst = TestUtils.lst_validate(lst)
        dictionary_1 = Dictionary()
        dictionary_1.from_list(lst)
        dictionary_2 = copy.deepcopy(dictionary_1)
        dictionary_3 = copy.deepcopy(dictionary_1)

        # ae = a
        dictionary_1.mconcat(dictionary_1.mempty())
        self.assertEqual(dictionary_1, dictionary_2)

        # ea = a
        tmp = dictionary_3.mempty()
        tmp.mconcat(dictionary_3)
        self.assertEqual(tmp, dictionary_2)

    @given(lst_1=st.lists(st.tuples(st.text(), st.text())), lst_2=st.lists(st.tuples(st.integers(), st.text())), lst_3=st.lists(st.tuples(st.sets(st.integers()), st.text())),)
    def test_associativity(self, lst_1, lst_2, lst_3):
        lst_1 = TestUtils.lst_validate(lst_1)
        lst_2 = TestUtils.lst_validate(lst_2)
        lst_3 = TestUtils.lst_validate(lst_3)
        dictionary_1 = Dictionary()
        dictionary_1.from_list(lst_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(lst_2)
        dictionary_3 = Dictionary()
        dictionary_3.from_list(lst_3)

        # It equals to "(ab)c".
        dictionary_1.mconcat(dictionary_2)
        dictionary_1.mconcat(dictionary_3)
        temp1 = dictionary_1

        dictionary_1 = Dictionary()
        dictionary_1.from_list(lst_1)
        dictionary_2 = Dictionary()
        dictionary_2.from_list(lst_2)

        # It equals to "a(bc)".
        dictionary_2.mconcat(dictionary_3)
        dictionary_1.mconcat(dictionary_2)
        temp2 = dictionary_1
        assert id(temp2) != id(temp1)

        # To determine if "(ab)c = a(bc)" holds.
        self.assertEqual(temp1, temp2)

    @given(st.lists(st.tuples(st.integers(), st.text())))
    def test_from_list_2(self, lst):
        dictionary = Dictionary()
        dictionary.from_list(lst)
        lst = TestUtils.lst_validate(lst)
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

    @given(lst=st.lists(st.tuples(st.integers(), st.text())))
    def test_from_list_to_list_equality(self, lst):
        dictionary = Dictionary()
        lst = TestUtils.lst_validate(lst)
        dictionary.from_list(lst)
        self.assertEqual(dictionary.to_list(), TestUtils.sort(lst))

    @given(lst=st.lists(st.tuples(st.text(), st.text())))
    def test_python_len_and_dictionary_size_equality(self, lst):
        dictionary = Dictionary()
        lst = TestUtils.lst_validate(lst)
        dictionary.from_list(lst)
        self.assertEqual(len(dictionary.to_list()), dictionary.size()[1])


if __name__ == '__main__':
    unittest.main()

