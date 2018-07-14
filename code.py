# -*- coding: utf-8 -*-

import numpy as np

import urllib

G = 6.67408*10**-11
MT = 5.9772*10**24
mu = G*MT
RT = 6371.*10**3

def metres(m):
    return m/RT
    
R = metres(RT + 20000*10**3)


def TLE_parser():
    satellites = list()
    
    f = urllib.urlopen("https://www.celestrak.com/NORAD/elements/supplemental/gps.txt")
    fp = f.read().splitlines()
    for i in range(0,len(fp),3):
        satellites.append([])
        '''0'''; satellites[i//3].append(fp[i][:-2]) #NOM !!!
        
        #LIGNE 1
        '''1''';satellites[i//3].append(fp[i+1][2:7])#NUMERO DE SATELLITE
        '''2''';satellites[i//3].append(fp[i+1][7])#CLASSIFICATION
        '''3''';satellites[i//3].append(fp[i+1][9:12])#ANNEE DE LANCEMENT
        '''4''';satellites[i//3].append(fp[i+1][11:14])#NUMERO DE LANCEMENT DANS L'ANNEE
        '''5''';satellites[i//3].append(fp[i+1][14:17])#IDENTIFIANT D'OBJET DU LANCEMENT
        '''6''';satellites[i//3].append(fp[i+1][18:20])#EPOQUE(ANNEE)
        '''7''';satellites[i//3].append(fp[i+1][20:32])#EPOQUE(JOUR DE L'ANNEE ET PORTION FRACTIONELLE DU JOUR)
        '''8''';satellites[i//3].append(fp[i+1][33:43])
        '''9''';satellites[i//3].append(fp[i+1][44:52])
        '''10''';satellites[i//3].append(fp[i+1][53:61])
        '''11''';satellites[i//3].append(fp[i+1][63])
        '''12''';satellites[i//3].append(fp[i+1][64:68])
        
        #LIGNE 2
        '''13''';satellites[i//3].append(fp[i+2][2:7])#NUMERO DE SATELLITE
        '''14''';satellites[i//3].append(float(fp[i+2][8:16]))#INCLINAISON
        '''15''';satellites[i//3].append(float(fp[i+2][17:25]))#LONGITUDE DU NOEUD DESCENDANT
        '''16''';satellites[i//3].append(str(fp[i+2][26:33]))#EXCENTRICITE
        '''17''';satellites[i//3].append(float(fp[i+2][34:42]))#ARGUMENT DU PERIASTRE
        '''18''';satellites[i//3].append(float(fp[i+2][43:51]))#ANOMALIE MOYENNE
        '''19''';satellites[i//3].append(float(fp[i+2][52:63]))#MOYEN MOUVEMENT
        '''20''';satellites[i//3].append(float(fp[i+2][64:68]))#NOMBRE DE REVOLUTIONS A L'EPOQUE DONNEE
    return satellites,fp


def kepler2card(src,i,omega):
    #i_, omega_ = np.rad2deg(i),np.rad2deg(omega)    
    i_, omega_ = np.deg2rad(omega), np.deg2rad(i)
    Ry = np.array([[np.cos(i_),0,np.sin(i_)],[0,1,0],[-np.sin(i_),0,np.cos(i_)]])
    Rz = np.array([[np.cos(omega_),-np.sin(omega_),0],[np.sin(omega_),np.cos(omega_),0],[0,0,1]])
    return src.dot(Ry).dot(Rz)
    

def affichage_terre():
    from mayavi import mlab
    from tvtk.tools import visual
    a = mlab.figure(1, bgcolor=(0.48, 0.48, 0.48), fgcolor=(0, 0, 0),
               size=(1000, 800))
               
    mlab.clf()
    visual.set_viewer(a)
    from mayavi.sources.builtin_surface import BuiltinSurface
    continents_src = BuiltinSurface(source='earth', name='Countries')
    continents_src.data_source.on_ratio = 2
    continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0))
    sphere = mlab.points3d(0, 0, 0, scale_mode='none',
                                    scale_factor=2,
                                    color=(0.67, 0.77, 0.93),
                                    resolution=50,
                                    opacity=0.7,
                                    name='Earth')
    sphere.actor.property.specular = 0.45
    sphere.actor.property.specular_power = 5
    sphere.actor.property.backface_culling = True
    def Arrow_From_A_to_B(x1, y1, z1, x2, y2, z2):
        ar1=visual.arrow(x=x1, y=y1, z=z1)
        ar1.length_cone=0.4
    
        arrow_length=np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
        ar1.actor.scale=[arrow_length, arrow_length, arrow_length]
        ar1.pos = ar1.pos/arrow_length
        ar1.axis = [x2-x1, y2-y1, z2-z1]
        #ix = mlab.points3d(2,0,0,mode='arrow') PLUS ELEGANT ??? 
        #http://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html ! POINTS3D !
        return ar1
    
    axX = Arrow_From_A_to_B(0, 0, 0, 1, 0, 0)
    axY = Arrow_From_A_to_B(0, 0, 0, 0, 1, 0)
    axZ = Arrow_From_A_to_B(0, 0, 0, 0, 0, 1)
    
    
    '''coords = kepler2card(np.array([1,0,0]),satellites[0][14],-satellites[0][15])
    sat1 = Arrow_From_A_to_B(0, 0, 0, coords[0], coords[1], coords[2])
    coords2 = kepler2card(np.array([1,0,0]),satellites[0][14],0)
    sat2 = Arrow_From_A_to_B(0, 0, 0, coords[0], coords[1], coords[2])
    '''
    
    theta = np.linspace(0, 2 * np.pi, 100)
    for i in range(len(satellites)):
        U = kepler2card(np.array([1,0,0]),-satellites[i][15],satellites[i][14])   
        N = kepler2card(np.array([0,0,1]),-satellites[i][15],satellites[i][14])   
    
    
        #U = kepler2card(np.array([1,0,0]),-82.1335,54.1115)   
        #N = kepler2card(np.array([0,0,1]),-82.1335,54.1115)         
        
        UN = np.cross(U,N)    
        
        #P = R*np.cos(theta)*U+R*np.sin(theta)*U.cross(N)
        x= R*np.cos(theta)*U[0]+R*np.sin(theta)*UN[0]
        y= R*np.cos(theta)*U[1]+R*np.sin(theta)*UN[1]
        z= R*np.cos(theta)*U[2]+R*np.sin(theta)*UN[2]    
        mlab.plot3d(x, y, z, color=(1, 1, 1),opacity=0.2, tube_radius=None)
    
    for i in range(len(satellites)):
        U = kepler2card(np.array([1,0,0]),-cosatellites[i][15],satellites[i][14])   
        N = kepler2card(np.array([0,0,1]),-satellites[i][15],satellites[i][14])   
    
    
        #U = kepler2card(np.array([1,0,0]),-82.1335,54.1115)   
        #N = kepler2card(np.array([0,0,1]),-82.1335,54.1115) 
        
        
        UN = np.cross(U,N)
        theta = np.deg2rad(satellites[i][18])*0
        n = satellites[i][18]
        d = ((mu**(1/3))/((2*n*np.pi/86400)**(2/3)))
        x= (d*np.cos(theta)*U[0]+d*np.sin(theta)*UN[0])*R
        y= (d*np.cos(theta)*U[1]+d*np.sin(theta)*UN[1])*R
        z= (d*np.cos(theta)*U[2]+d*np.sin(theta)*UN[2] )*R
           
        
        if(satellites[i][0].find("16")!=-1 or satellites[i][0].find("26")!=-1):
            points = mlab.points3d(x, y, z,scale_mode='none',scale_factor=0.1, color=(1, 0, 0))
         
        x= (d*np.cos(theta)*U[0]+d*np.sin(theta)*UN[0])
        y= (d*np.cos(theta)*U[1]+d*np.sin(theta)*UN[1])
        z= (d*np.cos(theta)*U[2]+d*np.sin(theta)*UN[2] )  
        
        if(satellites[i][0].find("16")!=-1 or satellites[i][0].find("26")!=-1):
            print(theta)
            points = mlab.points3d(x, y, z,scale_mode='none',scale_factor=0.1, color=(1, 0, 0))                       
    return n,d                 
###############################################################################
# Plot the equator and the tropiques
'''theta = np.linspace(0, 2 * np.pi, 100)
for angle in (- np.pi / 6, 0, np.pi / 6):
    x = np.cos(theta) * np.cos(angle)
    y = np.sin(theta) * np.cos(angle)
    z = np.ones_like(theta) * np.sin(angle)


    mlab.plot3d(x, y, z, color=(1, 1, 1),
                        opacity=0.2, tube_radius=None)
'''
#trajectoires satellites
'''
angle = 0
theta = np.linspace(0, 2 * np.pi, 100)
x = R*np.sin(theta) * np.cos(angle)
y = R*np.cos(theta) * np.cos(angle)
z = R*np.ones_like(theta) * np.sin(angle)
mlab.plot3d(x, y, z, color=(1, 1, 1), opacity=0.2, tube_radius=None)
#b=visual.Arrow(x=0,y=0,z=0, color=(1,0,0))
def Arrow_From_A_to_B(x1, y1, z1, x2, y2, z2):
    ar1=visual.arrow(x=x1, y=y1, z=z1)
    ar1.length_cone=0.4

    arrow_length=np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    ar1.actor.scale=[arrow_length, arrow_length, arrow_length]
    ar1.pos = ar1.pos/arrow_length
    ar1.axis = [x2-x1, y2-y1, z2-z1]
    #ix = mlab.points3d(2,0,0,mode='arrow') PLUS ELEGANT ??? 
    #http://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html ! POINTS3D !
    return ar1
    
axX = Arrow_From_A_to_B(0, 0, 0, 1, 0, 0)
axY = Arrow_From_A_to_B(0, 0, 0, 0, 1, 0)
axZ = Arrow_From_A_to_B(0, 0, 0, 0, 0, 1)
'''




'''
@mlab.show
@mlab.animate(delay=10)


def anim():
    """Animate the b1 box."""
    for i in range(5000):
        continents.actor.actor.orientation = [0,0,continents.actor.actor.orientation[2]+np.float64(0.3)]
        yield
#anim()
'''


if __name__ == '__main__':
    satellites, fp = TLE_parser()
    affichage_terre()

