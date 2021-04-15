import unittest
import dictionary_immutable
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):

    def test_size(self):
        p = dictionary_immutable.Hashdic()
        self.assertEqual(dictionary_immutable.size(None), -1)
        p = dictionary_immutable.cons(p, 1, 5)
        self.assertEqual(dictionary_immutable.size(p), 1)
        p = dictionary_immutable.cons(p, 1025, 6)
        p = dictionary_immutable.cons(p, 2049, 9)
        self.assertEqual(dictionary_immutable.size(p), 3)

    def test_cons(self):
        p = dictionary_immutable.Hashdic()
        self.assertEqual(
            dictionary_immutable.cons(
                p, 1, 5), dictionary_immutable.cons(
                p, 1, 5))
        self.assertRaises(Exception, dictionary_immutable.cons, (p, None, 5))
        self.assertEqual(
            dictionary_immutable.cons(
                dictionary_immutable.cons(
                    p, "a", 5), 2, 6), dictionary_immutable.cons(
                dictionary_immutable.cons(
                    p, "a", 5), 2, 6))

    def test_remove(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 7)
        self.assertRaises(Exception, dictionary_immutable.remove, (p, None))
        self.assertRaises(Exception, dictionary_immutable.remove, (p, 7))
        self.assertEqual(
            dictionary_immutable.remove(
                p, 2), dictionary_immutable.cons(
                dictionary_immutable.Hashdic(), 1, 5))

    @given(a=st.integers(), b=st.integers(), c=st.integers(),
           d=st.integers(), e=st.integers(), f=st.integers())
    def test_mconcat(self, a, b, c, d, e, f):
        emp = dictionary_immutable.Hashdic()
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, a, b)
        m = dictionary_immutable.Hashdic()
        q = dictionary_immutable.Hashdic()
        q = dictionary_immutable.cons(q, c, d)
        m = dictionary_immutable.Hashdic()
        m = dictionary_immutable.cons(m, a, b)
        m = dictionary_immutable.cons(m, c, d)
        n = dictionary_immutable.Hashdic()
        n = dictionary_immutable.cons(n, e, f)
        self.assertEqual(dictionary_immutable.mconcat(None, None), None)
        self.assertEqual(dictionary_immutable.mconcat(p, None), p)
        self.assertEqual(dictionary_immutable.mconcat(emp, emp), emp)
        self.assertEqual(dictionary_immutable.mconcat(p, emp), p)
        self.assertEqual(dictionary_immutable.mconcat(p, q), m)
        self.assertEqual(
            dictionary_immutable.mconcat(
                dictionary_immutable.mconcat(
                    p, q), n), dictionary_immutable.mconcat(
                p, dictionary_immutable.mconcat(
                    q, n)))

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_to_list(self, a, b, c, d):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, a, b)
        self.assertEqual(dictionary_immutable.to_list(None), [])
        self.assertEqual(dictionary_immutable.to_list(p), [[a, b]])
        p = dictionary_immutable.cons(p, c, d)
        if a == c:
            self.assertEqual(dictionary_immutable.to_list(p), [[c, d]])
        else:
            if a.__hash__() % p.code > c.__hash__() % p.code:
                self.assertEqual(
                    dictionary_immutable.to_list(p), [[c, d], [a, b]])
            else:
                self.assertEqual(
                    dictionary_immutable.to_list(p), [[a, b], [c, d]])

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_from_list(self, a, b, c, d):
        test_data = [[]]
        test_data1 = [[a, b]]
        test_data2 = [[a, b], [c, d]]
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, a, b)
        self.assertEqual(dictionary_immutable.from_list(test_data), -1)
        self.assertEqual(
            dictionary_immutable.to_list(
                dictionary_immutable.from_list(test_data1)),
            test_data1)
        self.assertEqual(dictionary_immutable.from_list(test_data1), p)
        p = dictionary_immutable.cons(p, c, d)
        self.assertEqual(dictionary_immutable.from_list(test_data2), p)

    def test_iter(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)
        fun = dictionary_immutable.iterator(p)
        self.assertEqual(fun(), [1, 5])
        self.assertEqual(fun(), [2, 6])
        self.assertEqual(fun(), [3, 9])
        self.assertEqual(fun(), -1)

    def test_find(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)
        self.assertEqual(dictionary_immutable.find(p, 2), [2, 6])
        self.assertEqual(dictionary_immutable.find(p, 1), [1, 5])
        self.assertEqual(dictionary_immutable.find(p, None), -1)

    def test_map(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 1025, 6)
        p = dictionary_immutable.cons(p, 2049, 9)

        def add(a):
            return a + 1
        self.assertEqual(dictionary_immutable.to_list(
            dictionary_immutable.map(p, add)), [[1, 6], [1025, 7], [2049, 10]])

    def test_filter(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 1025, 6)
        p = dictionary_immutable.cons(p, 2049, 9)

        def is_even(a):
            return a % 2 == 0

        def is_odd(a):
            return a % 2 == 1
        self.assertEqual(dictionary_immutable.filter(p, is_even), [[1025, 6]])
        self.assertEqual(dictionary_immutable.filter(
            p, is_odd), [[1, 5], [2049, 9]])

    def test_reduce(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)

        def sum(a, b):
            return a + b
        self.assertEqual(dictionary_immutable.reduce(p, sum, 0), 5 + 6 + 9)


if __name__ == '__main__':
    unittest.main()
