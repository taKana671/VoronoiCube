# VoronoiCube

This repository was created to practice assigning different textures to each face of a cube.
I merged the textures for different faces into a large  “atlas”  texture and procedurally generated a 3D cube model, then modified the cube to have the UV coordinates point to the respective area in the texture.
The texture was generated from 3D Voronoi noise.Texture images were created as Python's Numpy.ndarray, and the Numpy.ndarray is converted into a texture.

Additionally, to learn about modifying UV coordinates, I repeatedly read the Panda3D manual and articles on the Community site. Thank you to all the mentors on the Community site for posting so many useful articles.

<img width="761" height="570" alt="Image" src="https://github.com/user-attachments/assets/e6c7e394-8d23-4344-927f-1367385f3522" />

# Requirements

* Panda3D 1.10.15
* Cython 3.1.6
* numpy 2.2.6
* opencv-contrib-python 4.12.0.88
* opencv-python 4.12.0.88

# Environment

* Python 3.13
* Windows11

# Building Cython code

### Clone this repository with submodule.
```
git clone --recursive https://github.com/taKana671/VoronoiCube.git
```

### Build cython code.
```
cd VoronoiCube
python setup.py build_ext --inplace
```
If the error like "ModuleNotFoundError: No module named ‘distutils’" occurs, install the setuptools.
```
pip install setuptools
```

# Usage

### voronoi_cube_demo

```
python voronoi_cube_demo.py [-h] (-f FILE | -n {voronoi,edges,rounded,transparent})

options:
  -h, --help            show this help message and exit
  -f, --file FILE       file_path
  -n, --noise {voronoi,edges,rounded,transparent}
```
When specifying a file, use one created beforehand with ```create_texture_atlas.py```.
When executed with noise specified, the atlas texture applied to the cube 3D model is converted from a Numpy.ndarray, but that atlas texture is also output as a file.
Drag the screen with your mouse to change the orientation of the cube.

### create_texture_atlas

```
from create_texture_atlas import TextureAtlasGenerator, output

# create an atlas texture image from voronoi noise.
generator = TextureAtlasGenerator.from_voronoi()
img = generator.generate_texture()
output(img, 'voronoi')

# create an atlas texture image from rounded voronoi noise.
generator = TextureAtlasGenerator.from_voronoi_round_edges()
img = generator.generate_texture()
output(img, 'rounded')

# create an atlas texture image from voronoi edges.
generator = TextureAtlasGenerator.from_voronoi_edges()
img = generator.generate_texture()
output(img, 'edges')
```


