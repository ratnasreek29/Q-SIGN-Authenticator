def extract_rgb_features(red, green, blue):
    """Convert RGB sensor values to the three Q-SIGN ratio features."""
    if green == 0 or blue == 0:
        raise ValueError("Green and blue readings must be non-zero.")

    return red / green, blue / green, red / blue