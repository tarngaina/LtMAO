from math import sqrt, acos, sin


class Vector:
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x, y, z=None, w=None):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __iter__(self):
        yield self.x
        yield self.y
        if self.z != None:
            yield self.z
        if self.w != None:
            yield self.w

    def __str__(self):
        s = f'{self.x:.4f} {self.y:.4f}'
        if self.z != None:
            s += f' {self.z:.4f}'
        if self.w != None:
            s += f' {self.w:.4f}'
        return s

    def __json__(self):
        return [v for v in self]
    
    def lerp(vec1, vec2, weight):        
        return Vector(
            vec1.x + (vec2.x - vec1.x) * weight,
            vec1.y + (vec2.y - vec1.y) * weight,
            vec1.z + (vec2.z - vec1.z) * weight
        )


class Quaternion:
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        yield self.w


    def __mul__(self, other):
        if type(other) in (float, int):
            self.x *= other
            self.y *= other
            self.z *= other
            self.w *= other
        return self

    def __str__(self):
        return f'{self.x:.4f} {self.y:.4f} {self.z:.4f} {self.w:.4f}'

    def __json__(self):
        return [v for v in self]
    
    def slerp(quat1, quat2, weight):
        epsilon = 1e-6
        cos_omega = quat1.x * quat2.x + quat1.y * quat2.y + quat1.z * quat2.z + quat1.w * quat2.w
        flip = False
        if cos_omega < 0.0:
            flip = True
            cos_omega = -cos_omega
        if cos_omega > (1.0 - epsilon):
            s1 = 1.0 - weight
            s2 = -weight if flip else weight
        else:
            omega = acos(cos_omega)
            inv_sin_omega = 1 / sin(omega)
            s1 = sin((1.0 - weight) * omega) * inv_sin_omega
            s2 = -sin(weight * omega) * inv_sin_omega if flip else sin(weight * omega) * inv_sin_omega
        return Quaternion(
            s1 * quat1.x + s2 * quat2.x,
            s1 * quat1.y + s2 * quat2.y,
            s1 * quat1.z + s2 * quat2.z,
            s1 * quat1.w + s2 * quat2.w,
        )        


class Matrix4:
    __slots__ = (
        'a', 'b', 'c', 'd',
        'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p'
    )

    def __init__(self, *values):
        if len(values) == 16:
            (self.a, self.b, self.c, self.d,
             self.e, self.f, self.g, self.h,
             self.i, self.j, self.k, self.l,
             self.m, self.n, self.o, self.p) = values
        else:
            self.a = self.f = self.k = self.p = 1.0
            self.b = self.c = self.d = self.e = self.g = self.h = self.i = self.j = self.l = self.m = self.n = self.o = 0.0

    def __getitem__(self, index):
        return (
            self.a, self.b, self.c, self.d,
            self.e, self.f, self.g, self.h,
            self.i, self.j, self.k, self.l,
            self.m, self.n, self.o, self.p
        )[index]

    def __setitem__(self, index, value):
        values = self[:]
        values[index] = value
        (
            self.a, self.b, self.c, self.d,
            self.e, self.f, self.g, self.h,
            self.i, self.j, self.k, self.l,
            self.m, self.n, self.o, self.p
        ) = values

    def __iter__(self):
        values = (
            self.a, self.b, self.c, self.d,
            self.e, self.f, self.g, self.h,
            self.i, self.j, self.k, self.l,
            self.m, self.n, self.o, self.p
        )
        for v in values:
            yield v

    def __str__(self):
        return (
            f'{self.a:.4f} {self.b:.4f} {self.c:.4f} {self.d:.4f}\n'
            f'{self.e:.4f} {self.f:.4f} {self.g:.4f} {self.h:.4f}\n'
            f'{self.i:.4f} {self.j:.4f} {self.k:.4f} {self.l:.4f}\n'
            f'{self.m:.4f} {self.n:.4f} {self.o:.4f} {self.p:.4f}'
        )

    def __json__(self):
        return [v for v in self]

    def __mul__(self, other):
        return Matrix4(
            self.a * other.a + self.b * other.e + self.c * other.i + self.d * other.m,
            self.a * other.b + self.b * other.f + self.c * other.j + self.d * other.n,
            self.a * other.c + self.b * other.g + self.c * other.k + self.d * other.o,
            self.a * other.d + self.b * other.h + self.c * other.l + self.d * other.p,

            self.e * other.a + self.f * other.e + self.g * other.i + self.h * other.m,
            self.e * other.b + self.f * other.f + self.g * other.j + self.h * other.n,
            self.e * other.c + self.f * other.g + self.g * other.k + self.h * other.o,
            self.e * other.d + self.f * other.h + self.g * other.l + self.h * other.p,

            self.i * other.a + self.j * other.e + self.k * other.i + self.l * other.m,
            self.i * other.b + self.j * other.f + self.k * other.j + self.l * other.n,
            self.i * other.c + self.j * other.g + self.k * other.k + self.l * other.o,
            self.i * other.d + self.j * other.h + self.k * other.l + self.l * other.p,

            self.m * other.a + self.n * other.e + self.o * other.i + self.p * other.m,
            self.m * other.b + self.n * other.f + self.o * other.j + self.p * other.n,
            self.m * other.c + self.n * other.g + self.o * other.k + self.p * other.o,
            self.m * other.d + self.n * other.h + self.o * other.l + self.p * other.p
        )

    def inverse(self):
        d = (
            (self.a * self.f - self.e * self.b)
            * (self.k * self.p - self.o * self.l)
            - (self.a * self.j - self.i * self.b)
            * (self.g * self.p - self.o * self.h)
            + (self.a * self.n - self.m * self.b)
            * (self.g * self.l - self.k * self.h)
            + (self.e * self.j - self.i * self.f)
            * (self.c * self.p - self.o * self.d)
            - (self.e * self.n - self.m * self.f)
            * (self.c * self.l - self.k * self.d)
            + (self.i * self.n - self.m * self.j)
            * (self.c * self.h - self.g * self.d)
        )

        inv = Matrix4()
        if abs(d) >= 0.001:
            d = 1.0 / d

            inv.a = d * (self.f * (self.k * self.p - self.o * self.l) + self.j * (
                self.o * self.h - self.g * self.p) + self.n * (self.g * self.l - self.k * self.h))
            inv.e = d * (self.g * (self.i * self.p - self.m * self.l) + self.k * (
                self.m * self.h - self.e * self.p) + self.o * (self.e * self.l - self.i * self.h))
            inv.i = d * (self.h * (self.i * self.n - self.m * self.j) + self.l * (
                self.m * self.f - self.e * self.n) + self.p * (self.e * self.j - self.i * self.f))
            inv.m = d * (self.e * (self.n * self.k - self.j * self.o) + self.i * (
                self.f * self.o - self.n * self.g) + self.m * (self.j * self.g - self.f * self.k))

            inv.b = d * (self.j * (self.c * self.p - self.o * self.d) + self.n * (
                self.k * self.d - self.c * self.l) + self.b * (self.o * self.l - self.k * self.p))
            inv.f = d * (self.k * (self.a * self.p - self.m * self.d) + self.o * (
                self.i * self.d - self.a * self.l) + self.c * (self.m * self.l - self.i * self.p))
            inv.j = d * (self.l * (self.a * self.n - self.m * self.b) + self.p * (
                self.i * self.b - self.a * self.j) + self.d * (self.m * self.j - self.i * self.n))
            inv.n = d * (self.i * (self.n * self.c - self.b * self.o) + self.m * (
                self.b * self.k - self.j * self.c) + self.a * (self.j * self.o - self.n * self.k))

            inv.c = d * (self.n * (self.c * self.h - self.g * self.d) + self.b * (
                self.g * self.p - self.o * self.h) + self.f * (self.o * self.d - self.c * self.p))
            inv.g = d * (self.o * (self.a * self.h - self.e * self.d) + self.c * (
                self.e * self.p - self.m * self.h) + self.g * (self.m * self.d - self.a * self.p))
            inv.k = d * (self.p * (self.a * self.f - self.e * self.b) + self.d * (
                self.e * self.n - self.m * self.f) + self.h * (self.m * self.b - self.a * self.n))
            inv.o = d * (self.m * (self.f * self.c - self.b * self.g) + self.a * (
                self.n * self.g - self.f * self.o) + self.e * (self.b * self.o - self.n * self.c))

            inv.d = d * (self.b * (self.k * self.h - self.g * self.l) + self.f * (
                self.c * self.l - self.k * self.d) + self.j * (self.g * self.d - self.c * self.h))
            inv.h = d * (self.c * (self.i * self.h - self.e * self.l) + self.g * (
                self.a * self.l - self.i * self.d) + self.k * (self.e * self.d - self.a * self.h))
            inv.l = d * (self.d * (self.i * self.f - self.e * self.j) + self.h * (
                self.a * self.j - self.i * self.b) + self.l * (self.e * self.b - self.a * self.f))
            inv.p = d * (self.a * (self.f * self.k - self.j * self.g) + self.e * (
                self.j * self.c - self.b * self.k) + self.i * (self.b * self.g - self.f * self.c))
        # else: return identity anyway
        return inv

    def decompose(self):
        # this only support scale (1.0, 1.0, 1.0)
        # but we only use for update old skl, so its enough
        translate = Vector(self.m, self.n, self.o)

        scale = Vector(
            self.p * sqrt(self.a**2 + self.b**2 + self.c**2),
            self.p * sqrt(self.e**2 + self.f**2 + self.g**2),
            self.p * sqrt(self.i**2 + self.j**2 + self.k**2)
        )

        r_mat = Matrix4(
            *(
                self.a/scale.x, self.b/scale.y, self.c/scale.z, 0,
                self.e/scale.x, self.f/scale.y, self.g/scale.z, 0,
                self.i/scale.x, self.j/scale.y, self.k/scale.z, 0,
                0, 0, 0, 1
            )
        )
        dott = (r_mat.b * r_mat.g - r_mat.c * r_mat.f) * r_mat.i \
            + (r_mat.c * r_mat.e - r_mat.a * r_mat.g) * r_mat.j \
            + (r_mat.a * r_mat.f - r_mat.b * r_mat.e) * r_mat.k
        if dott < 0:
            scale.x *= -1
            r_mat.a *= -1
            r_mat.b *= -1
            r_mat.c *= -1
        trace = r_mat.a + r_mat.f + r_mat.k
        if trace > 0.00000001:
            s = sqrt(trace + 1.0)
            i_s = 0.5 / s
            rotate = Quaternion(
                (r_mat.g - r_mat.j) * i_s,
                (r_mat.i - r_mat.c) * i_s,
                (r_mat.b - r_mat.e) * i_s,
                s * 0.5
            )
        else:
            if r_mat.a >= r_mat.f and r_mat.a >= r_mat.k:
                s = sqrt(1.0 + r_mat.a - r_mat.f - r_mat.k)
                i_s = 0.5 / s
                rotate = Quaternion(
                    0.5 * s,
                    (r_mat.b + r_mat.e) * i_s,
                    (r_mat.i + r_mat.c) * i_s,
                    (r_mat.g - r_mat.j) * i_s,
                )
            elif r_mat.f > r_mat.k:
                s = sqrt(1.0 + r_mat.f - r_mat.a - r_mat.k)
                i_s = 0.5 / s
                rotate = Quaternion(
                    (r_mat.e + r_mat.b) * i_s,
                    0.5 * s,
                    (r_mat.j + r_mat.g) * i_s,
                    (r_mat.c - r_mat.i) * i_s
                )
            else:
                s = sqrt(1.0 + r_mat.k - r_mat.a - r_mat.f)
                i_s = 0.5 / s
                rotate = Quaternion(
                    (r_mat.c + r_mat.i) * i_s,
                    (r_mat.j + r_mat.g) * i_s,
                    0.5 * s,
                    (r_mat.b - r_mat.e) * i_s
                )

        return translate, rotate, scale
