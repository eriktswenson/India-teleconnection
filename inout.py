
import numpy as np
from sklearn.linear_model import LinearRegression
from netCDF4 import Dataset as nc
import matplotlib.pyplot as plt

def readDTUV(domx1=[120,280,-15,20],domx2=[50,120,-15,5],domy=[55,95,5,35],nyrs=38):

# Read in JJAS 850 hPa U,V (m/s) with one specified domain
    f = nc('UV.nc')
    lonall = f.variables['lon'][:].data; nlonall = len(lonall)
    latall = f.variables['lat'][:].data; nlatall = len(latall)
    ilony = np.where((lonall>=domy[0])&(lonall<=domy[1]))[0]; lony = lonall[ilony]; nlony = len(ilony)
    ilaty = np.where((latall>=domy[2])&(latall<=domy[3]))[0]; laty = latall[ilaty]; nlaty = len(ilaty)
    ilonsy = np.reshape(np.repeat(ilony,nlaty),(-1,nlaty)).T
    ilatsy = np.reshape(np.repeat(ilaty,nlony),(nlaty,-1))
    U = f.variables['Uobs'][:].data[:,:,:]
    V = f.variables['Vobs'][:].data[:,:,:]
    Y1 = np.reshape(U[:,ilatsy,ilonsy],(nyrs,-1)).T
    Y2 = np.reshape(V[:,ilatsy,ilonsy],(nyrs,-1)).T
    Y = np.vstack((Y1,Y2))
    U = f.variables['Uctl'][:].data[:,:,:]
    V = f.variables['Vctl'][:].data[:,:,:]
    Y1 = np.reshape(U[:,ilatsy,ilonsy],(nyrs,-1)).T
    Y2 = np.reshape(V[:,ilatsy,ilonsy],(nyrs,-1)).T
    Yctl = np.vstack((Y1,Y2))
    U = f.variables['Uhtg'][:].data[:,:,:]
    V = f.variables['Vhtg'][:].data[:,:,:]
    Y1 = np.reshape(U[:,ilatsy,ilonsy],(nyrs,-1)).T
    Y2 = np.reshape(V[:,ilatsy,ilonsy],(nyrs,-1)).T
    Yhtg = np.vstack((Y1,Y2))
    f.close()

# Read in JJAS verticall-integrated heating (K/day) with two specified domains
    f = nc('DT.nc')
    lonall = f.variables['lon'][:].data; nlonall = len(lonall)
    latall = f.variables['lat'][:].data; nlatall = len(latall)
    ilonx1 = np.where((lonall>=domx1[0])&(lonall<=domx1[1]))[0]; lonx1 = lonall[ilonx1]; nlonx1 = len(ilonx1)
    ilatx1 = np.where((latall>=domx1[2])&(latall<=domx1[3]))[0]; latx1 = latall[ilatx1]; nlatx1 = len(ilatx1)
    ilonsx1 = np.reshape(np.repeat(ilonx1,nlatx1),(-1,nlatx1)).T
    ilatsx1 = np.reshape(np.repeat(ilatx1,nlonx1),(nlatx1,-1))
    ilonx2 = np.where((lonall>=domx2[0])&(lonall<=domx2[1]))[0]; lonx2 = lonall[ilonx2]; nlonx2 = len(ilonx2)
    ilatx2 = np.where((latall>=domx2[2])&(latall<=domx2[3]))[0]; latx2 = latall[ilatx2]; nlatx2 = len(ilatx2)
    ilonsx2 = np.reshape(np.repeat(ilonx2,nlatx2),(-1,nlatx2)).T
    ilatsx2 = np.reshape(np.repeat(ilatx2,nlonx2),(nlatx2,-1))
    DT = f.variables['DTobs'][:].data[:,:,:]
    X1 = np.reshape(DT[:,ilatsx1,ilonsx1],(nyrs,-1)).T
    X2 = np.reshape(DT[:,ilatsx2,ilonsx2],(nyrs,-1)).T
    DT = f.variables['DTctl'][:].data[:,:,:]
    Xctl1 = np.reshape(DT[:,ilatsx1,ilonsx1],(nyrs,-1)).T
    Xctl2 = np.reshape(DT[:,ilatsx2,ilonsx2],(nyrs,-1)).T
    DT = f.variables['DThtg'][:].data[:,:,:]
    Xhtg1 = np.reshape(DT[:,ilatsx1,ilonsx1],(nyrs,-1)).T
    Xhtg2 = np.reshape(DT[:,ilatsx2,ilonsx2],(nyrs,-1)).T
    DT = f.variables['DTadd'][:].data[:,:,:]
    Xadd1 = np.reshape(DT[:,ilatsx1,ilonsx1],(nyrs,-1)).T
    Xadd2 = np.reshape(DT[:,ilatsx2,ilonsx2],(nyrs,-1)).T
    f.close()

# Subtract time mean
    X1 = X1 - np.reshape(np.repeat(np.mean(X1,1),nyrs),(nlonx1*nlatx1,nyrs))
    X2 = X2 - np.reshape(np.repeat(np.mean(X2,1),nyrs),(nlonx2*nlatx2,nyrs))
    Xctl1 = Xctl1 - np.reshape(np.repeat(np.mean(Xctl1,1),nyrs),(nlonx1*nlatx1,nyrs))
    Xctl2 = Xctl2 - np.reshape(np.repeat(np.mean(Xctl2,1),nyrs),(nlonx2*nlatx2,nyrs))
    Xhtg1 = Xhtg1 - np.reshape(np.repeat(np.mean(Xhtg1,1),nyrs),(nlonx1*nlatx1,nyrs))
    Xhtg2 = Xhtg2 - np.reshape(np.repeat(np.mean(Xhtg2,1),nyrs),(nlonx2*nlatx2,nyrs))
    Y = Y - np.reshape(np.repeat(np.mean(Y,1),nyrs),(nlony*nlaty*2,nyrs))
    Yctl = Yctl - np.reshape(np.repeat(np.mean(Yctl,1),nyrs),(nlony*nlaty*2,nyrs))
    Yhtg = Yhtg - np.reshape(np.repeat(np.mean(Yhtg,1),nyrs),(nlony*nlaty*2,nyrs))

# Compute latitude weighting
    gx1 = np.sqrt(np.cos(np.reshape(latx1,(nlatx1,1))*(np.pi/180.0)))
    gx1 = np.reshape(np.repeat(gx1,nlonx1,axis=1),(-1,1))
    gx2 = np.sqrt(np.cos(np.reshape(latx2,(nlatx2,1))*(np.pi/180.0)))
    gx2 = np.reshape(np.repeat(gx2,nlonx2,axis=1),(-1,1))
    gy = np.sqrt(np.cos(np.reshape(laty,(nlaty,1))*(np.pi/180.0)))
    gy = np.reshape(np.repeat(gy,nlony,axis=1),(-1,1))
    gy = np.vstack((gy,gy))

# Spatial domain information and added heating mask on heating grid
    ilony = np.where((lonall>=domy[0])&(lonall<=domy[1]))[0]; nlony = len(ilony)
    ilaty = np.where((latall>=domy[2])&(latall<=domy[3]))[0]; nlaty = len(ilaty)
    ilonsy = np.reshape(np.repeat(ilony,nlaty),(-1,nlaty)).T
    ilatsy = np.reshape(np.repeat(ilaty,nlony),(nlaty,-1))
    Xdomain = np.zeros((1,nlatall,nlonall,6))
    Xdomain[0,ilatsx1,ilonsx1,1] = 1
    Xdomain[0,ilatsx2,ilonsx2,2] = 1
    Xdomain[0,ilatsy,ilonsy,3] = 1
    for j in range(0,nlatall):
        for i in range(0,nlonall):
            x = lonall[i]; y = latall[j]/10.0
            if ((x<30.0)&(x>290.0)):
                Xdomain[0,j,i,0] = -999.0
            if (Xdomain[0,j,i,0]>(-900.0)):
                xd = 0.0; yd = 0.0; kd = 0.0
                if (y<(-1.5)):
                    yd = (-1.0*y-1.5)*10.0/5.0
                if (y>2.0):
                    yd = (y-2.0)*10.0/5.0
                if (x<60.0):
                    xd = (60.0-x)/5.0
                if (x>260.0):
                    xd = (x-260.0)/5.0
                if ((x<120.0)&(y>0.5)):
                    kd  = (120.0-x)/5.0
                    kkd = (y-0.5)*10.0/2.5
                    if (kkd<kd):
                        kd = (y-0.5)*10.0/2.5 
# Fig. 1 domains for Fig. 2 calculations
                if ((x>=120)&(x<=260)&(y>=(-1.5))&(y<=2.0)):
                    Xdomain[0,j,i,4] = 1
                if ((x>=60)&(x<120)&(y>=(-1.5))&(y<=0.5)):
                    Xdomain[0,j,i,5] = 1
                Xdomain[0,j,i,0] = np.exp(-1.0*xd*xd-1.0*yd*yd-1.0*kd*kd)

# Write out domain information
    timeunits = 'years since 1979-06-01 00:00'
    varname = ['mask','pactele','iotele','ind','pac','io']
    varlongname = ['mask for added heating experiments','Pacific Ocean teleconnection domain','Indian Ocean teleconnection domain','Indian monsoon circulation domain','Pacific Ocean domain','Indian Ocean domain']
    varunits = ['unit-less','unit-less','unit-less','unit-less','unit-less','unit-less']
    title = 'Domain information and added heating mask'
    ncwrite(Xdomain,lonall,latall,timeunits=timeunits,undef=-999,varname=varname,varunits=varunits,varlongname=varlongname,title=title,filename='domain.nc')

    return (X1, Xctl1, Xhtg1, Xadd1, lonx1, latx1, gx1, X2, Xctl2, Xhtg2, Xadd2, lonx2, latx2, gx2, Y, Yctl, Yhtg, lony, laty, gy, Xdomain, lonall, latall)


def ncwrite(var0,lon1,lat1,timeunits='months since 1979-01-01 00:00',delt=1,undef=-9.99e+08,varname=['None'],varlongname=['None'],varunits=['None'],title='None',filename='vars.nc'):

# function writes one or n variables to netcdf file

# requires first 3 dimensions of input var0 such that:
#     var0.shape[0:3] == (len(time),len(lat),len(lon))
# optional 4th dimension of input var0 indicates multiple variables
#     var0.shape[4-1] == nvar
# requires nvar <= 20

    ndim = len(var0.shape)
    if ndim==3:
        nvar = 1

    if ndim==4:
        nvar = var0.shape[3]

    root_grp = nc(filename, 'w', format='NETCDF4')

# give title to file only if specified
    if title!='None':
        root_grp.description = title

# give dimensions
    root_grp.createDimension('lon', len(lon1))
    root_grp.createDimension('lat', len(lat1))
    root_grp.createDimension('time', None)

# give variables
    lon = root_grp.createVariable('lon', 'f8', ('lon',))
    lat = root_grp.createVariable('lat', 'f8', ('lat',))
    time = root_grp.createVariable('time', 'f8', ('time',))

# give default names if unspecified
    if varname[0]=='None':
        varname = []
        z = 1
        while z <= nvar:
            varname = np.append(varname,'var'+str(z))
            z = z + 1

    if varlongname[0]=='None':
        varlongname = []
        z = 1
        while z <= nvar:
            varlongname = np.append(varlongname,' ')
            z = z + 1

    if varunits[0]=='None':
        varunits = []
        z = 1
        while z <= nvar:
            varunits = np.append(varunits,' ')
            z = z + 1

    var1 = root_grp.createVariable(varname[0], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
    if nvar==1:
        var1[:,:,:] = var0[:,:,:]
        var1.long_name = varlongname[0]
        var1.units = varunits[0]
    if nvar>1:
        var1[:,:,:] = var0[:,:,:,0]
        var1.long_name = varlongname[0]
        var1.units = varunits[0]
        var2 = root_grp.createVariable(varname[1], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var2[:,:,:] = var0[:,:,:,1]
        var2.long_name = varlongname[1]
        var2.units = varunits[1]
    if nvar>2:
        var3 = root_grp.createVariable(varname[2], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var3[:,:,:] = var0[:,:,:,2]
        var3.long_name = varlongname[2]
        var3.units = varunits[2]
    if nvar>3:
        var4 = root_grp.createVariable(varname[3], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var4[:,:,:] = var0[:,:,:,3]
        var4.long_name = varlongname[3]
        var4.units = varunits[3]
    if nvar>4:
        var5 = root_grp.createVariable(varname[4], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var5[:,:,:] = var0[:,:,:,4]
        var5.long_name = varlongname[4]
        var5.units = varunits[4]
    if nvar>5:
        var6 = root_grp.createVariable(varname[5], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var6[:,:,:] = var0[:,:,:,5]
        var6.long_name = varlongname[5]
        var6.units = varunits[5]
    if nvar>6:
        var7 = root_grp.createVariable(varname[6], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var7[:,:,:] = var0[:,:,:,6]
        var7.long_name = varlongname[6]
        var7.units = varunits[6]
    if nvar>7:
        var8 = root_grp.createVariable(varname[7], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var8[:,:,:] = var0[:,:,:,7]
        var8.long_name = varlongname[7]
        var8.units = varunits[7]
    if nvar>8:
        var9= root_grp.createVariable(varname[8], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var9[:,:,:] = var0[:,:,:,8]
        var9.long_name = varlongname[8]
        var9.units = varunits[8]
    if nvar>9:
        var10= root_grp.createVariable(varname[9], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var10[:,:,:] = var0[:,:,:,9]
        var10.long_name = varlongname[9]
        var10.units = varunits[9]
    if nvar>10:
        var11 = root_grp.createVariable(varname[10], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var11[:,:,:] = var0[:,:,:,10]
        var11.long_name = varlongname[10]
        var11.units = varunits[10]
    if nvar>11:
        var12= root_grp.createVariable(varname[11], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var12[:,:,:] = var0[:,:,:,11]
        var12.long_name = varlongname[11]
        var12.units = varunits[11]
    if nvar>12:
        var13 = root_grp.createVariable(varname[12], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var13[:,:,:] = var0[:,:,:,12]
        var13.long_name = varlongname[12]
        var13.units = varunits[12]
    if nvar>13:
        var14= root_grp.createVariable(varname[13], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var14[:,:,:] = var0[:,:,:,13]
        var14.long_name = varlongname[13]
        var14.units = varunits[13]
    if nvar>14:
        var15 = root_grp.createVariable(varname[14], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var15[:,:,:] = var0[:,:,:,14]
        var15.long_name = varlongname[14]
        var15.units = varunits[14]
    if nvar>15:
        var16= root_grp.createVariable(varname[15], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var16[:,:,:] = var0[:,:,:,15]
        var16.long_name = varlongname[15]
        var16.units = varunits[15]
    if nvar>16:
        var17 = root_grp.createVariable(varname[16], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var17[:,:,:] = var0[:,:,:,16]
        var17.long_name = varlongname[16]
        var17.units = varunits[16]
    if nvar>17:
        var18= root_grp.createVariable(varname[17], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var18[:,:,:] = var0[:,:,:,17]
        var18.long_name = varlongname[17]
        var18.units = varunits[17]
    if nvar>18:
        var19= root_grp.createVariable(varname[19], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var19[:,:,:] = var0[:,:,:,18]
        var19.long_name = varlongname[18]
        var19.units = varunits[18]
    if nvar>19:
        var20= root_grp.createVariable(varname[19], 'f4', ('time', 'lat', 'lon'),fill_value=undef)
        var20[:,:,:] = var0[:,:,:,19]
        var20.long_name = varlongname[19]
        var20.units = varunits[19]


# Give attributes units and long_name
    lon.setncatts({'units':u"degrees_east",'long_name':u"Longitude"})
    lat.setncatts({'units':u"degrees_north",'long_name':u"Latitude"})
    time.setncatts({'units':timeunits,'long_name':u"Time"})

# Give data for dimensions
    lon_range = lon1
    lat_range = lat1
    lon[:] = lon1
    lat[:] = lat1
    time[:] = np.arange(var0.shape[0])*delt

    root_grp.close()

    return


def plotvariates(Rx,Ry,domx='',savename='Fig.pdf',show=True):

    nyrs = Rx.shape[0]
    x  = np.arange(nyrs)+1979
    plt.plot(x,Rx[:,1],color='blue')
    plt.plot(x,Rx[:,2],color='orange')
    plt.plot(x,Rx[:,0],color='black',linestyle='dashed')
    plt.xlabel('year'); plt.title('variates and ens. mean projections')
    ylim = [-4,15]; offset = 9
    plt.ylim(ylim[0],ylim[1])
    plt.plot(x,Ry[:,1]+offset,color='blue')
    plt.plot(x,Ry[:,2]+offset,color='orange')
    plt.plot(x,Ry[:,0]+offset,color='black',linestyle='dashed')
    plt.yticks(np.delete(np.arange(0,14)-2,[5,6,7,8]),[-2,1,0,1,2,-2,-1,0,1,2])
    plt.text(1976.0,ylim[1]+0.5,'(c)',fontsize=20)
    plt.text(1980.5,ylim[1]-0.9,'India')
    plt.text(1980.5,ylim[1]-1.7,'850 hPa U,V')
    plt.text(1990.5,ylim[1]-1.7,'ERA-Interim',color='black')
    plt.text(1990.5,ylim[1]-2.5,'Control',color='blue')
    plt.text(1990.5,ylim[1]-3.3,'Added heating',color='orange')
    VAR = np.round([np.var(Ry[:,1]),np.var(Ry[:,2])],2)
    COR = np.round([np.corrcoef(Ry[:,1],Ry[:,0])[1,0],np.corrcoef(Ry[:,2],Ry[:,0])[1,0]],2)
    crossCOR = np.round([np.corrcoef(Rx[:,1],Ry[:,1])[1,0],np.corrcoef(Rx[:,2],Ry[:,2])[1,0]],2)
    plt.text(2002.5,ylim[1]-1.7,'VAR',horizontalalignment='center')
    plt.text(2002.5,ylim[1]-2.5,VAR[0],horizontalalignment='center',color='blue')
    plt.text(2002.5,ylim[1]-3.3,VAR[1],horizontalalignment='center',color='orange')
    plt.text(2007.2,ylim[1]-1.7,'COR',horizontalalignment='center')
    plt.text(2007.5,ylim[1]-2.5,COR[0],horizontalalignment='center',color='blue')
    plt.text(2007.5,ylim[1]-3.3,COR[1],horizontalalignment='center',color='orange')
    plt.text(2012.5,ylim[1]-0.9,'cross-',horizontalalignment='center')
    plt.text(2012.5,ylim[1]-1.7,'COR',horizontalalignment='center')
    plt.text(2012.5,ylim[1]-2.5,crossCOR[0],horizontalalignment='center',color='blue')
    plt.text(2012.5,ylim[1]-3.3,crossCOR[1],horizontalalignment='center',color='orange')
    if (len(domx)<=7):
        plt.text(1980.5,4.8,domx+' heating')
    if (len(domx)>7):
        plt.text(1980.5,4.8,domx)
        plt.text(1980.5,4.0,'heating')
    plt.text(1990.5,4.8,'ERA-Interim',color='black')
    plt.text(1990.5,4.0,'Control',color='blue')
    plt.text(1990.5,3.2,'Added heating',color='orange')
    VAR = np.round([np.var(Rx[:,1]),np.var(Rx[:,2])],2)
    COR = np.round([np.corrcoef(Rx[:,1],Rx[:,0])[1,0],np.corrcoef(Rx[:,2],Rx[:,0])[1,0]],2)
    plt.text(2002.5,4.8,'VAR',horizontalalignment='center')
    plt.text(2002.5,4.0,VAR[0],horizontalalignment='center',color='blue')
    plt.text(2002.5,3.2,VAR[1],horizontalalignment='center',color='orange')
    plt.text(2007.5,4.8,'COR',horizontalalignment='center')
    plt.text(2007.5,4.0,COR[0],horizontalalignment='center',color='blue')
    plt.text(2007.5,3.2,COR[1],horizontalalignment='center',color='orange')
    plt.grid(True); plt.savefig(savename,format='pdf')
    if show:
        plt.show()
    
    return

