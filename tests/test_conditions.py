import unittest
from covenant.conditions import *
from covenant.exceptions import *


class PreconditionTests(unittest.TestCase):
    def test_one_precondition(self):
        @pre(lambda x: x > 5)
        def foo(x):
            return x
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo(6), 6)
        with self.assertRaises(PreconditionViolationError):
            foo(5)

    def test_method(self):
        class Foo(object):
            @pre(lambda self, x: x > 5)
            def foo(self, x):
                return x
        f = Foo()
        self.assertEqual(f.foo.__name__, "foo")
        self.assertEqual(f.foo(6), 6)
        with self.assertRaises(PreconditionViolationError):
            f.foo(5)

    def test_two_preconditions(self):
        @pre(lambda x: x < 10)
        @pre(lambda x: x > 3)
        def foo(x):
            return x
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo(5), 5)
        with self.assertRaises(PreconditionViolationError):
            foo(2)
        with self.assertRaises(PreconditionViolationError):
            foo(11)

    def test_two_arguments(self):
        @pre(lambda x, y: x % y == 0)
        @pre(lambda x, y: x < 8)
        def foo(x, y):
            return x / y
        self.assertEqual(foo(4, 2), 2)
        with self.assertRaises(PreconditionViolationError):
            foo(4, 3)
        with self.assertRaises(PreconditionViolationError):
            foo(10, 2)

    def test_three_preconditions(self):
        @pre(lambda x: x > 0)
        @pre(lambda x: x < 10)
        @pre(lambda x: x % 2 == 0)
        def foo(x):
            return x
        self.assertEqual(foo(4), 4)

    def test_imports(self):
        def validate(x):
            return x > 5

        @pre(validate)
        def foo(x):
            return x

        self.assertEqual(foo(6), 6)
        with self.assertRaises(PreconditionViolationError):
            foo(5)

    def test_args(self):
        @pre(lambda args: len(args) > 1)
        def foo(*args):
            return len(args)
        self.assertEqual(foo(1, 2), 2)
        with self.assertRaises(PreconditionViolationError):
            foo(1)

    def test_with_exception(self):
        @pre(lambda x: float(x))
        def foo(x):
            return x + 1.0
        self.assertAlmostEqual(foo(1.0), 2.0)
        with self.assertRaises(PreconditionViolationError):
            foo("abcd")


class PostconditionTest(unittest.TestCase):
    def test_one_postcondition(self):
        @post(lambda r: r == 5)
        def foo():
            return 5
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo(), 5)

    def test_failed_postcondition(self):
        @post(lambda r: r == 5)
        def foo():
            return 6
        with self.assertRaises(PostconditionViolationError):
            foo()

    def test_with_arg(self):
        @post(lambda r, a: r == a * 2)
        def foo(a):
            return a * 2
        self.assertEqual(foo(2), 4)

    def test_two_postconditions(self):
        @post(lambda r, a: r == a * 2)
        @post(lambda r, a: r % 2 == 0)
        def foo(a):
            return a * 2

        self.assertEqual(foo(2), 4)

    def test_three_postconditions(self):
        @post(lambda r, a: r == a * 2)
        @post(lambda r, a: r % 2 == 0)
        @post(lambda r, a: True)
        def foo(a):
            return a * 2

        self.assertEqual(foo(2), 4)

    def test_with_exception(self):
        @post(lambda r: float(r))
        def foo():
            return "abcd"
        with self.assertRaises(PostconditionViolationError):
            foo()


class PostAndPreconditionTests(unittest.TestCase):
    def test_post_and_pre(self):
        @post(lambda r, a: r == a * 2)
        @pre(lambda a: a > 1)
        def foo(a):
            return a * 2

        self.assertEqual(foo(2), 4)
        with self.assertRaises(PreconditionViolationError):
            foo(1)


if __name__ == "__main__":
    unittest.main()
