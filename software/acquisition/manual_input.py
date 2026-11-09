def read_rgb_reading():
    """Prompt for one RGB reading and return its numeric channel values."""
    red = float(input("Enter Red value: "))
    green = float(input("Enter Green value: "))
    blue = float(input("Enter Blue value: "))
    return red, green, blue