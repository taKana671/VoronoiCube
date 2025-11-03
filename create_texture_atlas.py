from datetime import datetime
import random

import cv2
import numpy as np

from noise import VoronoiNoise, VoronoiEdges, VoronoiRoundEdges


def output(img, stem, parent='.', with_suffix=True):
    if with_suffix:
        now = datetime.now()
        stem = f'{stem}_{now.strftime("%Y%m%d%H%M%S")}'

    file_path = f"{parent}/{stem}.png"
    # file_name = f'{stem}_{now.strftime("%Y%m%d%H%M%S")}.{ext}'
    cv2.imwrite(file_path, img)


class Faces:

    def __init__(self, noise, size, grid):
        self.noise = noise
        self.size = size
        self.grid = grid

    def convert_arr(self, arr):
        if arr.ndim == 2:
            arr = arr.reshape(self.size, self.size, 3)
        else:
            arr = arr.reshape(self.size, self.size)
            arr = np.stack([arr] * 3, axis=2)

        return np.clip(arr * 255, a_min=0, a_max=255).astype(np.uint8)

    def create_top_bottom(self, z, t):
        arr = np.array(
            [self.noise(x + t, y + t, z + t)
                for y in np.linspace(0, self.grid, self.size)
                for x in np.linspace(0, self.grid, self.size)]
        )
        arr = self.convert_arr(arr)
        return arr

    def create_left_right(self, x, t):
        arr = np.array(
            [self.noise(x + t, y + t, z + t)
                for z in np.linspace(0, self.grid, self.size)
                for y in np.linspace(0, self.grid, self.size)]
        )
        arr = self.convert_arr(arr)
        return arr

    def create_forward_back(self, y, t):
        arr = np.array(
            [self.noise(x + t, y + t, z + t)
                for z in np.linspace(0, self.grid, self.size)
                for x in np.linspace(0, self.grid, self.size)]
        )
        arr = self.convert_arr(arr)
        return arr

    def output(self, img):
        name = self.__class__.__name__.lower()
        output(img, name)


class Bottom(Faces):

    def generate_image(self, t=0):
        img = self.create_top_bottom(z=self.grid, t=t)
        return img


class Top(Faces):

    def generate_image(self, t=0):
        img = self.create_top_bottom(z=0, t=t)
        img = img[:, ::-1]
        img = np.rot90(img, 2)
        return img


class Back(Faces):

    def generate_image(self, t=0):
        img = self.create_forward_back(y=0, t=t)
        return img


class Forward(Faces):

    def generate_image(self, t=0):
        img = self.create_forward_back(y=self.grid, t=t)
        img = img[:, ::-1]
        return img


class Left(Faces):

    def generate_image(self, t=0):
        img = self.create_left_right(x=0, t=t)
        img = img[:, ::-1]
        return img


class Right(Faces):

    def generate_image(self, t=0):
        img = self.create_left_right(x=self.grid, t=t)
        return img


class TextureAtlasGenerator:

    def __init__(self, noise, grid=4, size=256):
        self.noise = noise
        self.grid = grid
        self.size = size

    def generate_texture(self, t=0):
        faces = [Back, Forward, Left, Right, Bottom, Top]
        bg_img = np.zeros((self.size * 2, self.size * 4, 3), dtype=np.uint8)
        w = h = 0

        for i, face in enumerate(faces):
            face_creator = face(self.noise, self.size, self.grid)
            img = face_creator.generate_image(t)
            # face_creator.output(img)

            h = i // 4 * self.size
            w = i % 4 * self.size
            bg_img[h: h + self.size, w: w + self.size] = img

        # Flipping bg_img by numpy slice like below causes
        # 'TypeError: Texture.set_ram_image() requires a contiguous buffer'.
        # bg_img = bg_img[::-1]
        bg_img = cv2.flip(bg_img, 0)
        output(bg_img, 'atras')
        return bg_img

    @classmethod
    def from_voronoi(cls, grid=4, size=256):
        voronoi = VoronoiNoise()
        image_generator = cls(voronoi.voronoi3, grid, size)
        return image_generator

    @classmethod
    def from_voronoi_edges(cls, grid=4, size=256):
        voronoi = VoronoiEdges()
        image_generator = cls(voronoi.vmix3, grid, size)
        return image_generator

    @classmethod
    def from_voronoi_round_edges(cls, grid=4, size=256):
        voronoi = VoronoiRoundEdges()
        image_generator = cls(voronoi.vmix3_round, grid, size)
        return image_generator

    @classmethod
    def from_transparent_round_edges(cls, grid=4, size=256):
        voronoi = VoronoiRoundEdges()
        func = lambda x, y, z: voronoi.vmix1(voronoi.voronoi_round_edge3(x, y, z, tp=20), 0.0, 1.0)
        image_generator = cls(func, grid, size)
        return image_generator


if __name__ == '__main__':
    tex_atlas = TextureAtlasGenerator.from_transparent_round_edges()
    t = random.uniform(0, 1000)
    tex_atlas.generate_texture(t)