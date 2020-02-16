import png


class Kompleksiluku:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(a, b):
        return Kompleksiluku(a.x + b.x, a.y + b.y)

    def __pow__(a, b):
        if b == 2:
            return Kompleksiluku(a.x**2 - a.y**2, 2 * a.x * a.y)
        raise Error

    def __le__(a, b):
        if a.x <= b and a.y <= b:
            return True
        return False

    def __abs__(self):
        return Kompleksiluku(abs(self.x), abs(self.y))


def interpolate(arvo, a_min, a_max, b_min, b_max):
    a_ala = a_max - a_min
    b_ala = b_max - b_min
    skaalattu_arvo = float(arvo - a_min) / float(a_ala)
    return b_min + (skaalattu_arvo * b_ala)


def Mandelbrot(c, t):
    n = 0
    z = Kompleksiluku(0, 0)
    while abs(z) <= 2 and n < t:
        z = z**2 + c
        n += 1
    return n

leveys = 640
korkeus = 480
suhde = leveys / korkeus
tarkkuus = 256
zoom = 1
rivit = []
for j in range(korkeus):
    rivi = []
    for i in range(leveys):
        x = interpolate(i, 0, leveys, -1.0, 0.0)
        y = interpolate(j, 0, korkeus, -0.5, 0.5)
        m = Mandelbrot(Kompleksiluku(x, y), tarkkuus)
        #print(str(a) + ", " + str(b) + ": " + str(m))
        t = interpolate(m, 1, tarkkuus, 0, 255)
        rivi.append(int(t))
    rivit.append(rivi)
    print("rivi " + str(j) + ": " + str(rivi))
print(rivit)

f = open('mandelbrot.png', 'w+b')
w = png.Writer(leveys, korkeus, greyscale=True)
w.write(f, rivit)
f.close()
