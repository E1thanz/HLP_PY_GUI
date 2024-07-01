class Layer:
    def __init__(self, a: int = 0, b: int = 0, ma: bool = False, mb: bool = False):
        # a represents the barrel that the value goes into its comparator's side
        self.a = max(min(15, a), 0)
        # b represents the barrel that the value goes into its comparator's input
        self.b = max(min(15, b), 0)
        self.mode_a = ma
        self.mode_b = mb
        self.next_layer = None
        # precalculating the layer's mapping
        self.map = []
        self.calculate_map()

    # input a list of length 16 and return the output of the entire layer
    def output(self, input_vector: list) -> list:
        if self.next_layer is not None:
            return self.next_layer.output([self.map[value] for value in input_vector])
        return [self.map[value] for value in input_vector]

    # input a single value and return the output of the entire layer for this value
    def output_single(self, value: int) -> int:
        if self.next_layer is not None:
            return self.next_layer.output_single(self.map[value])
        return self.map[value]

    # return the text representation of the layer
    # representation made of: * if the mode is on (subtract) and a " " empty space if its on compare
    # after that that comparator's barrel's value in hexadecimal, then a comma (",") then the same thing for
    # the second comparator then a ";" sign
    def get_text_representation(self) -> str:
        if self.next_layer is not None:
            return ("*" if self.mode_b else " ") + str(hex(self.b))[2:].upper() + "," + ("*" if self.mode_a else " ") + str(hex(self.a))[2:].upper() + ";" + self.next_layer.get_text_representation()
        return ("*" if self.mode_b else " ") + str(hex(self.b))[2:].upper() + "," + ("*" if self.mode_a else " ") + str(hex(self.a))[2:].upper() + ";"

    # setting all the layers parameters using a text representation
    def set_text_representation(self, text_repr: str):
        self.mode_a = text_repr.startswith("*")
        text_repr = text_repr[1:]
        self.a = int(text_repr[0], 16)
        text_repr = text_repr[2:]
        self.mode_b = text_repr.startswith("*")
        text_repr = text_repr[1:]
        self.b = int(text_repr[0], 16)
        text_repr = text_repr[2:]
        if text_repr and self.next_layer is not None:
            self.next_layer.set_text_representation(text_repr)

    # prints all the layer's values
    def print(self, depth=0):
        if self.next_layer is not None:
            self.next_layer.print(depth + 1)
        print(f"{depth}: ({self.a}, {self.b}), ({round(self.a)}, {round(self.b)})")
        print(self.map, end="\n")

    # setter for a
    def set_a(self, new_a: int):
        self.a = max(min(15, new_a), 0)
        self.calculate_map()

    # setter for b
    def set_b(self, new_b: int):
        self.b = max(min(15, new_b), 0)
        self.calculate_map()

    # setting for a's comparator mode
    def set_mode_a(self, new_mode_a: bool):
        self.mode_a = new_mode_a
        self.calculate_map()

    # setting for b's comparator mode
    def set_mode_b(self, new_mode_b: bool):
        self.mode_b = new_mode_b
        self.calculate_map()

    # just makes the map
    def calculate_map(self):
        self.map = []
        for value in range(16):
            if self.mode_a:
                a_value = self.a - value
            else:
                a_value = self.a if self.a >= value else 0

            if self.mode_b:
                b_value = value - self.b
            else:
                b_value = value if value >= self.b else 0
            self.map.append(max(a_value, b_value, 0))


if __name__ == "__main__":
    layer = Layer()
    layer.next_layer = Layer()
    layer.set_text_representation("*1, F; A,*5;")
    layer.print()
    # params = ((9, 2, 1, 1), (11, 5, 1, 1), (1, 7, 1, 1))
    # layer = Layer(params[0][0], params[0][1], params[0][2], params[0][3])
    # layer_hold = layer
    # for i in range(1, 3):
    #     layer_hold.next_layer = Layer(params[i][0], params[i][1], params[i][2], params[i][3])
    #     layer_hold = layer_hold.next_layer
    # output = layer.output([i for i in range(16)])
    # layer.print()
    # print(output)

    # for i in range(1):
    #     layer.run(np.arange(16), np.array([0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1]), 0.1)
    #     # [3, 4, 4, 4, 4, 3, 3, 3, 4, 4, 4, 4, 3, 3, 4, 4]
    #     output = [layer.output(i) for i in range(16)]
    #     print(output)
    #     print(i)
    # layer.print()
