import numpy as np
from math import cos, sin, pi, sqrt, log
from PIL import Image, ImageDraw

class Fractal_Mandelbrot:
    def __init__(self, width=800, height=600, max_iter=100, power=2, c=0+0j):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.power = power      # exponent v z -> z**power + c
        self.c = c              # konstantní c, nebo použij v compute podle bodu

    def compute(self, x_min=-2.0, x_max=1.0, y_min=-1.5, y_max=1.5):
        """
        Vypočte pole (height×width) s počtem iterací do divergence.
        """
        xs = np.linspace(x_min, x_max, self.width)
        ys = np.linspace(y_min, y_max, self.height)
        Z = np.zeros((self.height, self.width), dtype=np.complex128)
        C = np.array([[complex(x, y) for x in xs] for y in ys], dtype=np.complex128)
        M = np.zeros_like(Z, dtype=int)

        for i in range(self.max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**self.power + C[mask]
            M[mask] = i
        # přepočet intenzity do 0–255
        return np.uint8(255 * M / self.max_iter)

    def to_image(self, x_min=-2.0, x_max=1.0, y_min=-1.5, y_max=1.5):
        data = self.compute(x_min, x_max, y_min, y_max)
        return Image.fromarray(data, mode='L')
class FractalJulia:
    """
    Vypočítá Juliovu množinu a vrátí PIL Image.
    """
    def __init__(self, width=800, height=600, max_iter=100, power=2, c=complex(-0.7,0.27015)):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.power = power
        self.c = c

    def compute(self, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
        xs = np.linspace(x_min, x_max, self.width)
        ys = np.linspace(y_min, y_max, self.height)
        Z = np.array([[complex(x, y) for x in xs] for y in ys], dtype=np.complex128)
        M = np.zeros_like(Z, dtype=int)
        for i in range(self.max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**self.power + self.c
            M[mask] = i
        return np.uint8(255 * M / self.max_iter)

    def to_image(self, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
        data = self.compute(x_min, x_max, y_min, y_max)
        return Image.fromarray(data, mode='L')


class KochSnowflake:
    """
    Generuje obrázek Kochovy vločky.

    Parametry:
      size         -- velikost (šířka) výstupního obrázku v pixelech
      depth        -- hloubka rekurze (počet iterací)
      line_width   -- tloušťka čáry v pixelech
      line_color   -- barva čáry jako (R, G, B)
      background   -- barva pozadí jako (R, G, B)
    """
    def __init__(self,
                 size: int = 800,
                 depth: int = 4,
                 line_width: int = 1,
                 line_color=(0, 0, 0),
                 background=(255, 255, 255)):
        self.size = size
        self.depth = depth
        self.line_width = line_width
        self.line_color = line_color
        self.background = background

    def _koch_iteration(self, points: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """
        Jedna iterace rozdělení každé úsečky na 4 úsečky s vnitřním špičatým vrcholem.
        """
        new_points: list[tuple[float, float]] = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p5 = points[i + 1]
            # dělení segmentu na třetiny
            dx = (p5[0] - p1[0]) / 3
            dy = (p5[1] - p1[1]) / 3
            p2 = (p1[0] + dx, p1[1] + dy)
            p4 = (p1[0] + 2*dx, p1[1] + 2*dy)
            # vrchol trojúhelníku otočený o 60°
            vx = p4[0] - p2[0]
            vy = p4[1] - p2[1]
            angle = -pi / 3  # -60°
            px = vx * cos(angle) - vy * sin(angle)
            py = vx * sin(angle) + vy * cos(angle)
            p3 = (p2[0] + px, p2[1] + py)

            # přidej body do nové řady: p1, p2, p3, p4
            new_points.extend([p1, p2, p3, p4])
        new_points.append(points[-1])
        return new_points

    def generate(self) -> list[tuple[float, float]]:
        """
        Vygeneruje výchozí trojúhelník a aplikuje Kochovu iteraci depth-krát.
        Vrací seznam bodů v pořadí, které lze přímo nakreslit jako uzavřenou lomenou čáru.
        """
        # výška rovnoramenného trojúhelníku se stranou size
        height = self.size * sqrt(3) / 2
        # počáteční rovnostranný trojúhelník
        p1 = (0, height)
        p2 = (self.size / 2, 0)
        p3 = (self.size, height)
        points = [p1, p2, p3, p1]
        for _ in range(self.depth):
            points = self._koch_iteration(points)
        return points

    def to_image(self) -> Image:
        """
        Vytvoří PIL.Image kreslením Kochovy vločky na bílé pozadí.
        """
        pts = self.generate()
        # vypočítej bounding box
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = int(max_x - min_x) + 2*self.line_width
        height = int(max_y - min_y) + 2*self.line_width

        # připrav plátno
        img = Image.new('RGB', (width, height), self.background)
        draw = ImageDraw.Draw(img)

        # posuň body tak, aby min_x,min_y byl v (line_width,line_width)
        offset = (-min_x + self.line_width, -min_y + self.line_width)
        shifted = [(x + offset[0], y + offset[1]) for (x, y) in pts]

        # vykresli čáru
        draw.line(shifted, fill=self.line_color, width=self.line_width)
        return img

class SquareSnowflake:
    """
    Generuje vnitřní "Čtvercovou vločku" podobnou Kochově, založenou na čtvercovém fractalu.
    Každý úsek se rozdělí do čtyř částí s vrcholem otočeným o +90° ( dovnitř čtverce ).
    """
    def __init__(self, size: int = 800, depth: int = 4,
                 line_width: int = 1, line_color=(0,0,0), background=(255,255,255)):
        self.size = size
        self.depth = depth
        self.line_width = line_width
        self.line_color = line_color
        self.background = background

    def _square_iteration(self, points: list[tuple[float,float]]) -> list[tuple[float,float]]:
        new_pts: list[tuple[float, float]] = []
        for i in range(len(points) - 1):
            p1, p5 = points[i], points[i + 1]
            # rozděl segment na třetiny
            dx = (p5[0] - p1[0]) / 3
            dy = (p5[1] - p1[1]) / 3
            p2 = (p1[0] + dx, p1[1] + dy)
            p4 = (p1[0] + 2*dx, p1[1] + 2*dy)
            # vnitřní čtverec: rotace o 90° (pi/2)
            angle = pi / 2
            ux = dx * cos(angle) - dy * sin(angle)
            uy = dx * sin(angle) + dy * cos(angle)
            p3 = (p2[0] + ux, p2[1] + uy)
            p3b = (p4[0] + ux, p4[1] + uy)
            # přidej body: p1, p2, p3, p3b, p4
            new_pts.extend([p1, p2, p3, p3b, p4])
        new_pts.append(points[-1])
        return new_pts

    def generate(self) -> list[tuple[float,float]]:
        # základní čtverec
        pts = [(0,0), (self.size,0), (self.size,self.size), (0,self.size), (0,0)]
        for _ in range(self.depth): pts = self._square_iteration(pts)
        return pts

    def to_image(self) -> Image:
        pts = self.generate()
        xs, ys = [x for x,y in pts], [y for x,y in pts]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = int(max_x-min_x)+2*self.line_width
        h = int(max_y-min_y)+2*self.line_width
        img = Image.new('RGB', (w,h), self.background)
        draw = ImageDraw.Draw(img)
        off = (-min_x+self.line_width, -min_y+self.line_width)
        shifted = [(x+off[0],y+off[1]) for x,y in pts]
        draw.line(shifted, fill=self.line_color, width=self.line_width)
        return img

class LyapunovFractal:
    """
    Vypočítá Lyapunovův fraktál pro dané parametry A a B podle zvoleného vzoru (pattern).
    Exponenciální nárůst chaosu: λ = lim (1/N) Σ log|r_i (1 - 2 x_i)|

    Parametry:
      width, height -- rozměry obrázku
      iterations    -- počet iterací pro výpočet exponentu
      pattern       -- řetězec složený z 'A' a 'B', podle něhož volíme r=A nebo r=B
      a_range       -- (min,max) pro parametr A
      b_range       -- (min,max) pro parametr B
    """
    def __init__(self,
                 width=400,
                 height=400,
                 iterations=100,
                 pattern='AB',
                 a_range=(2.5, 4.0),
                 b_range=(2.5, 4.0)):
        self.width = width
        self.height = height
        self.iterations = iterations
        self.pattern = pattern
        self.a_min, self.a_max = a_range
        self.b_min, self.b_max = b_range

    def compute(self):
        # připrav pole pro výsledné exponenty
        exponents = np.zeros((self.height, self.width), dtype=float)
        # grid hodnot A a B pro osy
        A = np.linspace(self.a_min, self.a_max, self.width)
        B = np.linspace(self.b_min, self.b_max, self.height)
        for j, b in enumerate(B):
            for i, a in enumerate(A):
                x = 0.5
                lyap = 0.0
                for n in range(self.iterations):
                    r = a if self.pattern[n % len(self.pattern)] == 'A' else b
                    x = r * x * (1 - x)
                    # vynech prvních 10% iterací jako transient
                    if n > self.iterations * 0.1:
                        lyap += log(abs(r * (1 - 2*x)) + 1e-12)
                exponents[j, i] = lyap / (self.iterations * 0.9)
        # škálování do 0–255
        # posun a násobek pro viditelné kontrasty
        min_e, max_e = exponents.min(), exponents.max()
        norm = (exponents - min_e) / (max_e - min_e) * 255
        return np.uint8(norm)

    def to_image(self):
        data = self.compute()
        return Image.fromarray(data, mode='L')

class BarnsleyFern:
    """
    Generuje Barnsleyův kapradinový fraktál pomocí IFS.
    """
    def __init__(self, width=500, height=600, iterations=100000):
        self.width = width; self.height = height
        self.iterations = iterations
        # IFS pravděpodobnosti a transformace
        self.trans = [
            (0.0,    0.0,    0.0,  0.16, 0.0,    0.0, 0.01),
            (0.85,  0.04,  -0.04, 0.85, 0.0, 1.60, 0.85),
            (0.20, -0.26,   0.23, 0.22, 0.0, 1.60, 0.07),
            (-0.15, 0.28,   0.26, 0.24, 0.0, 0.44, 0.07)
        ]

    def compute(self):
        img = Image.new('L', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)
        x,y = 0.0, 0.0
        for _ in range(self.iterations):
            r = np.random.random()
            cumulative = 0.0
            for a,b,c,d,e,f,p in self.trans:
                cumulative += p
                if r <= cumulative:
                    x,y = a*x + b*y + e, c*x + d*y + f
                    break
            px = int(self.width*(x+2.1820)/4.8378)
            py = int(self.height - self.height*y/9.9983)
            draw.point((px,py), fill=0)
        return img

    def to_image(self):
        return self.compute()