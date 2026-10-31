import unittest

from software.authentication.product_authentication import authenticate_reading


class ProductAuthenticationTests(unittest.TestCase):
    def test_matches_registered_products_using_rgb_readings(self):
        products = {"PROD_001": "TAG_A"}
        references = {"TAG_A": [1.2, 0.8, 1.5]}

        tag, distance, matched = authenticate_reading(
            "PROD_001", (120, 100, 80), products, references
        )

        self.assertEqual(tag, "TAG_A")
        self.assertAlmostEqual(distance, 0.0)
        self.assertTrue(matched)

    def test_rejects_unregistered_products(self):
        with self.assertRaises(KeyError):
            authenticate_reading("PROD_UNKNOWN", (120, 100, 80), {}, {})


if __name__ == "__main__":
    unittest.main()