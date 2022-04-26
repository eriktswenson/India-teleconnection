
import numpy as np
from netCDF4 import Dataset as nc
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import inout
import cvsvd

# longitude/latitude for domains
domx1 = [120,280,-15,20]
domx2 = [ 50,120,-15, 5]
domy  = [ 55, 95,  5,35]
nyrs = 38; nens = 10

# read in heating DT and 850 hPa horizontal winds U,V
X1, Xctl1, Xhtg1, Xadd1, lonx1, latx1, gx1, X2, Xctl2, Xhtg2, Xadd2, lonx2, latx2, gx2, Y, Yctl, Yhtg, lony, laty, gy, Xdomain, lon, lat = inout.readDTUV(domx1,domx2,domy)

# Compute PCA with k-fold cross-validation
k = 1
E1, F1, sx1, xclim1, Find1, Eproj1, fve1, lw1, mu1, cp1, nu1 = cvsvd.pca(X1,gx1,k=k)
E2, F2, sx2, xclim2, Find2, Eproj2, fve2, lw2, mu2, cp2, nu2 = cvsvd.pca(Y,gy,k=k)

# SVD technique
docp = False; a = 1; b = 1; neof = 'null'; meth = 'MCA'       #   MCA
docp = False; a = 0; b = 0; neof = 10; meth = 'CCA10'         #   CCA
docp = False; a = lw1; b = lw2; neof = 'null'; meth = 'RCCA'  #  RCCA
docp = True; a = lw1; b = lw2; neof = 'null'; meth = 'CPCCA'  # CPCCA

# Compute Pac modes (leading mode ENSO)
P1, R1, Rind1, Pproj1, P2, R2, Rind2, Pproj2, cor1, cor2 = cvsvd.cross(E1,F1,sx1,Find1,Eproj1,E2,F2,sx2,Find2,Eproj2,lw1=a,lw2=b,k=k,neof=neof,docp=docp,cp1=cp1,cp2=cp2)

# Cross-validated correlation coefficents
list(np.round(cor2[0:5],9))

# Save Pac ENSO mode
nlatx1 = len(latx1); nlonx1 = len(lonx1)
Px1 = np.reshape(P1[:,0,0],(1,nlatx1,nlonx1))
nlaty = len(laty); nlony = len(lony)
Py1 = np.reshape(np.reshape(P2[:,0,0],(2,nlaty*nlony)).T,(1,nlaty,nlony,2))
Pprojx1 = Pproj1[:,0]; Pprojy1 = Pproj2[:,0]
Rx = np.zeros((nyrs,3,2)); Ry = np.zeros((nyrs,3,2))
Rx[:,0,0] = R1[0,:,0]; Ry[:,0,0] = R2[0,:,0]

# Regress out Pac ENSO mode and compute PCA
y = R1[0,:,:]
E1, F1, sx1, xclim1, Find1, Eproj1, fve1, lw1, mu1, cp1, nu1, Beta1 = cvsvd.pcarem(y,X2,gx2,k=k)
E2, F2, sx2, xclim2, Find2, Eproj2, fve2, lw2, mu2, cp2, nu2, Beta2 = cvsvd.pcarem(y,Y,gy,k=k)

# Compute IO modes (leading mode EQUINOO)
P1, R1, Rind1, Pproj1, P2, R2, Rind2, Pproj2, cor1, cor2 = cvsvd.cross(E1,F1,sx1,Find1,Eproj1,E2,F2,sx2,Find2,Eproj2,lw1=a,lw2=b,k=k,neof=neof,docp=docp,cp1=cp1,cp2=cp2)
list(np.round(cor2[0:5],9))


# Write out patterns
timeunits = 'years since 1979-06-01 00:00'
title = meth+'-1 for ERA-Interim Pac JJAS diabatic heating rate (averaged 1000-50 hPa, K/day) and India 850hPa U,V (1979-2016)'
inout.ncwrite(Px1,lonx1,latx1,timeunits=timeunits,varname=['DT'],varunits=['K/day'],varlongname=['heating '+meth+'-1'],title=title,filename=meth+'.DT.pac.nc')

nlatx2 = len(latx2); nlonx2 = len(lonx2)
Px2 = np.zeros((1,nlatx2,nlonx2,2))
Px2[:,:,:,0] = np.reshape(P1[:,0,0],(1,nlatx2,nlonx2))
Px2[:,:,:,1] = np.reshape(Beta1,(1,nlatx2,nlonx2))
title = meth+'-1 (DT) for ERA-Interim IO JJAS diabatic heating rate (averaged 1000-50 hPa, K/day) and India 850hPa U,V (1979-2016) after Pac ENSO mode removed (DTreg)'
inout.ncwrite(Px2,lonx2,latx2,timeunits=timeunits,varname=['DT','DTreg'],varunits=['K/day','K/day'],varlongname=['heating '+meth+'-1','heating regression with Pac ENSO mode'],title=title,filename=meth+'.DT.io.nc')

varname=['Upac1','Vpac1','Ureg','Vreg','Uio1','Vio1']; filename=meth+'.UV.ind.nc'
varlongname = ['850 hPa U '+meth+'-1 w/Pac','850 hPa V '+meth+'-1 w/Pac','850 hPa U regression w/Pac ENSO mode','850 hPa V regression w/Pac ENSO mode','850 hPa U '+meth+'-1 w/IO','850 hPa V '+meth+'-1 w/IO']
varunits = ['m/s','m/s','m/s','m/s','m/s','m/s']
title = meth+'-1 for ERA-Interim IO JJAS diabatic heating rate (averaged 1000-50 hPa, K/day) and India 850hPa U,V (1979-2016) after Pac ENSO mode removed'
Py2 = np.reshape(np.reshape(P2[:,0,0],(2,nlaty*nlony)).T,(1,nlaty,nlony,2))
Beta2 = np.reshape(np.reshape(Beta2,(2,nlaty*nlony)).T,(1,nlaty,nlony,2))
Py = np.zeros((1,nlaty,nlony,6)); Py[:,:,:,0:2] = Py1[:,:,:,:]
Py[:,:,:,2:4] = Beta2[:,:,:,:]; Py[:,:,:,4:6] = Py2[:,:,:,:]
inout.ncwrite(Py,lony,laty,timeunits=timeunits,varname=varname,varunits=varunits,varlongname=varlongname,title=title,filename=meth+'.UV.io.nc')


# Variates and projections (flip sign for EQUINOO)
Rx[:,0,1] = -1*R1[0,:,0]; Ry[:,0,1] = -1*R2[0,:,0]
Pprojx2 = -1*Pproj1[:,0]; Pprojy2 = -1*Pproj2[:,0]

# CFSv2 projections and indices of Tables 1-3
# index.dat stream binary file with dimensions of (nyrs,1+2*nens,16)
# 16 - Pac X,Pac Y,IO X, IO Y, 12 indices from Tables 1-3
# IO projections first have CFSv2 Pac ENSO mode computed and removed
# Corresponds to default domains for CPCCA-1 closest to Ledoit-Wolf solution
index = np.reshape(np.fromfile('index.dat',dtype='float32'),(nyrs,1+2*nens,16))
indexobs = index[:,0,:]
indexctl = np.mean(index[:,1:(1+nens),:],1)
indexhtg = np.mean(index[:,(1+nens):(1+2*nens),:],1)
Rx[:,1,0:2] = indexctl[:,[0,2]]; Ry[:,1,0:2] = indexctl[:,[1,3]]
Rx[:,2,0:2] = indexhtg[:,[0,2]]; Ry[:,2,0:2] = indexhtg[:,[1,3]]
np.allclose(Rx[:,1,0],np.matmul(Pprojx1.T,Xctl1)) # equivalent
np.allclose(Ry[:,1,0],np.matmul(Pprojy1.T,Yctl))

# Years for Pac ENSO composites (Fig. 6) and IO EQUINOO composites (Fig. 8)
ipos1 = np.where(Rx[:,0,0]>1)[0]; ineg1 = np.where(Rx[:,0,0]<(-1))[0]
ipos2 = np.where(Rx[:,0,1]>1)[0]; ineg2 = np.where(Rx[:,0,1]<(-1))[0]

# Plot Figs. 5c & 7c
inout.plotvariates(Rx[:,:,0],Ry[:,:,0],domx='Pacific',savename='Fig5c.pdf')
inout.plotvariates(Rx[:,:,1],Ry[:,:,1],domx='Indian Ocean',savename='Fig7c.pdf')

# Subtract means and normalize
indexobs = indexobs - np.mean(indexobs,0); indexobs = indexobs/np.sqrt(np.mean(indexobs**2,0))
indexctl = indexctl - np.mean(indexctl,0); indexctl = indexctl/np.sqrt(np.mean(indexctl**2,0))
indexhtg = indexhtg - np.mean(indexhtg,0); indexhtg = indexhtg/np.sqrt(np.mean(indexhtg**2,0))

# Ensemble mean correlations with observed
names = ['ENSO heat','ENSO U,V','EQUINOO heat','EQUINOO U,V','Nino 3.4','WC','EMI','WNPSH','WFI','DMI','EQWIN','EQOLR','MH','SJ','WSI','ISMR']
print(names)
print(np.round(np.diag(np.matmul(indexobs.T,indexctl))/nyrs,2))
print(np.round(np.diag(np.matmul(indexobs.T,indexhtg))/nyrs,2))

indexctl = np.reshape(index[:,1:(1+nens),:],(nyrs*nens,16))
indexctl = indexctl - np.mean(indexctl,0); indexctl = indexctl/np.sqrt(np.mean(indexctl**2,0))
indexhtg = np.reshape(index[:,(1+nens):(1+2*nens),:],(nyrs*nens,16))
indexhtg = indexhtg - np.mean(indexhtg,0); indexhtg = indexhtg/np.sqrt(np.mean(indexhtg**2,0))

i = np.array([4,5,0,6,9,10,11,2,12,13,14])
print(np.round(np.matmul(indexobs[:,15].T,indexobs[:,i])/nyrs,2))
print(np.round(np.matmul(indexctl[:,15].T,indexctl[:,i])/(nens*nyrs),2))
print(np.round(np.matmul(indexhtg[:,15].T,indexhtg[:,i])/(nens*nyrs),2))


