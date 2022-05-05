class NumberNegativeError(Exception):
    def __init__(self, message="The length has to be a positive number"):
        self.message = message
        super().__init__(self.message)


def area(x):
    """
    calculate the area of a square
    :param x: Length of the side of a square
    :return: a number real that indicates the area of a square of side x
    """
    return x**2


print("Enter the length")
side = input()

try:
    float(side)
    if float(side) <= 0:
        raise NumberNegativeError
    else:
        side=float(side)
        print(f"The area of a square of side {side} is " + f"{area(side)}")
except ValueError:
    print(f'{side} is not a real number')
