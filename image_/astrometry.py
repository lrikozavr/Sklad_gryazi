from astropy.io import fits
import numpy as np

fname = ['R2048554P.fit','R1544516P.fit']
# Read fits
ffile = fits.open(f'{fname[0]}')

config = {
    "location": {
        "lon" : 23.954290051419513,
        "lat" : 49.91760760673526,
        "height" : 100
    },
    "FOV": (3.20264288, 4.27019051),
    "scale": 3
}

from support import PlateRecognize

plane = PlateRecognize(ffile,config)
# Встановлюємо нове, правильне, значення центру
for i in range(4):
    plane.calibration(mod = 6, aperture=[5,np.deg2rad(3)])
# Рахуємо константи кадру
plane.plane_constant(mod="medium")


def grid(func, shape = (576,768), n = 50):
    x = np.linspace(0,shape[0],n)
    y = np.linspace(0,shape[1],n)
    xv, yv = np.meshgrid(x,y)

    grid_xy = np.append(xv.flatten(),yv.flatten()).reshape(2,n*n).transpose()
    new_grid_xy = func(grid_xy)

    new_xv = new_grid_xy.transpose()[0,:].reshape(n,n)
    new_yv = new_grid_xy.transpose()[1,:].reshape(n,n)

    return new_xv, new_yv

new_xv, new_yv = grid(plane.plane_constants.real_coordinate)

import matplotlib.pyplot as plt
from photutils.aperture import CircularAperture
# Draw data
stars = plane.RADEC_to_PlaneXY(plane.stars).transpose()
plt.imshow(plane.data, cmap="Greys_r")
# Проекція зірок на кадр
_ = CircularAperture(stars, r=12.0).plot(color="g")
#
_ = CircularAperture(plane.RADEC_to_PlaneXY(plane.stars).transpose()[plane.plane_objects_index_array_of_stars[np.argwhere(plane.plane_objects_index_array_of_stars >= 0).flatten()]], r=12.0).plot(color="r")
# Об'єкти на кадрі, які знайшов лагоритм
_ = CircularAperture(plane.plane_objects, r=10.0).plot(color="b")
# Врахування констант кадру для об'єктів які знайшов алгоритм
_ = CircularAperture(plane.plane_constants.real_coordinate(plane.plane_objects), r=10.0).plot(color="y")


plt.plot(new_xv, new_yv, marker='o', markersize=1, color='pink', linestyle='none')
plt.xlim((0,576))
plt.ylim((0,768))

#plt.colorbar()
plt.show()