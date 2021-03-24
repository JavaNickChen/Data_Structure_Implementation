import unittest
import CPO1
class TestImmutableList(unittest.TestCase):
    def test_size(self):
        p=CPO1.Hashdic()
        self.assertEqual(CPO1.size(None), -1)
        p = CPO1.cons(p, 1, 5)

        self.assertEqual(CPO1.size(p), 1)
        p = CPO1.cons(p, 1025, 6)
        p = CPO1.cons(p, 2049, 9)
        self.assertEqual(CPO1.size(p), 3)

    def test_cons(self):
        p = CPO1.Hashdic()
        self.assertEqual(CPO1.cons(p, 1, 5), CPO1.cons(p, 1, 5))
        self.assertEqual(CPO1.cons(CPO1.cons(p, 1, 5),2,6),CPO1.cons(CPO1.cons(p, 1, 5),2,6))

    def test_remove(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 2, 7)
        self.assertEqual(CPO1.remove(p,None), -1)
        self.assertEqual(CPO1.remove(p,2), CPO1.cons(CPO1.Hashdic(),1,5))

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
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        b = CPO1.Hashdic()
        b = CPO1.cons(b, 2, 10)
        c=CPO1.Hashdic()
        c= CPO1.cons(c, 2, 10)
        c = CPO1.cons(c, 1, 5)
        self.assertEqual(CPO1.mconcat(None, None), None)
        self.assertEqual(CPO1.mconcat(p, None), p)
        self.assertEqual(CPO1.mconcat(p,b), c)

    def test_to_list(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        self.assertEqual(CPO1.to_list(None), [])
        self.assertEqual(CPO1.to_list(p), [[1,5]])

    def test_from_list(self):
        test_data = [[]]
        test_data1=[[1,5]]
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        self.assertEqual(CPO1.from_list(test_data), -1)
        self.assertEqual(CPO1.to_list(CPO1.from_list(test_data1)), test_data1)
        self.assertEqual(CPO1.from_list(test_data1), p)



    def test_iter(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 2, 6)
        p = CPO1.cons(p, 3, 9)
        fun=CPO1.iterator(p)

        self.assertEqual(fun(), [1,5])
        self.assertEqual(fun(), [2, 6])
        self.assertEqual(fun(), [3, 9])
        self.assertEqual(fun(), -1)

    def test_find(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 2, 6)
        p = CPO1.cons(p, 3, 9)
        self.assertEqual(CPO1.find(p,2),[2,6])
        self.assertEqual(CPO1.find(p, 1),[1,5])
        self.assertEqual(CPO1.find(p, None), -1)

    def test_map(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 1025, 6)
        p = CPO1.cons(p, 2049, 9)
        def add(a):
            return a+1
        self.assertEqual(CPO1.to_list(CPO1.map(p,add)), [[1,6],[1025, 7],[2049, 10]])

    def test_filter(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 1025, 6)
        p = CPO1.cons(p, 2049, 9)

        self.assertEqual(CPO1.filter(p,True), [[1025, 6]])
        self.assertEqual(CPO1.filter(p, False), [[1,5],[2049, 9]])

    def test_reduce(self):
        p = CPO1.Hashdic()
        p = CPO1.cons(p, 1, 5)
        p = CPO1.cons(p, 2, 6)
        p = CPO1.cons(p, 3, 9)
        def sum(a,b):
            return a+b
        self.assertEqual(CPO1.reduce(p, sum,0), 5+6+9)

if __name__ == '__main__':
    unittest.main()

