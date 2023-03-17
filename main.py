from objek3d import *
from kamera import *
from proyeksi import *
import pygame as py

# Kelas untuk menjalankan engine
class EngineRender:
    def __init__(self):
        py.init()
        self.RES = self.WIDTH, self.HEIGHT = 1200, 600
        self.SETENGAH_WIDTH, self.SETENGAH_HEIGHT = self.WIDTH //2, self.HEIGHT //2
        self.FPS= 60
        self.screen = py.display.set_mode(self.RES)
        self.clock = py.time.Clock()
        self.buat_objek() 

    def buat_objek(self):
        self.kamera = Kamera(self, [-5, 5, -50])
        self.proyeksi = Proyeksi(self)
        self.objek = self.get_objek('resource\girl OBJ.obj')
        self.objek.skala(10)
        # self.objek.translasi([0.2, 0.4, 0.2])
        # self.axis = Axis(self)
        # self.axis.translasi([0.7, 0.9, 0.7])
        # self.axis_dunia = Axis(self)
        # self.axis_dunia.gerak_flag = False
        # self.axis_dunia.skala(2.5)
        # self.axis_dunia.translasi([0.0001, 0.0001, 0.0001])
        # self.objek.rotasi_y(math.pi / 6)

    def get_objek(self, filename):
        titik, muka = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    titik.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f '):
                    muka_ = line.split()[1:]
                    muka.append([int(muk_.split('/')[0]) - 1 for muk_ in muka_])
        return Objek3D(self, titik, muka)

    # Menggambarkan yang ada di engine
    def draw(self):
        self.screen.fill(py.Color('darkslategray'))
        # self.axis_dunia.draw()
        # self.axis.draw()
        self.objek.draw()

    # Menjalankan engine
    def run(self):
        while True:
            self.draw()
            self.kamera.kontrol()
            [exit() for i in py.event.get() if i.type == py.QUIT] 
            py.display.set_caption(str(self.clock.get_fps()))
            py.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = EngineRender()
    app.run()
