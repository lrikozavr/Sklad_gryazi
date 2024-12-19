import numpy as np

def matrix(angle,axes,round=15):
    """
    Output rotation matrix that rotate vectors by an angle about the x-, y-, or z-axis, in three dimensions, using the right-hand rule

    see : https://en.wikipedia.org/wiki/Rotation_matrix

    Parameters
    ----------
    angle : rotation angle [radian]
    axes : ("x","y","z")
    round : value for `~np.round` module

    Output
    ------
        3D rotation matrix

    Example:
    --------
    >>> matrix(np.pi/2.,"x")
      array([[ 1.,  0.,  0.],
             [ 0.,  0., -1.],
             [ 0.,  1.,  0.]])
    """
    if(axes == "x"):
        return np.array([[1,0,0],
                         [0,np.cos(angle),-np.sin(angle)],
                         [0,np.sin(angle),np.cos(angle)]]).round(round)
    elif(axes == "y"):
        return np.array([[np.cos(angle),0,np.sin(angle)],
                         [0,1,0],
                         [-np.sin(angle),0,np.cos(angle)]]).round(round)
    elif(axes == "z"):
        return np.array([[np.cos(angle),-np.sin(angle),0],
                         [np.sin(angle),np.cos(angle),0],
                         [0,0,1]]).round(round)

def horizontal_to_equatorial(A, h, fi, round = 15):
    """
    These function are for converting `horizontal coordinates` to `equatorial coordinates`

    see : https://en.wikipedia.org/wiki/Astronomical_coordinate_systems
    
    Parameters
    ----------
    A : azimuth [radian]
    h : height (altitude) [radian]
    fi : observer's latitude [radian]
    round : value for `~np.round` module

    Output
    ------
        (hour angle, declination) [radian]

    Example:
    --------
    >>> import numpy as np
    >>> A, h, fi = np.pi, np.pi/3., np.pi/2.
    >>> H, d = horizontal_to_equatorial(A, h, fi)
    >>> H, d
    (np.float64(3.14159265359), np.float64(1.047197551196))
    >>> np.rad2deg([A, h, fi])
    array([180.,  60.,  90.])
    >>> np.rad2deg([H, d])
    array([180.,  60.])
    """
    #δ
    temp = np.sin(h).round(round)*np.sin(fi).round(round) - np.cos(A).round(round)*np.cos(h).round(round)*np.cos(fi).round(round)
    if(abs(temp) > 1.0):
        temp = np.round(temp)
    delta = np.asin(temp)
    #α
    hour = np.arctan2(np.sin(A).round(round),(np.sin(fi).round(round)*np.cos(A).round(round) + np.cos(fi).round(round)*np.tan(h).round(round)))

    if(hour < 0):
        hour += np.pi*2

    return np.round([hour, delta],round)

def equatorial_to_horizontal(hour, delta, fi, round = 15):
    """
    These function are for converting `equatorial coordinates` to `horizontal coordinates`

    see : https://en.wikipedia.org/wiki/Astronomical_coordinate_systems

    Parameters
    ----------
    hour : hour angle [radian]
    delta : declination [radian]
    fi : observer's latitude [radian]
    round : value for `~np.round` module

    Output
    ------
        (azimuth, height (altitude)) [radian]

    Example:
    --------
    >>> import numpy as np
    >>> hour, delta, fi = np.pi, np.pi/3., np.pi/2.
    >>> A, h = equatorial_to_horizontal(hour, delta, fi)
    >>> A, h
    (np.float64(3.14159265359), np.float64(1.047197551196))
    >>> np.rad2deg([hour, delta, fi])
    array([180.,  60.,  90.])
    >>> np.rad2deg([A, h])
    array([180.,  60.])
    """
    #A
    A = np.arctan2(np.sin(hour).round(round),(np.sin(fi).round(round)*np.cos(hour).round(round) - np.tan(delta).round(round)*np.cos(fi).round(round)))
    if(A < 0):
        A += np.pi*2
    #h
    temp = np.sin(fi).round(round)*np.sin(delta).round(round) + np.cos(fi).round(round)*np.cos(delta).round(round)*np.cos(hour).round(round)
    if(abs(temp) > 1):
        temp = np.round(temp)
    h = np.asin(temp)
    
    return np.round([A, h],round)

def cartesian_to_spherical(x, y, z, round = 15):
    """
    These function are for converting `cartesian coordinates` to `spherical coordinates`
    
    Parameters
    ----------
    x : [float]
    y : [float]
    z : [float]
    round : value for `~np.round` module
    
    Output
    ------
    (r, θ, φ) [radian]

    Example:
    --------
    >>> r, θ, φ = cartesian_to_spherical(0,1,0)
    >>> r, θ, φ
    (np.float64(1.0), np.float64(1.570796326795), np.float64(1.570796326795))
    """
    r = np.sqrt(np.pow(x,2) + np.pow(y,2) + np.pow(z,2))
    tetha = np.acos(z/r)
    fi = np.sign(y)*np.acos(x/(np.sqrt(np.pow(x,2) + np.pow(y,2))))

    return np.round([r, tetha, fi], round)

def spherical_to_cartesian(r, fi, tetha, round = 15):
    """
    These function are for converting `spherical coordinates` to `cartesian coordinates`
    
    Parameters
    ----------
    r : radius
    fi : [radian]
    tetha : [rafian]
    round : value for `~np.round` module

    Output
    ------
    (x, y, z)

    Example:
    --------
    >>> x, y, z = spherical_to_cartesian(1,np.pi/2.,np.pi/2.)
    >>> x, y, z
    (np.float64(0.0), np.float64(1.0), np.float64(0.0))
    """
    x = r*np.sin(tetha).round(round)*np.cos(fi).round(round)
    y = r*np.sin(tetha).round(round)*np.sin(fi).round(round)
    z = r*np.cos(tetha)

    return np.round([x, y, z],round)

def plane_to_cartesian(X,Y,naxis=(576, 768),fov=np.deg2rad((3,4)),orientation=(1,1)):
    """
    These function are for converting `2D plane of CCD camera frame` to `cartesian coordinates`, if z- axes was positive normal of frame

    Parameters
    ----------
    X : 1 axes of frame

    Y : 2 axes of frame

    naxis : size of frame CCD camera (axis X, axis Y)

    fov : field of view CCD camera (angle, angle)

    orientation : CCD camera orientation (X axis, Y axis). Example: (1, -1) * (X, Y) => (X, -Y) => (x, y)
    
    Output
    ------
        (x, y, z)

    Example:
    --------
    >>> x, y, z = plane_to_cartesian(576/2.,768/2.,naxis=(576,768))
    >>> x, y, z
    (np.float64(0.0), np.float64(0.0), np.float64(1.0))
    >>> x, y, z = plane_to_cartesian(500.,700.,naxis=(576,768),fov=np.deg2rad([3,4]))
    >>> x, y, z
    (np.float64(0.019269142504406627),
    np.float64(0.028719377494766423),
    np.float64(0.9994017698120501))

    """

    koef_fov = [2*np.tan(fov[0]/2.),2*np.tan(fov[1]/2.)]

    step = lambda x,i: (x - naxis[i]/2.)*orientation[i]*(koef_fov[i]/naxis[i])

    x = step(X,0)
    y = step(Y,1)

    z = np.sqrt(1 - np.pow(x,2) - np.pow(y,2))

    return np.array([x, y, z])

def cartesian_to_plane(x,y,naxis=(512, 768),fov=np.deg2rad((3,4)),orientation=(1,1)):
    """
    These function are for converting `cartesian coordinates` to `2D plane of CCD camera frame`, if z- axes was positive normal of frame

    Parameters
    ----------
    x : x axes value
    
    y : y axes value
    
    naxis : size of frame CCD camera (axis X, axis Y)

    fov : field of view CCD camera (angle, angle)

    orientation : CCD camera orientation (X axis, Y axis). Example: (1, -1) * (x, y) => (x, -y) => (X, Y)    

    Output
    ------
        (X, Y)

    Example:
    --------
    >>> x, y = 0.019269142504406627, 0.028719377494766423
    >>> X, Y = cartesian_to_plane(x, y, naxis=(576,768),fov=np.deg2rad([3,4]))
    >>> X, Y
    (np.float64(500.0), np.float64(700.0))

    """
    koef_fov = [2*np.tan(fov[0]/2.),2*np.tan(fov[1]/2.)]

    step = lambda x,i: x*(naxis[i]/koef_fov[i])*orientation[i] + naxis[i]/2.

    X = step(x,0)
    Y = step(y,1)

    return np.array([X, Y])

def hour_ra_(angle, siderial_time, local_longitude = 0):
    """
    These function are for converting `hour angle` (right ascension) to `right ascension` (hour angle)

    Parameters
    ----------
    angle : hour angle or right ascension [rad]
    siderial_time : Greenwich sidereal time [rad]
    local_longitude : observer's longitude [rad]

    Output
    ------
        right ascension or hour angle
    Example:
    --------
    >>> hour_ra_(np.pi/2,np.pi, np.pi/8.)
    1.9634954084936207

    """
    result = siderial_time + local_longitude - angle 
    if(isinstance(result,np.ndarray)):
        return np.where(result < 0, result + np.pi*2, result)
    if(result < 0):
        result += np.pi*2
    return result

######################################################################################

def stat(xy):
    mean, median, std = sigma_clipped_stats(xy)
    print("mean:\t", mean)
    print("median:\t", median)
    print("std:\t", std)
    return mean, median, std

######################################################################################

class ShiftFinder():
    
    def array_to_shift(self,xy_1,xy_2):
        # Функція яка обраховує зсув
        # Перше значення, це відстань
        # Друге значення, це варіація тангенсу кута у полярній системі координат
        return np.array([np.hypot(xy_1[:,0] - xy_2[:,0], xy_1[:,1] - xy_2[:,1]),
                        np.arctan2((xy_1[:,0] - xy_2[:,0]),(xy_1[:,1] - xy_2[:,1]))]).transpose()

    def __init__(self,xy_1: np.ndarray, xy_2: np.ndarray, N: int | None = None, gap_value: int = 1, accuracy: list = [0,0], aperture: list = [3,np.deg2rad(3)]):
        #
        self.xy_1 = xy_1
        self.xy_2 = xy_2
        #
        if(N is None):
            N = xy_1.shape[0]
        #
        if(N > xy_1.shape[0]):
            raise Exception("Number of unit (of base array), that must have oponent out of base array size\n Please decrease value of parameter N")
        #
        self.gap_value = gap_value
        self.accuracy = accuracy
        self.aperture = aperture
        #
        self.main_shift_array = np.zeros((N,xy_2.shape[0],2))
        #
        for i in range(0,N,1):
            self.main_shift_array[i,:] = self.array_to_shift(xy_1[i:i+1:1],xy_2)

    def operation_on_shift(self, main_shift: np.ndarray, array_of_shifts: np.ndarray, evaluate: str = "hypot", option: str = "min"):
        """
        Виводить індекс найближчого значення вектору зсуву з масиву відповідників
    
        Input
        -----
        main_shift : [radius, angle]
        array_of_shifts : array of [radius, angle]
        evaluate : {"hypot","sum","radius","angle"}
        option : {"min","sort"}
        
        Output
        ------
            Index
        """

        temp_shift = abs(array_of_shifts - main_shift)
        first_step = np.array([])
        if(evaluate == "hypot"):
            first_step = np.hypot(temp_shift[:,0],temp_shift[:,1])
        elif(evaluate == "sum"):
            first_step = np.sum(temp_shift,axis=1)
        elif(evaluate == "radius"):
            first_step = temp_shift[:,0]
        elif(evaluate == "angle"):
            first_step = temp_shift[:,1]
        else:
            raise Exception("Wrong [evaluate] parameter value, check descrintion for more info")
        #print("first step", first_step)

        second_step = np.array([])
        if(option == "min"):
            second_step = np.array([np.argmin(first_step)])
        elif(option == "sort"):
            second_step = np.argsort(first_step)[::-1]
        else:
            raise Exception("Wrong [option] parameter value, check description for more info")

        return second_step

    def check_window(self, shift: np.ndarray, array_shift: np.ndarray, accuracy: list | None = None, aperture: list | None = None):
        """
        Функція яка виводить індекси рядків масиву, які задовільняють умовам вікна ототожнення

        Input
        -----
        shift : [radius, angle]
        array_shift : array of [radius, angle]
        accuracy : percent shift of [radius, angle] as radius of searching window
        aperture : solid shift of [radius, angle] of searching window

        Output
        ------
        1D array of index 
        """

        if(accuracy is None):
            accuracy = self.accuracy
        if(aperture is None):
            aperture = self.aperture

        bool_temp = ((array_shift[:,0] < shift[0]*(1+accuracy[0]) + aperture[0]) & (array_shift[:,0] > shift[0]*(1-accuracy[0]) - aperture[0])) & ((array_shift[:,1] < shift[1]*(1+accuracy[1]) + aperture[1]) & (array_shift[:,1] > shift[1]*(1-accuracy[1]) - aperture[1]))
        if(bool_temp.any()):
            #return np.argwhere(bool_temp == True).flatten()
            # Масив індексів, значень які відповідають критеріям
            temp_array = np.argwhere(bool_temp == True).flatten()
            # Якщо один елемент у масиві, то виводимо значення одразу
            if(temp_array.shape[0] == 1):
                return temp_array 
            # Виводить відсортований по відстані масив індексів масиву індексів
            temp_index_array = self.operation_on_shift(shift,array_shift[temp_array],
                                           evaluate="sum",
                                           option="sort")

            return temp_array[temp_index_array]
            #return 
            
        else:
            return -1

    def one_by_one(self, step: int = 3, N: int | None = None, accuracy: list | None = None, aperture: list | None = None):
        """
        Алгоритм знаходження відповідників

        Input
        -----
        step : count of first failure loop

        Output
        ------
        np.ndarray indexes of oponent from sub array
        
        """
        if(N is None):
            N = self.main_shift_array.shape[0]
        elif(N > self.main_shift_array.shape[0]):
            raise Exception("Number of unit (of base array), that must have oponent out of base array size\n Please decrease value of parameter N")

        if(step > self.main_shift_array.shape[0]):
            raise Exception("Step value out of range")

        for i in range(0,step,1):
            for j in range(0,self.main_shift_array.shape[1],1):
                # Створюємо масив індексів, який повністю складається з -1, 
                # щоб надалі туди додавати лише значення індексів відповідників
                idx = np.full(N,fill_value = -1)
                # Додаємо значення індекса початкової відстані, 
                # яку використовуємо для порівняння з іншими
                # до масиву індексів, який виводимо
                idx[i] = j
                # та до масиву індексів, який робимо для збереження повторів
                index_array = np.array([j])
                # Флаг знаходження відповідників
                idx_flag = 1
                for deep in range(0,N,1):
                    # Пропускаємо коло, яке відповідає вже обраному індексу
                    if (deep == i):
                        continue
                    # Виводить індекси елементів іншого масиву, які відповідають умовам
                    index = self.check_window(self.main_shift_array[i,j],self.main_shift_array[deep],accuracy,aperture)
                    # Умова за якої можливий другий шанс
                    second_chanse_flag = (((deep > i) and (deep - index_array.shape[0] < self.gap_value)) or ((deep < i) and (deep - index_array.shape[0] + 1 < self.gap_value)))
                    # якщо не вдалося знайти відповідник(-и) виводимо -1
                    if(not isinstance(index,np.ndarray)):
                        #Другий шанс
                        if(second_chanse_flag):
                            continue
                        else:
                            idx_flag = -1
                            break

                    # Перевіряємо, чи не повторюються індекси
                    repeat_flag = -1
                    for i_i in index:
                        if(not i_i in index_array):
                            repeat_flag = 1
                            index_array = np.append(index_array,i_i)
                            idx[deep] = i_i
                            break
                    # Якщо повторюються і можливість другого шансу відсутня, то переходимо на наступне коло
                    if(repeat_flag == -1 and (not second_chanse_flag)):
                        idx_flag = -1
                        break
                
                if(idx_flag == 1):
                    return idx
        
        raise Exception("Something go wrong, increase accuracy")

    def shift_statistic(self,index_array: np.ndarray):
        """
        Виводить значення зсуву і середнє квадратичне відхилення

        Input
        -----
        index_array : array of index from self.one_by_one()

        Output
        ------
        mean, std
        """
        # Визначаємо елементи які мають відповідники
        xy_index = np.argwhere(index_array >= 0).flatten()
        #
        print("Count of stars with oponent: ",xy_index.shape[0])
        # 
        shift_temp = self.xy_1[xy_index] - self.xy_2[index_array[xy_index]]
        X_mean, X_median, X_std = sigma_clipped_stats(shift_temp[:,0])
        Y_mean, Y_median, Y_std = sigma_clipped_stats(shift_temp[:,1])
        
        return np.array([X_mean,Y_mean]),np.array([X_median, Y_median]),np.array([X_std, Y_std])

#
class PlaneConstant():
    
    def __init__(self, plane_param: np.ndarray | None = None, mod: str = "simple"):
        """
        plane_param : Параметри пластинки у вигляді [x,y]
        mod : [simple, medium or hard] Для більшості випадків, вистачає лише перших 3-х коефіціентів рівнянь Тернера
        """
        self.mod = mod
        if(plane_param is None):
            return None
        self.plane_param = plane_param
        print(f"{self.check(plane_param.shape[1])} parameters plane calibration")
        
    def check(self, length: int):
        p = 0
        if(length < 3):
            raise Exception("RIP. Should have at least 3 parameters or base coordinates")
        elif(length < 6):
            p = 3
            self.function = self.__plane_parameters_1__
        elif(length < 10):
            p=6
            if(self.mod == "simple"):
                self.function = self.__plane_parameters_1__
            else:
                self.function = self.__plane_parameters_2__
        elif(length < 15):
            p=10
            if(self.mod == "simple"):
                self.function = self.__plane_parameters_1__
            elif(self.mod == "medium"):
                self.function = self.__plane_parameters_2__
            else:    
                self.function = self.__plane_parameters_3__
        else:
            p=15
            if(self.mod == "simple"):
                self.function = self.__plane_parameters_1__
            elif(self.mod == "medium"):
                self.function = self.__plane_parameters_2__
            else:
                self.function = self.__plane_parameters_4__
        print("Plane constant calculation mod: ", self.mod)
        return p

    def __plane_parameters_1__(self,x,y):
        return np.array([x, y, np.ones(len(x))]).transpose()
    
    def __plane_parameters_2__(self,x,y):
        return np.array([x, y, np.ones(len(x)), 
                         np.pow(x,2), x*y, np.pow(y,2)]).transpose()
    
    def __plane_parameters_3__(self,x,y):
        return np.array([x, y, np.ones(len(x)), 
                         np.pow(x,2), x*y, np.pow(y,2), 
                         np.pow(x,3), np.pow(x,2)*y, x*np.pow(y,2), np.pow(y,3)]).transpose()

    def __plane_parameters_4__(self,x,y):
        return np.array([x, y, np.ones(len(x)), 
                         np.pow(x,2), x*y, np.pow(y,2), 
                         np.pow(x,3), np.pow(x,2)*y, x*np.pow(y,2), np.pow(y,3),
                         np.pow(x,4), np.pow(x,3)*y, np.pow(x,2)*np.pow(y,2), x*np.pow(y,3), np.pow(y,4)]).transpose()

    def plane_parameters(self, xy_1: np.ndarray, xy_2: np.ndarray):
        #
        print(f"{self.check(xy_1.shape[0])} parameters plane calibration")
        # xy_1 - coordinate from plane
        temp = xy_2 - xy_1

        Q = self.function(xy_1[:,0],xy_1[:,1])
        #print(Q)
        temp_plane = np.linalg.inv(Q.transpose() @ Q) @ Q.transpose()

        X_param = temp_plane @ temp[:,0]
        Y_param = temp_plane @ temp[:,1]
        
        self.plane_param =  np.array([X_param,Y_param])
    
    def real_coordinate(self, xy_1: np.ndarray):
        xy = np.zeros(xy_1.shape)
        
        if(hasattr(self,'function')):
            Q = self.function(xy_1[:,0],xy_1[:,1])
        else:
            raise Exception("""Function don't know about plane parameters set, please: 
initiate class with 'plane_param', or use one of this function first:
'check', 'plane_parameters'  """)    
        
        if(not hasattr(self,'plane_param')):
            raise Exception("""Function don't know about 'plane_param', please:
initiate class with 'plane_param', or use 'plane_parameters' first""")

        xy[:,0] = xy_1[:,0] + Q @ self.plane_param[0,:]
        xy[:,1] = xy_1[:,1] + Q @ self.plane_param[1,:]
        
        return xy

from astropy.coordinates import SkyCoord, Angle, EarthLocation, AltAz, HADec
from astropy.stats import sigma_clipped_stats
from astropy.time import Time
import astropy.units as u
from astropy.io import fits

from photutils.detection import DAOStarFinder
from photutils.psf import PSFPhotometry
from photutils.psf import CircularGaussianPRF 

from astroquery.vizier import Vizier

class PlateRecognize():

    def __init__(self, fits: fits, config: dict):
        self.config = config
        #
        self.data = fits[0].data
        self.header = fits[0].header
        #
        #self.center = SimpleNamespace()
        self.center = SkyCoord(f'{self.header["RA"]} {self.header["DEC"]}', 
                 unit=("hourangle","deg"), 
                 frame="icrs")
                 #obstime=f'{self.header["DATE-OBS"]}T{self.header["TIME-OBS"]}')
        # another way
        #self.observation_time.sidereal_time('apparent').radian
        self.local_sidereal_time = Angle(f'{self.header["TIME-SID"]} hours').to_value(u.rad)
        #
        self.location = EarthLocation(lon = config["location"]["lon"] * u.deg,lat = config["location"]["lat"] * u.deg, height = config["location"]["height"] * u.m)
        self.observation_time = Time(f'{self.header["DATE-OBS"]}T{self.header["TIME-OBS"]}', location=self.location)
        #
        self.rotation_matrix = self.rotation_matrix_func()
        #        
        self.stars = self.query_stars_coordinate(self.center,fov=config["FOV"], scale=config["scale"])
        self.plane_objects = self.detect_stars()       
    
    def rotation_matrix_func(self):        
        hour_angle = hour_ra_(self.center.ra.radian,self.local_sidereal_time)
        azimuth, altitude = equatorial_to_horizontal(hour_angle,self.center.dec.radian,np.deg2rad(self.config["location"]["lat"]))
        return matrix(-(np.pi/2.-altitude),"y") @ (
                            matrix(-azimuth,"z") @ matrix(-(np.pi/2.-np.deg2rad(self.config["location"]["lat"])),"y"))
        
    def rotation_matrix_alt(self):
        frame = AltAz(obstime=self.observation_time, location=self.location)
        altaz = self.center.transform_to(frame)
        return matrix(-(np.pi/2.-altaz.alt.radian),"y") @ (
                            matrix(-altaz.az.radian,"z") @ matrix(-(np.pi/2.-np.deg2rad(self.config["location"]["lat"])),"y"))

    def RADEC_to_PlaneXY(self,radec):
        # Перехід зі сферичної до декартової системи координат з множенням на матрицю повороту
        xyz = (self.rotation_matrix @ spherical_to_cartesian(1,hour_ra_(radec[:,0],self.local_sidereal_time),np.pi/2. - radec[:,1])).transpose()

        # Перехід від декартової сист. коорд. до координат площини кадру
        XY = cartesian_to_plane(xyz[:,0],xyz[:,1],naxis = (self.header["NAXIS1"],self.header["NAXIS2"]), fov=np.deg2rad(self.config["FOV"]))
        #
        return XY

    def PlaneXY_to_RADEC(self,XY):
        #
        xyz = (self.rotation_matrix.transpose() @ plane_to_cartesian(XY[:,0],XY[:,1],naxis = (self.header["NAXIS1"],self.header["NAXIS2"]),fov=np.deg2rad(self.config["FOV"]))).transpose()
        #
        temp = cartesian_to_spherical(xyz[:,0],xyz[:,1],xyz[:,2]).transpose()
        #
        RADEC = np.zeros((temp.shape[0],2))
        RADEC[:,1] = np.pi/2. - temp[:,1]
        RADEC[:,0] = hour_ra_(temp[:,2],self.local_sidereal_time)
        #
        return RADEC

    def query_stars_coordinate(self, center: SkyCoord, fov: tuple = (3.20264288, 4.27019051), 
                                catalog: str = "I/350/tyc2tdsc", mag: float = 8.5, scale: float = 2.):
        #Кидаємо запит до Vizier, щоб витягнути зірки з каталогу Tycho2, які мають яскравість менше 6 mag
        TYCHO2 = Vizier(catalog=catalog)
        # Критерій який скидує ліміт на кількість зірок 
        TYCHO2.ROW_LIMIT = -1
        # 
        result = TYCHO2.query_region(coordinates=center,
                                width=fov[1]*scale*u.deg,height=fov[0]*scale*u.deg,
                                column_filters={'BTmag': f'<{mag}'})

        return np.deg2rad(np.sort(result[0],order="BTmag")[["RAT","DET"]].tolist())

    def detect_stars(self, fwhm: float = 7.):
        # Get statistics
        #img = (img-np.min(img)).astype(np.uint16)
        mean, median, std = sigma_clipped_stats(self.data, sigma=3)
        #threshold = mean + (3. * std)
        threshold = std*6

        # Detect sources
        # https://photutils.readthedocs.io/en/2.0.0/user_guide/psf.html
        # maybe should pay attention to http://www.aspylib.com/
        FWHM = fwhm
        R = int(FWHM*4) // 2 + 1

        psf_model = CircularGaussianPRF(flux=mean*3, fwhm=FWHM)
        fit_shape = (R, R)
        finder = DAOStarFinder(threshold, FWHM)
        psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
                                aperture_radius=R)
        phot = psfphot(self.data)
        #Сортуємо по значенню яскравості
        phot = np.sort(phot, order = "flux_fit")[::-1]

        xy = [[rec['x_fit'], rec['y_fit']] for rec in phot if rec["flags"] == 0]

        return np.array(xy)
    
    def calibration(self, mod: int = 6, aperture: list = [2,np.deg2rad(2)]):
        """
        mod -- кількість опорних зірок; мінімальна кількість 3.
        """
        if(mod < 3):
            raise Exception("Value of 'mod' is too small for calibration. Check description")

        xy_2 = self.RADEC_to_PlaneXY(self.stars).transpose()
        xy_1 = self.plane_objects

        shift = ShiftFinder(xy_1,xy_2,N = xy_1.shape[0], gap_value = xy_1.shape[0] - mod, aperture=aperture)
        # Треба універсалізувати
        for i in range(mod - 1):
            if(i==mod - 2):
                raise Exception("Calibration failed") 
            try:
                self.plane_objects_index_array_of_stars = shift.one_by_one(xy_1.shape[0])
                break
            except:
                shift.gap_value += 1
                continue

        mean_shift, median_shift, std_shift = shift.shift_statistic(self.plane_objects_index_array_of_stars)

        real_XY_center = np.array([self.header["NAXIS1"]/2.,self.header["NAXIS2"]/2.]) - mean_shift

        new_center = self.PlaneXY_to_RADEC(np.array([real_XY_center]))
        #print(new_center)
        #print(new_center[:,0][0])
        new_center = SkyCoord(new_center[:,0][0], new_center[:,1][0], 
                 unit=(u.rad,u.rad), 
                 frame="icrs")
        #
        print("Agulare distance ", self.center.separation(new_center))
        print("Plane distance:")
        print("mean:\t", mean_shift)
        print("median:\t", median_shift)
        print("std:\t", std_shift)

        self.center = new_center
        self.rotation_matrix = self.rotation_matrix_func()

    def plane_constant(self):
        index_array = np.argwhere(self.plane_objects_index_array_of_stars >= 0).flatten()
        xy = self.plane_objects[index_array]
        real_xy = self.RADEC_to_PlaneXY(self.stars).transpose()[self.plane_objects_index_array_of_stars[index_array]]
        
        self.plane_constants = PlaneConstant()
        self.plane_constants.plane_parameters(xy,real_xy)
                
        print("Plane constants precision")
        stat(self.plane_constants.real_coordinate(xy) - real_xy)
        print("RADEC precision in angular seconds")
        stat(np.rad2deg(self.PlaneXY_to_RADEC(self.plane_constants.real_coordinate(xy)) - self.PlaneXY_to_RADEC(real_xy))*3600)

    def real_coordinate(self, xy_1: np.ndarray):
        
        if(hasattr(self,'plane_constants')):
            return self.PlaneXY_to_RADEC(self.plane_constants.real_coordinate(xy_1))
        else:
            raise Exception("""Function don't know about 'plane_constants', please:
use function 'plane_constant' first""")



