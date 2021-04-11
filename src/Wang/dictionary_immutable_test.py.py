import unittest
import dictionary_immutable
class TestImmutableList(unittest.TestCase):
    def test_size(self):
        p=dictionary_immutable.Hashdic()
        self.assertEqual(dictionary_immutable.size(None), -1)
        p = dictionary_immutable.cons(p, 1, 5)

        self.assertEqual(dictionary_immutable.size(p), 1)
        p = dictionary_immutable.cons(p, 1025, 6)
        p = dictionary_immutable.cons(p, 2049, 9)
        self.assertEqual(dictionary_immutable.size(p), 3)

    def test_cons(self):
        p = dictionary_immutable.Hashdic()
        self.assertEqual(dictionary_immutable.cons(p, 1, 5), dictionary_immutable.cons(p, 1, 5))
        self.assertRaises(Exception, dictionary_immutable.cons, (p, None, 5))
        self.assertEqual(dictionary_immutable.cons(dictionary_immutable.cons(p, "a", 5), 2, 6), dictionary_immutable.cons(dictionary_immutable.cons(p, "a", 5), 2, 6))

    def test_remove(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 7)
        self.assertRaises(Exception, dictionary_immutable.remove, (p, None))
        self.assertRaises(Exception, dictionary_immutable.remove, (p, 7))
        self.assertEqual(dictionary_immutable.remove(p, 2), dictionary_immutable.cons(dictionary_immutable.Hashdic(), 1, 5))

    #
    # def test_head(self):
    #     self.assertRaises(AssertionError, lambda: head(None))
    #     self.assertEqual(head(cons('a', None)), 'a')
    #
    # def test_tail(self):
    #     self.assertRaises(AssertionError, lambda: tail(None))
    #     self.assertEqual(tail(cons('a', None)), None)
    #     self.assertEqual(tail(cons('a', cons('b', None))), cons('b', None))
    #
    # def test_reverse(self):
    #     self.assertEqual(reverse(None), None)
    #     self.assertEqual(reverse(cons('a', None)), cons('a', None))
    #     self.assertEqual(reverse(cons('a', cons('b', None))), cons('b', cons('a', None)))
    #
    def test_mconcat(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        m=dictionary_immutable.Hashdic()
        b = dictionary_immutable.Hashdic()
        b = dictionary_immutable.cons(b, 2, 10)
        c=dictionary_immutable.Hashdic()
        c= dictionary_immutable.cons(c, 2, 10)
        c = dictionary_immutable.cons(c, 1, 5)
        self.assertEqual(dictionary_immutable.mconcat(None, None), None)
        self.assertEqual(dictionary_immutable.mconcat(p, None), p)
        self.assertEqual(dictionary_immutable.mconcat(p, b), c)

    def test_to_list(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        self.assertEqual(dictionary_immutable.to_list(None), [])
        self.assertEqual(dictionary_immutable.to_list(p), [[1, 5]])
        p = dictionary_immutable.cons(p, "a", 6)
        self.assertEqual(dictionary_immutable.to_list(p), [[1, 5], ["a", 6]])

    def test_from_list(self):
        test_data = [[]]
        test_data1=[[1,5]]
        test_data2 = [[1, 5],["a", 6]]
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        self.assertEqual(dictionary_immutable.from_list(test_data), -1)
        self.assertEqual(dictionary_immutable.to_list(dictionary_immutable.from_list(test_data1)), test_data1)
        self.assertEqual(dictionary_immutable.from_list(test_data1), p)
        p = dictionary_immutable.cons(p, "a", 6)
        self.assertEqual(dictionary_immutable.from_list(test_data2), p)



    def test_iter(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)
        fun=dictionary_immutable.iterator(p)

        self.assertEqual(fun(), [1,5])
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
            return a+1
        self.assertEqual(dictionary_immutable.to_list(dictionary_immutable.map(p, add)), [[1, 6], [1025, 7], [2049, 10]])





    def test_filter(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 1025, 6)
        p = dictionary_immutable.cons(p, 2049, 9)

        def is_even(a):
            if a % 2 == 0:
                return True
            else:
                return False

        def is_odd(a):
            if a % 2 == 1:
                return True
            else:
                return False
        self.assertEqual(dictionary_immutable.filter(p, is_even), [[1025, 6]])
        self.assertEqual(dictionary_immutable.filter(p, is_odd), [[1, 5], [2049, 9]])


    def test_reduce(self):
        p = dictionary_immutable.Hashdic()
        p = dictionary_immutable.cons(p, 1, 5)
        p = dictionary_immutable.cons(p, 2, 6)
        p = dictionary_immutable.cons(p, 3, 9)
        def sum(a,b):
            return a+b
        self.assertEqual(dictionary_immutable.reduce(p, sum, 0), 5 + 6 + 9)

if __name__ == '__main__':
    unittest.main()

