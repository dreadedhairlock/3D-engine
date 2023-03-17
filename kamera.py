import pygame as py
from fungsi_matrix import *

class Kamera:
    def __init__(self, render, posisi):
        self.render = render
        self.posisi = np.array([*posisi, 1.0])
        self.maju = np.array([0, 0, 1, 1])
        self.atas = np.array([0, 1, 0, 1])
        self.kanan = np.array([1, 0, 0, 1])
        self.fov_hor = math.pi / 3
        self.fov_ver = self.fov_hor * (render.HEIGHT / render.WIDTH)
        self.planar_dekat = 0.1
        self.planar_jauh = 100
        self.speed_gerak = 0.06
        self.speed_rotasi = 0.01

    def kontrol(self):
        key = py.key.get_pressed()
        if key[py.K_a]:
            self.posisi -= self.kanan * self.speed_gerak
        if key[py.K_d]:
            self.posisi += self.kanan * self.speed_gerak
        if key[py.K_w]:
            self.posisi += self.maju * self.speed_gerak
        if key[py.K_s]:
            self.posisi -= self.maju * self.speed_gerak
        if key[py.K_q]:
            self.posisi += self.atas * self.speed_gerak
        if key[py.K_e]:
            self.posisi -= self.atas * self.speed_gerak

        if key[py.K_LEFT]:
            self.kamera_yaw(-self.speed_rotasi)
        if key[py.K_RIGHT]:
            self.kamera_yaw(self.speed_rotasi)
        if key[py.K_UP]:
            self.kamera_pitch(-self.speed_rotasi)
        if key[py.K_DOWN]:
            self.kamera_pitch(self.speed_rotasi)

    def kamera_yaw(self, sudut):
        rotasi = rotasi_y(sudut)
        self.maju = self.maju @ rotasi
        self.kanan = self.kanan @ rotasi
        self.atas = self.atas @ rotasi

    def kamera_pitch(self, sudut):
        rotasi = rotasi_x(sudut)
        self.maju = self.maju @ rotasi
        self.kanan = self.kanan @ rotasi
        self.atas = self.atas @ rotasi

    def translasi_matrix(self):
        x, y, z, w = self.posisi
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotasi_matrix(self):
        rx, ry, rz, w = self.kanan
        fx, fy, fz, w = self.maju
        ux, uy, uz, w = self.atas
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def kamera_matrix(self):
        return self.translasi_matrix() @ self.rotasi_matrix()