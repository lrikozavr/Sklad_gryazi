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


######################################################################################

# Функція яка обраховує зсув
# Перше значення, це відстань
# Друге значення, це варіація тангенсу кута у полярній системі координат
shift = lambda xy_1, xy_2: [np.hypot(xy_1[0] - xy_2[0], xy_1[1] - xy_2[1]),np.arctan2((xy_1[0] - xy_2[0]),(xy_1[1] - xy_2[1]))]

#  
def step(ra: np.ndarray, array_ra: np.ndarray,accuracy: list,aperture: list):
    """
    Функція яка виводить індекси рядків масиву, які задовільняють умовам вікна ототожнення

    Input
    -----
    ra : [radius, angle]
    array_ra : array of [radius, angle]
    accuracy : percent shift of [radius, angle] as radius of searching window
    aperture : solid shift of [radius, angle] of searching window

    Output
    ------
    1D array of index 
    """
    bool_temp = ((array_ra[:,0] < ra[0]*(1+accuracy[0]) + aperture[0]) & (array_ra[:,0] > ra[0]*(1-accuracy[0]) - aperture[0])) & ((array_ra[:,1] < ra[1]*(1+accuracy[1]) + aperture[1]) & (array_ra[:,1] > ra[1]*(1-accuracy[1]) - aperture[1]))
    if(bool_temp.any()):
        return np.argwhere(bool_temp == True).flatten()
    else:
        return -1

def cycle(ra,pair,i,j,N,gap_value,acc,ap):
    """
    Рекурсивна функція пошуку відповідників

    Input
    -----
    ra : [radius, angle]
    pair : 3D array like (index of base array, index of sub array,[radius, angle])
    i : index of base array
    j : array of used index of xub array
    N : number of unit (of base array), that must have oponent
    gap_value : number of unit (of base array) that may not have oponent
    acc : (accuracy) percent of [radius, angle] as radius of searching window
    ap : (aperture) solid [radius, angle] of searching window

    Output
    ------
    if not have oponent => -1

    else                => [index of oponents] 
    """
    
    index = step(ra,pair[i],acc,ap)
    
    #якщо не вдалося знайти відповідник(-и) виводимо -1
    if(not isinstance(index,np.ndarray)):
        #Другий шанс
        if((not i >= N-1) and (i - len(j) < gap_value)):
            temp = cycle(ra,pair,i+1,j,N,gap_value,acc,ap)
            if(isinstance(temp,np.ndarray)):
                return np.append([-1],temp)
                    
        return -1

    # якщо відповідники знайшлися, 
    # але наступне коло виходить 
    # за межі кількості відповідників N
    # виводимо перший елемент
    if(i == N-1):
        #print(index)
        for i_i in index:
            if(not i_i in j):
                return np.array(i_i)
        return -1

    indx = []
    idx = -1
    for i_i in index:
        # якщо виникає повтор то переходимо до наступного індексу
        if(i_i in j):
            continue
        # додаємо індекс до переліку вже використаних індексів
        j_j = [i_i]
        j_j.extend(j)
        # j_j можна вважати набором індексів (це на потім)
        #print(j_j)
        # 1
        # якщо індексів ототожнених рядків на цьому колі більше ніж 1
        # і ми маємо можливість запустити позанаступне коло
        # то ви запускаємо коло i + 1
        if(isinstance(indx,np.ndarray) and not i >= N-2):
            j_j.extend(indx)
            temp = cycle(ra,pair,i+2,j_j,N,gap_value,acc,ap)
            #мом
            if(not isinstance(temp,np.ndarray)):
                return -1
            indx = np.append(indx,temp)
            idx = i_i
            break
        # запускає пошук відповідників на наступне коло 
        # збільшуючи і на 1
        indx = cycle(ra,pair,i+1,j_j,N,gap_value,acc,ap)
        # якщо невдалося знайти відповідник
        if(not isinstance(indx,np.ndarray)):
            # 1
            # пробуємо перевірити гіпотезу, 
            # що на наступному колі є відповідник 
            # під індексом який ми вже зайняли на цьому колі 
            indx = step(ra,np.array([pair[i+1][i_i]]),acc,ap)
            if(not isinstance(indx,np.ndarray)):
                return -1
            #continue
            # 1
            # якщо нам вдається, то ми кладемо в indx значення індексу цього рядку
            else:
                indx = np.array([i_i])
        else:
            idx = i_i
            break

    if(idx == -1):
        return -1

    return np.append([idx],indx)

def one(xy_1,xy_2, N, gap_value = 0, accuracy = [0.1,0.1], aperture=[0,0]):
    """
    Алгоритм пошуку відповідників за лінійного значення зсуву

    Input
    -----
    xy_1 : base coordinate array
    xy_2 :  sub coordinate array
    N : number of unit (of base array), that must have oponent
    gap_value : number of unit (of base array) that may not have oponent
    acc : (accuracy) percent of [radius, angle] as radius of searching window
    ap : (aperture) solid [radius, angle] of searching window

    Output
    ------
       idx - np.array() of index from sub array
    """
    n = len(xy_2)
    
    # розраховуємо відстані одразу для N перших точок точок базового масиву
    pair = np.zeros((N,n,2))
    for i in range(0,N,1):
        for j in range(0,n,1):
            pair[i,j] = shift(xy_1[i],xy_2[j])
    
    # запускаємо рекурсію відштовхуючись від значення відстані для першої точки
    idx = []
    for j in range(0,n,1):    
        # point 2
        temp_idx = cycle(pair[0,j],pair,1,[j],N,gap_value,accuracy,aperture)
        # у випадку невдалого пошуку, беремо наступне значення відстані
        if (not isinstance(temp_idx,np.ndarray)):
            continue
        idx = np.append([np.int64(j)],temp_idx)
        break
    # якщо алгоритм так і не знайшов відповідників, то пишемо
    if(not isinstance(idx,np.ndarray)):
        print("Something go wrong. Increse accuracy")
    # і виводимо -1
    return idx