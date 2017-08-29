import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
#matplotlib.use('Agg')
import matplotlib.path as mpath
from astropy.io import fits
from astropy import wcs
from astropy import units as u
import copy as cp
import zmf as z
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
    for i in range(len(data)):
        result.append(np.nan_to_num(data[i]))
        result[i] = (result[i]-np.mean(result[i]))+np.mean(result[i])*contrast
    result=np.array(result)
    
    region = 48.7,49.7,-1.0,0 
    head[0]['CUNIT3']='m/s'
    x1,y1,x2,y2 = z.coo_box(head[0],region)
        
    plt.subplots() 
    plt.title(name)
    plt.xlabel('l (deg)')
    plt.ylabel('b (deg)')
    p=data[4]/data[5]
    plt.imshow(np.log10(result[0][0][y1:y2,x1:x2]),origin='lower',interpolation='nearest',extent=[49.7,48.7,-1.0,0])
#    plt.imshow(p,origin='lower',interpolation='nearest',extent=[l2,l1,b1,b2])      
    cbar = plt.colorbar()
    cbar.set_label('log(T/K)')
    l = np.linspace(l2,l1,data[1].shape[0])
    b = np.linspace(b1,b2,data[1].shape[0])
    x,y = np.meshgrid(l,b)
    
#    plt.quiver(x,y,p*np.cos(np.deg2rad(data[3])),p*np.sin(np.deg2rad(data[3])),scale=0.04,color='w')
    
#    plt.grid()
#    plt.close()
#    plt.imshow(data[4])
    return result
    
if __name__=='__main__':
    file=['../data/VGPS_cont_MOS049.fits','../data/fitq28271.fits',           \
    '../data/fitu28271.fits','../data/fita28271.fits','../data/fitp28271.fits',\
    '../data/fits1259.fits']
    head,data = mag(file)
    data[4] = data[4]-data[5]*0.007
    for i in data[4]:
        for j in i:
            if j < 0:
                y=np.where(data[4] == j)[0][0]
                x=np.where(data[4] == j)[1][0]
                data[4][y,x]=0
    for i in data[5]:
        for j in i:
            if j < 12540:
                y=np.where(data[5] == j)[0][0]
                x=np.where(data[5] == j)[1][0]
                data[5][y,x]=np.inf
    p=plot(data,head,1,'1420 MHz continuum')

