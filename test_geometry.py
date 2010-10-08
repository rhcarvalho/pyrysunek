import unittest
from geometry import Point


class PointTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(Point(4, 5) + Point(1, -3), Point(5, 2))
        self.assertEqual(Point(4, 5) - Point(1, -3), Point(3, 8))
        self.assertEqual((Point(4, 5) + Point(1, -3)) / 2.0, Point(2.5, 1.0))
        self.assertEqual(Point(4, 5) * 2.0, Point(8.0, 10.0))

    def test_comparison(self):
        self.assertTrue(Point(1, 1) < Point(2, 3))
        self.assertTrue(Point(10, 1) < Point(5, 9))
        self.assertTrue(Point(10, 5) > Point(5, 6))
        self.assertTrue(Point(1, 5) == Point(1, 5))
        self.assertTrue(Point(2, 5) != Point(1, 5))
        self.assertTrue(Point(1, 1) <= Point(1, 1))
        self.assertTrue(Point(0, 1) <= Point(1, 1))
        self.assertTrue(Point(5, 6) >= Point(5, 6))
        self.assertTrue(Point(10, 5) >= Point(5, 6))

    def test_aggregation(self):
        self.assertTrue(Point(4, 6) & Point(2, 3), (4, 6, 2, 3))


if __name__ == "__main__":
    unittest.main()