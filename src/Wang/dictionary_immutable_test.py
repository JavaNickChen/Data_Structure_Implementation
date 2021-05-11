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
        self.assertRaises(
            Exception,
            dictionary_immutable.from_list,
            (test_data))
        self.assertEqual(
            dictionary_immutable.to_list(
                dictionary_immutable.from_list(test_data1)),
            test_data1)
        self.assertEqual(dictionary_immutable.from_list(test_data1), p)
        p = dictionary_immutable.cons(p, c, d)
        self.assertEqual(dictionary_immutable.from_list(test_data2), p)

    def generate_testlist(self, list):
        result = []
        temp = []
        index = 0
        pas = True
        if len(list) > 0:
            for e in list:
                index += 1
                temp.append(e)
                if index == 2:
                    result.append(temp)
                    index = 0
                    temp = []
        else:
            pas = False
        if len(temp) > 0:
            result.append(temp)
            pas = False
        return result, pas

    @given(a=st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        res, pas = self.generate_testlist(a)
        if res == []:
            self.assertEqual(
                dictionary_immutable.to_list(
                    dictionary_immutable.from_list(res)), [])
        else:
            if not pas:
                self.assertRaises(
                    Exception, dictionary_immutable.from_list, (res))
            else:
                test = True
                while test:
                    test = False
                    for i in range(len(res) - 1, -1, -1):
                        for j in range(i - 1, -1, -1):
                            if res[j][0] == res[i][0]:
                                res.remove(res[j])
                                test = True
                                break
                        if test:
                            break
                self.assertEqual(set(tuple(_) for _ in dictionary_immutable.to_list(
                    dictionary_immutable.from_list(res))), set(tuple(_) for _ in res))

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
        roll = 0
        for e in p:
            if roll == 0:
                self.assertEqual(e, [1, 5])
                roll += 1
            elif roll == 1:
                self.assertEqual(e, [2, 6])
                roll += 1
            else:
                self.assertEqual(e, [3, 9])
        i1 = iter(p)
        i2 = iter(p)
        self.assertEqual(next(i1), [1, 5])
        self.assertEqual(next(i1), [2, 6])
        self.assertEqual(next(i2), [1, 5])
        self.assertEqual(next(i2), [2, 6])
        self.assertEqual(next(i1), [3, 9])

    def test_find(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)
        self.assertEqual(dictionary_immutable.find(p, 2), [2, 6])
        self.assertEqual(dictionary_immutable.find(p, 1), [1, 5])
        self.assertEqual(dictionary_immutable.find(p, None), [-1, -1])
        self.assertRaises(
            Exception, dictionary_immutable.find, (p, 5))

    def test_map(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 1026, 6)
        p = dictionary_immutable.cons(p, 2012, 9)

        def add(a):
            return a + 1
        self.assertEqual(dictionary_immutable.to_list(
            dictionary_immutable.map(p, add)), [[1, 6], [1026, 7], [2012, 10]])

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

    @given(a=st.integers(), b=st.integers(), c=st.integers(), d=st.integers())
    def test_immutability_check(self, a, b, c, d):
        p = dictionary_immutable.Hashdic()
        p1 = dictionary_immutable.cons(p, a, b)
        self.assertNotEqual(id(p), id(p1))
        p2 = dictionary_immutable.remove(p1, a)
        self.assertNotEqual(id(p1), id(p2))
        p3 = dictionary_immutable.mempty(p2)
        self.assertNotEqual(id(p2), id(p3))
        p4 = dictionary_immutable.mconcat(p, p1)
        self.assertNotEqual(id(p4), id(p))
        self.assertNotEqual(id(p4), id(p1))

        def add(a):
            return a + 1
        p5 = dictionary_immutable.map(p4, add)
        self.assertNotEqual(id(p5), id(p4))


if __name__ == '__main__':
    unittest.main()
