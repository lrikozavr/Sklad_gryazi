import numpy as np

def matrix(angle,axes,round=12):
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

def horizontal_to_equatorial(A, h, fi, round = 12):
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

def equatorial_to_horizontal(hour, delta, fi, round = 12):
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

def cartesian_to_spherical(x, y, z, round = 12):
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

def spherical_to_cartesian(r, fi, tetha, round = 12):
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

    koef_fov = [2*np.sin(fov[0]/2.),2*np.sin(fov[1]/2.)]

    step = lambda x,i: (x - naxis[i]/2.)*orientation[i]*(koef_fov[i]/naxis[i])

    x = step(X,0)
    y = step(Y,1)

    z = np.sqrt(1 - np.pow(x,2) - np.pow(y,2))

    return x, y, z

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
    koef_fov = [2*np.sin(fov[0]/2.),2*np.sin(fov[1]/2.)]

    step = lambda x,i: x*(naxis[i]/koef_fov[i])*orientation[i] + naxis[i]/2.

    X = step(x,0)
    Y = step(y,1)

    return X, Y

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
    if(result < 0):
        result += np.pi*2
    return result
