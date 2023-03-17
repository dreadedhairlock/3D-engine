import math
import numpy as np

class Proyeksi:
    def __init__(self, render):
        DEKAT = render.kamera.planar_dekat
        JAUH = render.kamera.planar_jauh
        KANAN = math.tan(render.kamera.fov_hor / 2)
        KIRI = -KANAN
        ATAS = math.tan(render.kamera.fov_ver / 2)
        BAWAH = -ATAS

        m00 = 2 / (KANAN - KIRI)
        m11 = 2 / (ATAS -BAWAH)
        m22 = (JAUH + DEKAT) / (JAUH - DEKAT)
        m32 = -2 * DEKAT * JAUH / (JAUH - DEKAT)
        self.proyeksi_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        HW, HH = render.SETENGAH_WIDTH, render.SETENGAH_HEIGHT
        self.matrix_ke_layar = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])