# astrometry functions

import numpy as np
from itertools import combinations
from time import time
from functools import reduce

from astropy.io import fits
from astropy.stats import sigma_clipped_stats

from photutils.detection import DAOStarFinder
from photutils.psf import PSFPhotometry
from photutils.psf import CircularGaussianPRF

from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord

import astropy.units as u

from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales, skycoord_to_pixel

# ===================================================================
class Astrometry():
    def __init__(self, fitsobj: fits):

        self.head = fitsobj[0].header
        self.data = fitsobj[0].data
        #
        self.wcs = WCS(self.head)

# ----------------------------------------------------------------------

    def queryStars(self,
                   magnitude: float = 8.5,
                   limit: int = -1,
                   aspect: float = 2.):
        # Координати центру
        coord = SkyCoord(f'{self.head["RA"]} {self.head["DEC"]}', 
                         unit=("hourangle", "deg"), 
                         frame="icrs", 
                         obstime=f'{self.head["DATE-OBS"]}T{self.head["TIME-OBS"]}')

        # Кидаємо запит до Vizier, щоб витягнути зірки з каталогу Tycho2,
        # які мають яскравість менше self.minmag і відсортовані за спаданням яскравості
        TYCHO2 = Vizier(columns=["*", "+BTmag"], catalog="I/350/tyc2tdsc")
        # Критерій який скидує ліміт на кількість зірок 
        TYCHO2.ROW_LIMIT = limit
        # обчислюємо радіус для запиту
        r = np.hypot(self.head['CRPIX1']*self.head['CDELT1'],
                     self.head['CRPIX2']*self.head['CDELT2'])*aspect
        # скачуємо каталожні зірки в полі зору FOV*aspect
        self.queried = TYCHO2.query_region(coordinates=coord,
                                           radius=r*u.deg,
                                           column_filters={'BTmag': f'<{magnitude}'})
        # формуємо структуру з каталожних координат
        self.queried_radec = SkyCoord(ra = self.queried[0]["RAT"],
                                      dec = self.queried[0]["DET"],
                                      unit=("deg", "deg"))
        # переводимо небесні координати в пікселі
        self.queried_xy = np.asarray(skycoord_to_pixel(self.queried_radec,
                                                       self.wcs)).transpose()
        self.queried_radec = np.array([self.queried[0]["RAT"],
                                       self.queried[0]["DET"]]).T
        
# ----------------------------------------------------------------------

    def detectStars(self, FWHM: float = 7.):
        # Get statistics
        img = (self.data-np.min(self.data)).astype(np.uint16)
        img = np.fliplr(np.flipud(img))
        mean, median, std = sigma_clipped_stats(img, sigma=3)
        threshold = 6. * std
        #threshold = mean + (3. * std)
#        threshold = median + (3. * std)

        # Detect sources
        R = int(FWHM*4) // 2 + 1

        psf_model = CircularGaussianPRF(flux=mean*3, fwhm=FWHM)
        #psf_model = CircularGaussianPRF(flux=median*3, fwhm=FWHM)
        #psf_model = CircularGaussianPRF(flux=std*3, fwhm=FWHM)
        fit_shape = (R, R)
        finder = DAOStarFinder(threshold, FWHM)
        psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
                                aperture_radius=R)
        phot = psfphot(img)
        #Сортуємо по значенню яскравості
        phot = np.sort(phot, order = "flux_fit")[::-1]

        self.detected_xy = np.array([[rec['x_fit'], rec['y_fit']] for rec in phot if rec["flags"] == 0])
        self.detected_radec = self.wcs.all_pix2world(self.detected_xy, 0)

# ----------------------------------------------------------------------

    def _construct(self, opt):
        # Create combinatorial list of detected stars array indices
        if opt == 'detected':
            lim = self.detected_xy.shape[0]
            comb = np.array(list(combinations(np.linspace(0, lim-1, lim,
                                                          dtype=np.uint32), 3)))
            triangles = self.detected_xy[comb]
        else:
            lim = self.queried_xy.shape[0]
            comb = np.array(list(combinations(np.linspace(0, lim-1, lim,
                                                          dtype=np.uint32), 3)))
            # Create array of triangles
            triangles = self.queried_xy[comb]

        # 1) compute triangles centroid
        ctr = np.mean(triangles, axis=1)
        # 2) subtract centroid from triangle
        sub = [triangles[i]-c for i, c in enumerate(ctr)]
        # 3) compute length of centered edges
        edges = np.linalg.norm(sub, axis=2)
        # 4) sort them and get indices
        pnts = np.argsort(edges)
        edges = np.sort(edges)
        comb = np.array([t[pnts[i]] for i, t in enumerate(comb)])

        return comb, edges

# ----------------------------------------------------------------------

    def _match(self, accuracy: float = 0.01):
        # construct triangles for detected stars
        det_comb, det_edge = self._construct('detected')
        # construct triangles for queried stars
        que_comb, que_edge = self._construct('queried')

        matched_d = []
        matched_q = []
        # define tolarence
        tol = que_edge*accuracy

        for i, p in enumerate(det_edge):
            diff = np.abs(que_edge-p)

            idx0 = np.argwhere(diff[:, 0] < tol[:, 0])
            idx1 = np.argwhere(diff[:, 1] < tol[:, 1])
            idx2 = np.argwhere(diff[:, 2] < tol[:, 2])
            idx = reduce(np.intersect1d, (idx0, idx1, idx2))
            if idx.any():
                matched_d.append(det_comb[i])
                matched_q.append(que_comb[idx])
            
        return np.array(matched_d), np.array(matched_q)

# ----------------------------------------------------------------------

    def _final(self, d_idx, q_idx):
        fin = []
        # fits image center
        ctr = np.array([self.head['CRPIX1'], self.head['CRPIX2']])
        for ki, di in enumerate(d_idx):
            # detected triangle
            td = self.detected_xy[di]
            for qi in q_idx[ki]:
                # queried triangle
                tq = np.fliplr(self.queried_xy[qi])
                # compute angle
                a = td[1]-td[0]
                b = tq[1]-tq[0]
                # cosine
                ca = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
                if ca < 0:
                    # two triangles are mirrored
                    continue
                # sine
                sa = (1-ca**2)**0.5
                # rotation matrix
                rotm = np.array([[ca, sa], [-sa, ca]])
                # rotate queried triangle around image center
                for i, s in enumerate(tq):
                    tq[i] = (s-ctr).dot(rotm)+ctr
                # compute average offset between detected and queried triangles
                diff = tq-td
                off = np.mean(diff, axis=0)
                # store data if offset std is small
                k = np.mean(np.std(diff, axis=0))
                if k < 1:
                    fin.append([di, qi, np.arccos(ca), off.tolist()])

        # combine detected indices
        didx = np.unique([p[0] for p in fin])
        # combine queried indices
        qidx = np.unique([p[1] for p in fin])
        # get angle statistics
        ang = [p[2] for p in fin]
        angstat = [np.mean(ang), np.std(ang)]
        # get offset statistics
        off = [p[3] for p in fin]
        offstat = [np.mean(off, axis=0), np.std(off, axis=0)]

        return didx, qidx, angstat, offstat

# ----------------------------------------------------------------------

    def identificate(self, accuracy: float = 0.01):
        d_idx, q_idx = self._match(accuracy)

        didx, qidx, ang, offs = self._final(d_idx, q_idx)

        return didx, qidx, ang, offs

# ===================================================================
