import unittest

from software.processing.preprocessing import extract_rgb_features


class FeatureExtractionTests(unittest.TestCase):
    def test_extracts_rgb_ratios(self):
        self.assertEqual(extract_rgb_features(120, 100, 80), (1.2, 0.8, 1.5))

    def test_rejects_zero_denominators(self):
        with self.assertRaises(ValueError):
            extract_rgb_features(10, 0, 5)
        with self.assertRaises(ValueError):
            extract_rgb_features(10, 5, 0)


if __name__ == "__main__":
    unittest.main()