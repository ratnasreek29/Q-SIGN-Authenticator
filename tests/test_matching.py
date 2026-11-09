import unittest

from software.authentication.fingerprint_matching import (
    calculate_distance,
    find_closest_match,
)


class FingerprintMatchingTests(unittest.TestCase):
    def test_calculates_euclidean_distance(self):
        self.assertAlmostEqual(calculate_distance([0, 0, 0], [1, 2, 2]), 3.0)

    def test_finds_nearest_reference(self):
        references = {"TAG_A": [0, 0, 0], "TAG_B": [1, 1, 1]}
        self.assertEqual(find_closest_match([0.1, 0.1, 0.1], references)[0], "TAG_A")


if __name__ == "__main__":
    unittest.main()