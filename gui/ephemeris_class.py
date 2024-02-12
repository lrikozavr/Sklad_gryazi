# ephemeris class
# contains common math functions for computing
# positions of observer, satellite, Sun and Moon
#


import math
import numpy as np

from astropy.time import Time
import astropy.coordinates
from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz, get_body
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy.coordinates import ITRS
from astropy.coordinates import Angle

from sgp4.api import Satrec
from sgp4.api import WGS72

# =================================
# Constants
#
raanearth = 7.2921150e-5 # earth rotational speed in rads/sec
sm = 1e-8
one_sec = 1.0/86400.0

# =================================


# ---------------------------------
#  this procedure computes topocentric right-ascension declination with
#  position and velocity vectors. uses velocity vector to find the
#  solution of singular cases.
#
#  author        : david vallado                  719-573-2600   22 jun 2002
#
#  inputs          description                              range / units
#    satpos        -  satellite position [N, 3] array               er
#    satvel        -  velocity [N, 3] array                         er/tu
#    locpos        -  site position [3, N] array                    er
#
#  outputs       :
#    rho         - satellite range [N] array                        er
#    ra          - satellite right ascension [N] array              rad
#    de          - satellite declination [N] array                  rad
#    drho        - satellite range rate [N] array                   er/tu
#    dra         - satellite ascension rate [N] array               rad/tu
#    dde         - satellite declination rate [N] array             rad/tu
#
#  references    :
#    vallado       2013, 260, alg 26
#  Python adapted:
#    R. Nogach     2023
# ---------------------------------
def rvtradec(satpos=[], satvel=[], locpos=[]):

    latgc = np.arcsin(locpos[:, 2]/np.linalg.norm(locpos))
    earthrate = np.asarray([0.0, 0.0, raanearth])
    vs = np.cross(earthrate, locpos.transpose())
    rhov = satpos-locpos.transpose()
    drhov = satvel-vs*np.cos(latgc)

    rho = np.linalg.norm(rhov, axis=1)
    temp = np.array(np.sqrt(rhov[:, 0] * rhov[:, 0] + rhov[:, 1] * rhov[:, 1]))
    small = np.where(temp < sm)[0]
    big = np.where(temp >= sm)[0]
    if np.size(small):
        temp1 = np.sqrt(drhov[small, 0] * drhov[small, 0] + drhov[small, 1] * drhov[small, 1])
        tra = np.arctan2(drhov[small, 1] / temp1, drhov[small, 0] / temp1)
    if np.size(big):
        tra = np.arctan2(rhov[big, 1] / temp[big], rhov[big, 0] / temp[big])
#    idx = np.where(tra < 0)
#    if np.size(idx[0]) > 0:
#        tra[idx[0]] += 2.0*np.pi*u.rad
    tra += 2.0*np.pi*u.rad

    tde = np.arcsin(rhov[:, 2] / rho)
    temp1 = -rhov[:, 1] * rhov[:, 1] - rhov[:, 0] * rhov[:, 0]
    drho = (rhov*drhov).sum(axis=1) / rho
    big = np.where(np.fabs(temp1) > sm)[0]
    small = np.where(np.fabs(temp1) <= sm)[0]
    dtrtasc = np.zeros(np.size(temp1))
    if np.size(big):
        dtrtasc[big] = (drhov[big, 0] * rhov[big, 1] - drhov[big, 1] * rhov[big, 0]) / temp1
    if np.size(small):
        dtrtasc[small] = 0.0

    big = np.where(np.fabs(temp) > sm)[0]
    small = np.where(np.fabs(temp) <= sm)[0]
    dtdecl = np.zeros(np.size(temp))
    if np.size(big):
        dtdecl[big] = (drhov[:, 2] - drho * np.sin(tde)) / temp
    if np.size(small):
        dtdecl[small] = 0.0

    del(latgc, vs, rhov, drhov, temp, small, big, temp1)

    return tra, tde, rho, drho, dtrtasc, dtdecl

# ---------------------------------

# ---------------------------------
#  this procedure finds satellite's visibility.  
#
#  inputs          description                               range / units
#    rsat           - satellite position [N, 3] array                km
#    rsun	    - solar position [N, 3] array                    km
#    earthradius    -                                                km
#
#  outputs       :
#    value          - visibility [N] array          0 - not visible, 1 - visible
#
#  references    :
#    Vallado, Fundamentals of astrodynamics and applications
#  Python adapted:
#    R. Nogach     2023
# ---------------------------------
def sight(rsat, rsun, earthradius):

    v1 = rsat
    v2 = rsun
    v1n = np.linalg.norm(v1)
    v2n = np.linalg.norm(v2)
    v12 = (v1*v2).sum(axis=1)

    res = np.zeros(np.size(v12))
    
    taumin = (pow(v1n, 2)-v12)/(pow(v1n, 2) + pow(v2n, 2) - 2*v12)
    idx1 = np.where((taumin < 0.0) & (taumin > 1.0))
    if np.size(idx1) != 0:
        res[idx1] = 1
    else:
        idx2 = np.where((taumin >= 0.0) & (taumin <= 1.0))
        if np.size(idx2) != 0:
            ctau = ((1-taumin)*pow(v1n, 2) + v12*taumin)/pow(earthradius, 2)
            idx1 = np.where(ctau >= 1.0)
            if np.size(idx1) != 0:
                res[idx1] = 1
            del(ctau)

    del(v1, v2, v1n, v2n, v12, taumin, idx1, idx2)

    return res

# ---------------------------------

# ---------------------------------
#  this procedure computes topocentric solar position
#  regarding to observer position at given observation time
#
#  inputs          description                    range / units
#    obstime        - observing time                      JD (array of JD)
#
#  outputs
#    rsol           - solar gcrs position                 km (xyz)
#    ra             - solar gcrs right ascension          rad
#    de             - solar gcrs declination              rad
# ---------------------------------
def getsun(obstime=None):

    sol = get_body('sun', Time(obstime, format='jd'))
    ra = sol.ra.rad
    de = sol.dec.rad
    rsol = (sol.cartesian*u.au.to(u.km)/u.au).get_xyz()

    del(sol)
    
    return rsol, ra, de

# ---------------------------------

# ---------------------------------
#  this function computes time limits
#  for observation session
#
#  inputs          description                    range / units
#    obsdate        - date/time of session                array of JD
#                     if empty, computation
#                     for current date +1
#    obsloc         - observer position                   astropy's EartLocation object
#    MaxSunElev     - sun's topocentric elevation         deg
#
#  outputs
#    tlim           - time [2] array                      JD
# ---------------------------------
def getsessiontlim(obsdate=None, obsloc=None, MaxSunElev=0):

    if obsdate == None:
        t = Time(location=obsloc).now().jd
    else:
        t = Time(obsdate, format='jd').jd

    tlim = Time(np.arange(t, t+1.0, one_sec), format='jd')

#    loclim = AltAz(obstime=Time(tlim, format='jd'), location=obsloc)
    loclim = AltAz(obstime=tlim, location=obsloc)
    sol = get_body('sun', tlim).itrs.transform_to(loclim)
    idx = np.where(sol.alt.deg < MaxSunElev)
    t0 = tlim[idx[0][0]-1].jd
    t1 = tlim[idx[0][-1]+1].jd

    del(sol, idx, loclim, tlim)
    
    return [t0, t1]
# ---------------------------------

# ---------------------------------
#  this procedure computes topocentric lunar position
#  regarding to observer position at given observation time
#
#  inputs          description                       range / units
#    obstime        - observing time                         JD
#
#  outputs
#    rmoon          - lunar gcrs position [3, N] array       km (xyz)
#    ra             - lunar gcrs right ascension [N] array   rad
#    de             - lunar gcrs declination [N] array       rad
#    az             - lunar topocentric azimuth              deg
#    el             - lunar topocentric elevation            deg
# ---------------------------------
def getmoon(obstime, obsloc):

    moon = get_body('moon', Time(obstime, format='jd'))
    ra = moon.ra.rad
    de = moon.dec.rad
    rmoon = (moon.cartesian*u.au.to(u.km)/u.au).get_xyz()
    moonlim = moon.transform_to(AltAz(obstime=obstime, location=obsloc)).altaz
    az = moonlim.az.deg
    el = moonlim.alt.deg

    del(moon, moonlim)
    
    return rmoon, ra, de, az, el

# ---------------------------------

# ---------------------------------
#  this function computes moon illumination percents
#  and checks satellite to moon angle:
#  illumination range       acceptable angle (deg)
#        0 - 25                  10
#       25 - 50                  15
#       50 - 75                  20
#       75 - 100                 25
#
#  inputs          description                                range / units
#    rsol           - solar position [3, N] array                     km
#    solra          - solar right ascension [N] array                 rad
#    solde          - solar declination [N] array                     rad
#    rmoon          - lunar position [3, N] array                     km
#    moonra         - lunar right ascension [N] array                 rad
#    moonde         - lunar declination [N] array                     rad
#    az             - satellite topocentric azimuth [N] array         deg
#    el             - satellite topocentric elevation [N] array       deg
#    azm            - lunar topocentric azimuth [N] array             deg
#    elm            - lunar topocentric elevation [N] array           deg
#    rloc           - satellite position [3, N] array                 km
#
#  outputs
#    denied         - indices of denied satellite to moon angle        
# ---------------------------------
def checksatmoonangle(rsol, solra, solde, rmoon, moonra, moonde, az, el, azm, elm, rloc):

    cospsi = np.sin(solde)*np.sin(moonde)+np.cos(solde)*np.cos(moonde)*np.cos(solra-moonra)
    sinpsi = np.sin(np.arccos(cospsi))
    locsun = rloc-rsol
    locmoon = rloc-rmoon
    soldist = np.linalg.norm(locsun)
    moondist = np.linalg.norm(locmoon)
    tani = (soldist*sinpsi)/(moondist-soldist*cospsi)
    mill = np.mean(0.5*(1.0+np.cos(np.arctan(tani)))*100.0)
    if (mill > 0.0) & (mill <= 25.0):
        mang = 10.0
    if (mill > 25.0) & (mill <= 50.0):
        mang = 15.0
    if (mill > 50.0) & (mill <= 75.0):
        mang = 20.0
    if (mill > 75.0) & (mill <= 100.0):
        mang = 25.0
    v1 = np.array([np.cos(np.radians(elm))*np.cos(np.radians(azm)),
          np.cos(np.radians(elm))*np.sin(np.radians(azm)),
          np.sin(np.radians(elm))])
    v2 = np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),
          np.cos(np.radians(el))*np.sin(np.radians(az)),
          np.sin(np.radians(el))])
    npdot = (v1.transpose()*v2.transpose()).sum(axis=1)
    angle = np.degrees(np.arccos(npdot/(np.linalg.norm(v1)*np.linalg.norm(v2))))

    denied = np.where(angle < mang)

    del(cospsi, sinpsi, locsun, locmoon, soldist, moondist, tani, mill, v1, v2, npdot, angle)

    return denied

# ---------------------------------

# ---------------------------------
#  this function computes approximate magnitude of satellite
#  based on satellite range, elevation and solar phase angle
#  when standard magnitude is unknown
#
#  inputs          description                     range / units
#    rang           - satellite range                      km
#    elev           - satellite elevation                  rad
#    phang          - solar phase angle                    rad
#
#  local
#    X              - atmospheric extinction
#
#  output
#    apmag          - approximate magnitude of satellite   stellar mag
#
#  reference
#    Schmalzel - The feasibility and application of observing
#                small LEO satellites with amateur telescopes
# ---------------------------------
def approxmag(rang, elev, phang):

    msun = -26.75
    mag = 10.0
    diff = 100.0

    Lc = 1.0
    alb = np.sqrt(0.175)
    k = 0.17
    rng = rang*1000.0
    sixpi = np.pi*6.0
    sinpa = np.sin(phang)
    cospa = np.cos(phang)
    A = rng/alb
    B = np.sqrt(sixpi / (sinpa + (np.pi-phang)*cospa))
    secelev = 1.0/np.cos(np.pi/2.0 - elev)

    while (abs(diff) > 0.001):
        Lc_calc = pow(10.0, (msun-mag)/5.0) * A * B
        diff = Lc - Lc_calc
        mag -= (diff/Lc_calc)

    X = secelev * (1.0 - 0.0012 * (secelev*secelev - 1.0))

    apmag = mag - k*X - 2.0

    del(rng, A, B, X)
    
    return apmag

# ---------------------------------

# ---------------------------------
#  this function computes apparent magnitude of satellite
#  based on satellite range, elevation, solar phase angle
#  and standard magnitude
#
#  inputs          description                                  range / units
#    rang           - satellite range                                   km
#    elev           - satellite elevation                               rad
#    phang          - solar phase angle                                 rad
#
#  local
#    X              - atmospheric extinction
#
#  output
#    mag            - apparent magnitude of satellite                   stellar mag
#                     atmospheric extinction is taken into account
#
#  reference
#    Schmalzel - The feasibility and application of observing
#                small LEO satellites with amateur telescopes
# ---------------------------------
def appmag(rang, elev, stdmag, phang):

    fracil = (1.0 + np.cos(phang))/2.0
    secelev = 1.0/np.cos(np.pi/2.0 - elev)

    mag = (stdmag - 15.75 + 2.5 * np.log10(rang * rang / fracil)) \
           - 0.17*(secelev * (1.0 - 0.0012 * (pow(secelev, 2) - 1.0)))

    del(fracil, secelev)

    return mag

# ---------------------------------

# ---------------------------------
#  this function computes "standard" magnitude of satellite
#  based on satellite approximate shape area
#
#  inputs          description                                  range / units
#    lmin           - satellite minimum length                          m
#    lmax           - satellite maximum length                          m
#    dmt            - satellite diameter or width                       m
#
#  output
#    mag            - "standard" magnitude of satellite                 stellar mag
#
#  reference
#    Schmalzel - The feasibility and application of observing
#                small LEO satellites with amateur telescopes
# ---------------------------------
def getstdmag(lmin, lmax, dmt):

    Msun = -26.75
    alb = 0.175
    rang = 1e6
    pa = 0
    psi = np.sin(pa) + (np.pi - pa)*np.cos(pa)
    B = rang / np.sqrt(alb) * np.sqrt(6.0 * np.pi / psi)
    area = 1.0

    if (lmin != 0 and lmax == 0 and dmt == 0):
        area = lmin
    if (lmin != 0 and lmax != 0 and dmt == 0 and lmin == lmax):
        area = lmin
    if (lmin != 0 and lmax != 0 and dmt != 0 and lmin == lmax):
        area = np.sqrt(4.0*lmin*dmt/np.pi)
    if (lmin != 0 and lmax == 0 and dmt != 0):
        area = np.sqrt(4.0*lmin*dmt/np.pi)
    if (lmin != 0 and lmax != 0 and dmt != 0 and lmax > lmin):
        area = np.sqrt(2.0*(lmax*dmt+lmin*dmt)/np.pi)

    #if area > 0:
    mag = Msun-5.0*np.log10(area/B)
    return mag
# ---------------------------------------------------------
