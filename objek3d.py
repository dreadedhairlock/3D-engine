import pygame as py
from fungsi_matrix import *

from numba import njit

@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Objek3D:
    def __init__(self, render, titik2, muka):
        self.render = render
        # self.titik2 = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1),
        #                        (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        self.titik2 = np.array([np.array(v) for v in titik2])
        self.muka = np.array([np.array(muk) for muk in muka])
        # self.muka = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])

        self.font = py.font.SysFont('Arial', 30, bold=True)
        self.warna_muka = [(py.Color('orange'), muka) for muka in self.muka]
        self.gerak_flag, self.draw_axis = True, False
        self.label =''

    def draw(self):
        self.proyeksi_layar()
        self.gerak()

    def gerak(self):
        if self.gerak_flag:
            self.rotasi_y(py.time.get_ticks() % 0.005)

    def proyeksi_layar(self):
        titik2 = self.titik2 @ self.render.kamera.kamera_matrix()
        titik2 = titik2 @ self.render.proyeksi.proyeksi_matrix
        titik2 /= titik2[:, -1].reshape(-1, 1)
        titik2[(titik2 > 2) | (titik2 < -2)] = 0
        titik2 = titik2 @ self.render.proyeksi.matrix_ke_layar
        titik2 = titik2[:, :2]

        for index, warna_muka in enumerate(self.warna_muka):
            warna, muk = warna_muka
            poligon = titik2[muk]
            if not any_func(poligon, self.render.SETENGAH_WIDTH, self.render.SETENGAH_HEIGHT):
                py.draw.polygon(self.render.screen, warna, poligon, 1)
                if self.label:
                    teks = self.font.render(self.label[index], True, py.Color('white'))
                    self.render.screen.blit(teks, poligon[-1])

            if self.draw_axis:
                for titik in titik2:
                    if not any_func(titik, self.render.SETENGAH_WIDTH, self.render.SETENGAH_HEIGHT):
                        py.draw.circle(self.render.screen, py.Color('white'), titik, 2)

    def translasi(self, pos):
        self.titik2 = self.titik2 @ translasi(pos)

    def skala(self, scale_to):
        self.titik2 = self.titik2 @ skala(scale_to)

    def rotasi_x(self, angle):
        self.titik2 = self.titik2 @ rotasi_x(angle)

    def rotasi_y(self, angle):
        self.titik2 = self.titik2 @ rotasi_y(angle)

    def rotasi_z(self, angle):
        self.titik2 = self.titik2 @ rotasi_z(angle)

class Axis(Objek3D):
    def __init__(self, render):
            super().__init__(render)
            self.titik2 = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
            self.muka = np.array([(0,1), (0,2), (0, 3)])
            self.warna = [py.Color('red'), py.Color('blue'), py.Color('yellow')]
            self.warna_muka = [(warn, muk) for warn, muk in zip(self.warna, self.muka)]
            self.draw_axis = False
            self.label = 'XYZ'