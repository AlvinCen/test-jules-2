def complex_math(a, b):
    """
    A very complex mathematical operation.
    """
    result = 0
    for i in range(1000):
        result += (a * i) ** (b / (i + 1))
    return result

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        return [complex_math(x, 2) for x in self.data]
