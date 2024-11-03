#

import numpy as np

from astropy.io import fits
from astropy.stats import sigma_clipped_stats

from photutils.aperture import CircularAperture
from photutils.detection import DAOStarFinder
from photutils.psf import PSFPhotometry
from photutils.psf import CircularGaussianPRF

import matplotlib.pyplot as plt


fname = ['R2233018P.fit', 'R1948360P.fit', 
         'R2128554P.fit', '_0001.fit',
         'R2104061P.fit']

# Read fits
ffile = fits.open(fname[1])
data = ffile[0].data.transpose()
head = ffile[0].header

# Get statistics
data = (data-np.min(data)).astype(np.uint16)
mean, median, std = sigma_clipped_stats(data, sigma=3)
threshold = median + (3. * std)
print(mean, median, std, threshold)
#data = (data-np.min(data)).astype(np.uint16)

# Detect sources
# https://photutils.readthedocs.io/en/2.0.0/user_guide/psf.html
# maybe should pay attention to http://www.aspylib.com/
FWHM = 5.
R = int(FWHM*4) // 2 + 1

psf_model = CircularGaussianPRF(flux=mean*3, fwhm=FWHM)
fit_shape = (R, R)
finder = DAOStarFinder(std*6, FWHM)
psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
                        aperture_radius=R)
phot = psfphot(data)
print(phot[('id', 'x_fit', 'y_fit', 'flux_fit')])

xy = [[rec['x_fit'], rec['y_fit']] for rec in phot if rec["flags"] == 0]

# Draw data
plt.imshow(data, vmin=np.median(data), cmap="Greys_r")
_ = CircularAperture(xy, r=10.0).plot(color="y")
plt.colorbar()
plt.show()
