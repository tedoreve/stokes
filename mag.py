import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
#matplotlib.use('Agg')
import matplotlib.path as mpath
from astropy.io import fits
from astropy import wcs
from astropy import units as u
import copy as cp
from astropy.tests import zmf as z
#from astropy import constants as con

def mag(file):
    head = []
    data = []
    for i in range(len(file)):
        cont = fits.open(file[i])
        head.append(cont[0].header)
        data.append(cont[0].data[0,:,:])#*z.conversion(cont_head['BMAJ'],cont_head['BMIN'])    
        cont.close()
 
    return head,data
    
def plot(data,head,contrast,name):
    l1 = head[1]['CRVAL1']+head[1]['CRPIX1']*head[1]['CDELT1']
    b1 = head[1]['CRVAL2']-head[1]['CRPIX2']*head[1]['CDELT2']
    l2 = head[1]['CRVAL1']-head[1]['CRPIX1']*head[1]['CDELT1']
    b2 = head[1]['CRVAL2']+head[1]['CRPIX2']*head[1]['CDELT2']
    result = []
    for i in range(4):
        result.append(np.nan_to_num(data[i]))
        result[i] = (result[i]-np.mean(result[i]))+np.mean(result[i])*contrast
    result=np.array(result)
    
    region = l1,l2,b1,b2 
    head[0]['CUNIT3']='m/s'
    x1,y1,x2,y2 = z.coo_box(head[0],region)
        
    plt.subplots() 
    plt.title(name)
    
    plt.imshow(np.log(result[0][0][y1:y2,x1:x2]),origin='lower',interpolation='nearest',extent=[l2,l1,b1,b2])
    plt.colorbar()
    l = np.linspace(l1,l2,data[1].shape[0])
    b = np.linspace(b1,b2,data[1].shape[0])
    x,y = np.meshgrid(l,b)

    plt.quiver(x,y,data[4]*np.cos(np.deg2rad(data[3])),data[4]*np.sin(np.deg2rad(data[3])))
    
    plt.grid()
    
if __name__=='__main__':
    file=['../data/VGPS_cont_MOS049.fits','../data/fitq28457.fits',           \
    '../data/fitu28457.fits','../data/fita28457.fits','../data/fitp28457.fits']
    head,data = mag(file)
    plot(data,head,1,'Magnetic Field')

