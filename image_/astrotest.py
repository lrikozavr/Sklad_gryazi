# astrometrica test

import numpy as np
from time import time

from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.visualization.wcsaxes import WCSAxes

from photutils.aperture import CircularAperture

from astrometrica import Astrometry

import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

# ======================================================================

fname = ['R2048554P.fit'] # Photometry 768x576
#fname = ['R1544516P.fit'] # Photometry 768x576

# Read fits
ffile = fits.open(f'{fname[0]}')

# ----------------------------------------------------------------------
# додаткові дані
# масштаб пікселя до поля зору, градуси (Photometry 768x576)
cdelt = [20.016518/3600, 20.016518/3600]

# цетр картинки в пікселях
crpix = [ffile[0].header['NAXIS1']/2, ffile[0].header['NAXIS2']/2]

# цетр картинки в градусах
coord = SkyCoord(f'{ffile[0].header["RA"]} {ffile[0].header["DEC"]}',
                 unit=("hourangle", "deg"), 
                 frame="icrs", 
                 obstime=f'{ffile[0].header["DATE-OBS"]}T{ffile[0].header["TIME-OBS"]}')
crval = [coord.ra.deg, coord.dec.deg]

# тип проєкції координат поля зору
ctype = ["RA---TAN", "DEC--TAN"]

# доповнити head (робити це при збереженні fits)
# https://www.aanda.org/articles/aa/full/2002/45/aah3860/aah3860.right.html
# вказати центр картинки
ffile[0].header['CRPIX1'] = crpix[0]
ffile[0].header['CRPIX2'] = crpix[1]
# вказати кутові розміри піксела
ffile[0].header['CDELT1'] = cdelt[0]
ffile[0].header['CDELT2'] = cdelt[1]
# вказати цент картинки в градусах
ffile[0].header['CRVAL1'] = crval[1]
ffile[0].header['CRVAL2'] = crval[0]
# вказати тип проєкції координат поля зору
ffile[0].header['CTYPE1'] = ctype[1]
ffile[0].header['CTYPE2'] = ctype[0]
# ----------------------------------------------------------------------

# Запустити клас Astrometry
ast = Astrometry(ffile)

t = time()
# детектуємо зірки
ast.detectStars(FWHM=7.0)
print('Detection', time()-t)

t = time()
# Качаємо каталожні зірки
ast.queryStars(magnitude=8.5, limit=25, aspect=1.5)
print('Query', time()-t)

t = time()
# Шукаємо відповідники
didx, qidx, ang, offs = ast.identificate(accuracy=0.01)
print('Identification', time()-t)
print(ang, offs)

# Draw data
ax = plt.subplot()
#ax = plt.subplot(projection=mtc.wcs)
ax.set_aspect('equal', 'box')
ax.grid(color='white', ls='dotted')

# plot fits image
ax.imshow(np.fliplr(np.flipud(ast.data)), vmin=np.median(ast.data),
          vmax=3*np.median(ast.data), cmap="Greys_r", origin='lower')

# виводимо положення детектованих зірок в піксельних координатах
ax.scatter(ast.detected_xy[:, 0], ast.detected_xy[:, 1],
           s=40, facecolors='none', edgecolors='g', marker='o')

# виводимо положення каталожних зірок в піксельних координатах
ax.scatter(ast.queried_xy[:, 1], ast.queried_xy[:, 0],
           s=40, facecolors='none', edgecolors='r', marker='o')

# виводимо положення ототожнених зірок в піксельних координатах
if len(didx) and len(qidx):
    ax.scatter(ast.detected_xy[didx, 0],
               ast.detected_xy[didx, 1],
               s=50, facecolors='none', edgecolors='g', marker='s')
    ax.scatter(ast.queried_xy[qidx, 1],
               ast.queried_xy[qidx, 0],
               s=50, facecolors='none', edgecolors='r', marker='s')
plt.show()
