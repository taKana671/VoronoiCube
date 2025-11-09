# VoronoiCube

This repository was created to practice assigning different textures to each face of a cube.
I merged the textures for different faces into a large“atlas”texture and procedurally generated a 3D cube model, then have the UV coordinates of the cube point to the respective area in the texture.
The texture was generated from 3D Voronoi noise.Texture images are created using Python's Numpy.ndarray, and the Numpy.ndarray is converted into a texture.

Additionally, to learn about modifying UV coordinates, I repeatedly read the Panda3D manual and articles on the Community site. Thank you to all the mentors on the Community site for posting so many useful articles.

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


