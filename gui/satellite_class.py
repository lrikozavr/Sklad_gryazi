# satellite class


import numpy as np
import ephemeris_class as eph

from astropy.time import Time
from astropy import units as u
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy.coordinates import ITRS, AltAz

# https://pypi.org/project/sgp4/
from sgp4.api import Satrec
from sgp4.api import WGS72


class satellite:

    #
    #
    _sat = None
    _timestart = -1
    _timestop = -1
    _site = None
    _rsat = []
    _vsat = []

    satname = ''
    satnum = ''
    stdmag = 25
    priority = 0
    time = []
    rasc = []
    decl = []
    dtra = []
    dtde = []
    hang = []
    azim = []
    elev = []
    pang = []
    rang = []
    amag = []

    condition = -1

# ---------------------------------
    def __init__(self, tle, observtime, observloc):
        #
        # input
        #   tle         - 3-element array; 0 - satellite name,
        #                                  1 - first line of TLE 
        #                                  2 - second line of TLE 
        #   observtime  - two-element array of time (JD)
        #   observloc   - observer geocentric location (X, Y, Z in meters)
        #
        if len(tle[1]) > 0:
            self.satname = tle[0][2:]

        self._sat = Satrec.twoline2rv(tle[1], tle[2], WGS72)

        self._timestart = observtime[0]
        self._timestop = observtime[1]
        self._site = observloc
        self.satnum = self._sat.satnum

# ---------------------------------

# ---------------------------------
    def propagate(self, observtime):
        #
        # input
        #   observtime - time array (JD)
        #
        # output
        #   az       - satellite topocentric azimuth in degrees
        #   el       - satellite topocentric elevation in degrees
        #
        tt = Time(observtime, format='jd')
        e, self._rsat, self._vsat = self._sat.sgp4_array(tt.jd1, tt.jd2)
        
        teme_p = CartesianRepresentation(self._rsat[:, 0]*u.km,
                                         self._rsat[:, 1]*u.km,
                                         self._rsat[:, 2]*u.km)
        teme_v = CartesianDifferential(self._vsat[:, 0]*u.km/u.s,
                                    self._vsat[:, 1]*u.km/u.s,
                                    self._vsat[:, 2]*u.km/u.s)
        teme = TEME(teme_p.with_differentials(teme_v), obstime=tt)
        itrs_geo = teme.transform_to(ITRS(obstime=tt))
        topo_itrs_repr = itrs_geo.cartesian.without_differentials() \
                         - self._site.get_itrs(tt).cartesian
        itrs_topo = ITRS(topo_itrs_repr, obstime = tt, location=self._site)
        azel = itrs_topo.transform_to(AltAz(obstime=tt, location=self._site))
        
        del(teme_p, teme_v, teme, itrs_geo, topo_itrs_repr, itrs_topo, e) #warning: Is "azel" a copy?

        return azel.az.deg, azel.alt.deg
    
# ---------------------------------
    '''
# ---------------------------------
    def _sxp(self):
        # this function checks if satellite is LEO
        # returns boolean

        a1 = pow(self._sat.xke/self._sat.no_kozai, 2.0/3.0)
        r1 = np.cos(self._sat.inclo)
        temp = self._sat.j2/2 * 1.5 * (r1*r1 * 3.0 - 1.0) * pow( 1.0 - self._sat.ecco*self._sat.ecco, -1.5)
        del1 = temp / (a1*a1)
        ao = a1 * (1.0 - del1 * (1./3. + del1 * (del1 * 1.654320987654321 + 1.0)))
        delo = temp / (ao*ao)
        xnodp = self._sat.no_kozai / (delo + 1.0)

        return 2.0*np.pi/(xnodp * 1440.0) < 1.0/6.4
# ---------------------------------
    '''
# ---------------------------------
    def plan(self, timestep, obselev, stdmag, maglim, prior):
        #
        # input
        #   timestep   - value in seconds
        #   obselev    - two-element array of min and max elevation in degrees,
        #                where satellite can be observed
        #   stdmag     - satellite standard magnitude
        #   maglim     - min satellite magnitude which can be observed
        #   prior      - satellite observation priority (ascending)
        #
        # output
        #   result of this function is stored in "public" class members
        #   if nothing is computed then self.condition property is -1
        #   and procedure breaks, otherwise self.condition property is 1
        #

        self.priority = prior
        
        # compute time
        dt = timestep/86400.0
        epoch = self._sat.jdsatepoch + self._sat.jdsatepochF
        dts = np.trunc((self._timestart - epoch) / dt)
        tstart = epoch + dts*dt
        self.time = np.arange(tstart, self._timestop, dt)

        # get topocentric satellite azimuth/elevation during obsperiod
        self.azim, self.elev = self.propagate(self.time)

        # check if satellite is LEO
#        if not self._sxp():
#            self._clean()
#            return
            

        # exclude records where satellite elevation isn't in
        # min to max observation elevation
        idx = np.where((self.elev < obselev[0]) | (self.elev > obselev[1]))
        if np.size(idx) > 0:
            if np.size(idx) < np.size(self.time):
                self.time = np.delete(self.time, idx, axis=0)
                self._rsat = np.delete(self._rsat, idx, axis=0)
                self._vsat = np.delete(self._vsat, idx, axis=0)
                self.azim = np.delete(self.azim, idx, axis=0)
                self.elev = np.delete(self.elev, idx, axis=0)
            else:
                self._clean()
                return

        # get satellite to observer range
        tmploc = self._site.get_gcrs_posvel(Time(self.time, format='jd'))
        rloc = (tmploc[0] / u.m).get_xyz() / 1000
        del(tmploc)
        obsdif = self._rsat - rloc.transpose()
        self.rang = np.linalg.norm(obsdif, axis=1)

        # get phase angle
        rsol, solra, solde = eph.getsun(self.time)
        sundif = self._rsat - rsol.transpose()
        npdot = (obsdif * sundif).sum(axis=1)
        npnorm1 = np.linalg.norm(obsdif, axis=1)
        npnorm2 = np.linalg.norm(sundif, axis=1)
        self.pang = np.arccos(npdot / (npnorm1 * npnorm2))
        del(sundif, obsdif, npdot, npnorm1, npnorm2)

        # calculate satellite apparent magnitude
        if stdmag == None:
            self.amag = eph.approxmag(self.rang, np.radians(self.elev), self.pang)
        else:
            self.amag = eph.appmag(self.rang, np.radians(self.elev), stdmag, self.pang)
        self.stdmag = stdmag
        # exclude records where satellite magnitude is behind observation limit
        idx = np.where(self.amag > maglim)

        
        if np.size(idx) > 0:
            if np.size(idx) < np.size(self.time):
                self.time = np.delete(self.time, idx, axis=0)
                rloc = np.delete(rloc, idx, axis=1)
                self._rsat = np.delete(self._rsat, idx, axis=0)
                self._vsat = np.delete(self._vsat, idx, axis=0)
                self.azim = np.delete(self.azim, idx, axis=0)
                self.elev = np.delete(self.elev, idx, axis=0)
                self.rang = np.delete(self.rang, idx, axis=0)
                solra = np.delete(solra, idx, axis=0)
                solde = np.delete(solde, idx, axis=0)
                rsol = np.delete(rsol, idx, axis=1)
                self.pang = np.delete(self.pang, idx, axis=0)
                self.amag = np.delete(self.amag, idx, axis=0)
                return rloc, solra, solde, rsol, idx
            else:
                self._clean()
                return 0 #maybe, exception will help


        # compute satellite to moon angle
        rmoon, moonra, moonde, moonaz, moonel = eph.getmoon(Time(self.time, format='jd'), self._site)
        idx = eph.checksatmoonangle(rsol, solra, solde, rmoon, moonra, moonde, \
                                    self.azim, self.elev, moonaz, moonel, rloc)
        # exclude records where satellite magnitude is behind observation limit
        if np.size(idx) > 0:
            if np.size(idx) < np.size(self.time):
                self.time = np.delete(self.time, idx, axis=0)
                rloc = np.delete(rloc, idx, axis=1)
                self._rsat = np.delete(self._rsat, idx, axis=0)
                self._vsat = np.delete(self._vsat, idx, axis=0)
                self.azim = np.delete(self.azim, idx, axis=0)
                self.elev = np.delete(self.elev, idx, axis=0)
                self.rang = np.delete(self.rang, idx, axis=0)
                solra = np.delete(solra, idx, axis=0)
                solde = np.delete(solde, idx, axis=0)
                rsol = np.delete(rsol, idx, axis=1)
                self.pang = np.delete(self.pang, idx, axis=0)
                self.amag = np.delete(self.amag, idx, axis=0)
                return rloc, solra, solde, rsol, idx
            else:
                self._clean()
                return 0 #maybe, exception will help

        # check sat visibility
        vis = eph.sight(self._rsat, rsol.transpose(), self._sat.radiusearthkm)
        idx = np.where(vis == 0)
        if np.size(idx) > 0:
            if np.size(idx) < np.size(self.time):
                self.time = np.delete(self.time, idx, axis=0)
                rloc = np.delete(rloc, idx, axis=1)
                self._rsat = np.delete(self._rsat, idx, axis=0)
                self._vsat = np.delete(self._vsat, idx, axis=0)
                self.azim = np.delete(self.azim, idx, axis=0)
                self.elev = np.delete(self.elev, idx, axis=0)
                self.rang = np.delete(self.rang, idx, axis=0)
                solra = np.delete(solra, idx, axis=0)
                solde = np.delete(solde, idx, axis=0)
                rsol = np.delete(rsol, idx, axis=1)
                self.pang = np.delete(self.pang, idx, axis=0)
                self.amag = np.delete(self.amag, idx, axis=0)
                return rloc, solra, solde, rsol, idx
            else:
                self._clean()
                return 0 #maybe, exception will help

        # calculate satellite rates and hourangle
#        self.rasc, self.decl, satrho, satdrho, self.dtra, self.dtde = \
#                   eph.rvtradec(self._rsat/self._sat.radiusearthkm, \
#                                self._vsat*60.0/self._sat.radiusearthkm, \
#                                rloc/self._sat.radiusearthkm)
        self.rasc, self.decl, satrho, satdrho, self.dtra, self.dtde = \
                   eph.rvtradec(self._rsat, self._vsat*60.0, rloc)

        self.rasc = np.fmod(self.rasc.value, 2.0*np.pi)
        self.dtra = np.degrees(self.dtra)*3600
        self.dtde = np.degrees(self.dtde)*3600
        lst = Time(self.time, format='jd').sidereal_time('mean', self._site)
#        self.hang = np.fmod(lst.rad - self.rasc.value, 2.0*math.pi)
        self.hang = np.fmod(lst.rad - self.rasc, 2.0*np.pi)
        self.hang[self.hang < 0] += 2.0*np.pi

        del(rloc, solde, solra, rsol, lst)

        self.condition = 1

        #
# ---------------------------------

# ---------------------------------
    def _clean(self):
        self._rsat = []
        self._vsat = []

        self.time = []
        self.rasc = []
        self.decl = []
        self.dtra = []
        self.dtde = []
        self.hang = []
        self.azim = []
        self.elev = []
        self.pang = []
        self.rang = []
        self.amag = []
        
# ---------------------------------
        
