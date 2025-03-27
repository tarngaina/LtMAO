
class V:
    def __init__(self):
        pass

v = [V(), V(), V()]
v[0].a = { 'hello': 'hi' }
v[1].a = { 'yes': 'sir' }
v[2].a = { 'wassup': 'nigg' }

v[0].i = 5
v[1].i = 23
v[2].i = 0

v.sort(key=lambda vertex: vertex.i)

a = 5