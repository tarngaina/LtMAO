class BIN:
    def __init__(self):
        self.masks = []

    def get_mask(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            length = len(lines)
            for index in range(length):
                if '= MaskData {' in lines[index]:
                    weights = []
                    name = lines[index].split(' = ')[0].replace(
                        ' ', '').replace('\t', '')
                    for index2 in range(index, length):
                        if 'mWeightList: list[f32] = {' in lines[index2]:
                            break
                    for index3 in range(index2+1, length):
                        if '}' in lines[index3]:
                            break
                        weights.append(lines[index3].replace(
                            ' ', '').replace('\t', '').replace('\n', ''))

                    # validate weights

                    weights = [
                        f'{float(weight):.3f}'
                        for weight in weights
                    ]

                    self.masks.append((name, weights))

    def save_mask(self, path):
        with open(path, 'w+') as f:
            text = []
            for mask, weights in self.masks:
                text.append(f'            {mask} = MaskData {{\n')
                text.append('                mWeightList: list[f32] = {\n')
                text.append(
                    ''.join(
                        f'                    {weight}\n' for weight in weights)
                )
                text.append('                }\n')
                text.append('            }\n')
            f.write(''.join(text))
