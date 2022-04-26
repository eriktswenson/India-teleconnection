

import numpy as np
from sklearn.linear_model import LinearRegression

def pca(x,g,k=1):

# Computes Prinicipal Component Analysis (PCA) on x
# that varies spatially (m) and temporally (n) with x.shape == (m,n)
#  -anomalies are weighted by g with g.shape == (m,1)
#  -assume time mean removed prior
#  -performs k-fold cross-validation
#  -must have int(n/k)==int(np.ceil(n/k))

# Author:  Erik Swenson (latest revision Feb 2020)

# >>> import cvsvd
# >>> E, F, sx, xclim, Find, Eproj, fve, lw, cp, nu = cvsvd.pca(x,g,k)


    m = x.shape[0]
    n = x.shape[1]
    nk = int(n/k)
    nt = n-k

    nlim = min(m,nt)
    nlim0 = min(m,n)
    nsign = nlim
    signtol = 0.5
    check = False

    xclim = np.zeros((m,nk+1))
    sx = np.zeros((nlim0,nk+1))
    E = np.zeros((m,nlim0,nk+1))
    Eproj = np.zeros((m,nlim0,nk+1))
    F = np.zeros((nlim0,n,nk+1))
    Find = np.zeros((nlim,n))
    xind = np.zeros((m,n))

# location of training sample for each iteration
# of cross-validation; assigns False to location of 
# independent samples and True to location of training samples
    wheretrain = np.ones((nk,k,nk+1),dtype=bool)
    for z in range(1,nk+1):
        wheretrain[z-1,:,z] = False

    wheretrain = np.reshape(wheretrain,(n,nk+1))

    for z in range(0,nk+1):
        train = np.where(wheretrain[:,z])[0] 
# Compute climatology & apply weighting
        xk = x[:,train]; nt = len(train); nlim = min(m,nt)
        clim = np.mean(xk,axis=1,keepdims=True)
        xk = xk-clim
# Singular Value Decomposition (V actually transposed)
        Uk, sk, Vk = np.linalg.svd(g*xk,full_matrices=False)
        Sk = np.reshape(np.repeat(sk,m),(nlim,m)).T
        gEk = (1/np.sqrt(nt))*Uk*Sk
        Eprojk = nt*g*gEk/(Sk**2)
        Fk = np.sqrt(nt)*Vk
        Ek = gEk/g
# Ledoit-Wolf parameter for covariance extimation
        if z==0:
            ex = (sk[0:(nt-1)]**2)/n
            mu = np.sum(ex)/m
            C = np.matmul(xk,xk.T)/n
            denom = np.sum((C-mu*np.diag(np.ones(m)))**2)
            num = 0
            for zz in range(0,nt):
                Fzz = np.reshape(sk[0:(nt-1)]*Vk[0:(nt-1),zz],(-1,1))
                num = num + np.sum((np.matmul(Fzz,Fzz.T)-np.diag(ex))**2)/n/n
            lw = num/denom
# Find closest continuum power solution
            sxr = (1-lw)*ex+lw*mu
            cp = 0.25
            delta = 0.1
            while delta>0.00001:
                d = [-1*delta,0,delta]
                error = np.zeros(3)
                for zz in range(0,3):
                    sxc = ex**(1-cp-d[zz])
                    nu = mu*m/np.sum(sxc)
                    sxc = nu*sxc
                    error[zz] = np.sum((sxr-sxc)**2)
                if error[2]<error[1]:
                    cp = cp + delta
                if error[0]<error[1]:
                    cp = cp - delta
                if (error[1]<error[2])&(error[1]<error[0]):
                    delta = delta * 0.1
                sxc = ex**(1-cp)
                nu = mu*m/np.sum(sxc)
                sxc = nu*sxc
# Fraction of variance explained
            fve = (sk**2)/np.sum(sk**2)
        fvek = (sk**2)/np.sum(sk**2)
        if z>0:
# Cross-validated PCs from projecting
# independent data onto EOF patterns
            ind = np.where(wheretrain[:,z]==False)[0]
            Find[0:nt,ind] = np.matmul(Eprojk.T,x[:,ind]-clim)
# Save values
        xclim[:,z] = clim[:,0]
        sx[0:nlim,z] = sk
        E[:,0:nlim,z] = Ek
        Eproj[:,0:nlim,z] = Eprojk
        F[0:nlim,train,z] = Fk
        if check and z==0:
            np.allclose(g*xk,np.matmul(Uk*Sk,Vk),atol=1e-5)
            np.allclose(xk,np.matmul(Ek,Fk),atol=1e-5)
            check1 = fvek-fvek
            for i in range(0,nt):
                check1[i] = 1-np.sum((np.matmul(gEk[:,0:i],Fk[0:i,:])-g*xk)**2)/np.sum((g*xk)**2)
            np.allclose(fvek[0:9],check1[1:10]-check1[0:9],atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Uk[:,0:(nlim-1)].T,Uk[:,0:(nlim-1)]),atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Vk[0:(nlim-1),:],Vk[0:(nlim-1),:].T),atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Eprojk[:,0:(nlim-1)].T,Ek[:,0:(nlim-1)]),atol=1e-5)
            np.allclose(Fk[0:(nlim-1),:],np.matmul(Eprojk[:,0:(nlim-1)].T,xk),atol=1e-5)
            reg = LinearRegression().fit(Fk[0:(nlim-1),:].T,xk.T)
            np.allclose(Ek[:,0:(nlim-1)],reg.coef_,atol=1e-5)

# Modify sign of leading EOFs/PCs if PCs have significantly
# negative correlation with those computed with all data 
    for z in range(1,nk+1):
        train = np.where(wheretrain[:,z])[0]; nt = len(train)
        ind = np.where(wheretrain[:,z]==False)[0]
        for zz in range(0,nsign):
# If projection value significantly negative
#            val = np.sum(Eproj[:,zz,0]*E[:,zz,z])
# If correlation value significantly negative
            val = np.corrcoef(F[zz,train,z],F[zz,train,0])[0,1]
            if val < (signtol*-1):
                E[:,zz,z] = E[:,zz,z] * -1.0
                Eproj[:,zz,z] = Eproj[:,zz,z] * -1.0
                F[zz,train,z] = F[zz,train,z] * -1.0
                Find[zz,ind] = Find[zz,ind] * -1.0

# Cross-validated fraction of variance explained
#    fveind = fve-fve
#    denom = np.sum((g*x)**2)
#    for i in range(0,n):
#        for z in range(0,nk):
#            ind = np.where(wheretrain[:,z]==False)[0]
#            xind[:,ind] = xind[:,ind] + np.matmul(np.reshape(E[:,i,z],(-1,1)),np.reshape(Find[i,ind],(1,-1)))
#        fveind[i] = 1-np.sum((g*(x-xind))**2)/denom

#    temp = np.zeros(n)
#    temp[:] = fveind
#    for i in range(1,n):
#       fveind[i] = temp[i]-temp[i-1]
#

    return (E, F, sx, xclim, Find, Eproj, fve, lw, mu, cp, nu)


def pcarem(y,x,g,k=1):

# Computes Prinicipal Component Analysis (PCA) on x
# that varies spatially (m) and temporally (n) with x.shape == (m,n)
# Also regresses out time series y prior
#  -anomalies are weighted by g with g.shape == (m,1)
#  -assume time mean removed prior
#  -performs k-fold cross-validation
#  -must have int(n/k)==int(np.ceil(n/k))

# Author:  Erik Swenson (latest revision Aug 2020)

# >>> import cvsvd
# >>> E, F, sx, xclim, Find, Eproj, fve, lw, cp, nu = cvsvd.pcarem(y,x,g,k)


    m = x.shape[0]
    n = x.shape[1]
    nk = int(n/k)
    nt = n-k

    nlim = min(m,nt)
    nlim0 = min(m,n)
    nsign = nlim
    signtol = 0.5
    check = False

    xclim = np.zeros((m,nk+1))
    sx = np.zeros((nlim0,nk+1))
    E = np.zeros((m,nlim0,nk+1))
    Eproj = np.zeros((m,nlim0,nk+1))
    F = np.zeros((nlim0,n,nk+1))
    Find = np.zeros((nlim,n))
    xind = np.zeros((m,n))

# location of training sample for each iteration
# of cross-validation; assigns False to location of 
# independent samples and True to location of training samples
    wheretrain = np.ones((nk,k,nk+1),dtype=bool)
    for z in range(1,nk+1):
        wheretrain[z-1,:,z] = False

    wheretrain = np.reshape(wheretrain,(n,nk+1))

    for z in range(0,nk+1):
        train = np.where(wheretrain[:,z])[0]
# Compute climatology & apply weighting
        xk = x[:,train]; nt = len(train); nlim = min(m,nt)
        clim = np.mean(xk,axis=1,keepdims=True)
        xk = xk-clim
# Regress out y
        yk = np.reshape(y[train,z],(1,-1))
        reg = LinearRegression().fit(yk.T,xk.T)
        xk = xk - np.matmul(reg.coef_,yk)
# Singular Value Decomposition (V actually transposed)
        Uk, sk, Vk = np.linalg.svd(g*xk,full_matrices=False)
        Sk = np.reshape(np.repeat(sk,m),(nlim,m)).T
        gEk = (1/np.sqrt(nt))*Uk*Sk
        Eprojk = nt*g*gEk/(Sk**2)
        Fk = np.sqrt(nt)*Vk
        Ek = gEk/g
# Ledoit-Wolf parameter for covariance extimation
        if z==0:
            Beta = reg.coef_
            ex = (sk[0:(nt-1)]**2)/n
            mu = np.sum(ex)/m
            C = np.matmul(xk,xk.T)/n
            denom = np.sum((C-mu*np.diag(np.ones(m)))**2)
            num = 0
            for zz in range(0,nt):
                Fzz = np.reshape(sk[0:(nt-1)]*Vk[0:(nt-1),zz],(-1,1))
                num = num + np.sum((np.matmul(Fzz,Fzz.T)-np.diag(ex))**2)/n/n
            lw = num/denom
# Find closest continuum power solution
            sxr = (1-lw)*ex+lw*mu
            cp = 0.25
            delta = 0.1
            while delta>0.00001:
                d = [-1*delta,0,delta]
                error = np.zeros(3)
                for zz in range(0,3):
                    sxc = ex**(1-cp-d[zz])
                    nu = mu*m/np.sum(sxc)
                    sxc = nu*sxc
                    error[zz] = np.sum((sxr-sxc)**2)
                if error[2]<error[1]:
                    cp = cp + delta
                if error[0]<error[1]:
                    cp = cp - delta
                if (error[1]<error[2])&(error[1]<error[0]):
                    delta = delta * 0.1
                sxc = ex**(1-cp)
                nu = mu*m/np.sum(sxc)
                sxc = nu*sxc
# Fraction of variance explained
            fve = (sk**2)/np.sum(sk**2)
        fvek = (sk**2)/np.sum(sk**2)
        if z>0:
# Cross-validated PCs from projecting
# independent data onto EOF patterns
            ind = np.where(wheretrain[:,z]==False)[0]
            Find[0:nt,ind] = np.matmul(Eprojk.T,x[:,ind]-clim)
# Save values
        xclim[:,z] = clim[:,0]
        sx[0:nt,z] = sk
        E[:,0:nt,z] = Ek
        Eproj[:,0:nt,z] = Eprojk
        F[0:nt,train,z] = Fk
        if check and z==0:
            np.allclose(g*xk,np.matmul(Uk*Sk,Vk),atol=1e-5)
            np.allclose(xk,np.matmul(Ek,Fk),atol=1e-5)
            check1 = fvek-fvek
            for i in range(0,nt):
                check1[i] = 1-np.sum((np.matmul(gEk[:,0:i],Fk[0:i,:])-g*xk)**2)/np.sum((g*xk)**2)
            np.allclose(fvek[0:9],check1[1:10]-check1[0:9],atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Uk[:,0:(nlim-1)].T,Uk[:,0:(nlim-1)]),atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Vk[0:(nlim-1),:],Vk[0:(nlim-1),:].T),atol=1e-5)
            np.allclose(np.diag(np.ones(nlim-1)),np.matmul(Eprojk[:,0:(nlim-1)].T,Ek[:,0:(nlim-1)]),atol=1e-5)
            np.allclose(Fk[0:(nlim-1),:],np.matmul(Eprojk[:,0:(nlim-1)].T,xk),atol=1e-5)
            reg = LinearRegression().fit(Fk[0:(nlim-1),:].T,xk.T)
            np.allclose(Ek[:,0:(nlim-1)],reg.coef_,atol=1e-5)

# Modify sign of leading EOFs/PCs if PCs have significantly
# negative correlation with those computed with all data 
    for z in range(1,nk+1):
        train = np.where(wheretrain[:,z])[0]; nt = len(train)
        ind = np.where(wheretrain[:,z]==False)[0]
        for zz in range(0,nsign):
# If projection value significantly negative
#            val = np.sum(Eproj[:,zz,0]*E[:,zz,z])
# If correlation value significantly negative
            val = np.corrcoef(F[zz,train,z],F[zz,train,0])[0,1]
            if val < (signtol*-1):
                E[:,zz,z] = E[:,zz,z] * -1.0
                Eproj[:,zz,z] = Eproj[:,zz,z] * -1.0
                F[zz,train,z] = F[zz,train,z] * -1.0
                Find[zz,ind] = Find[zz,ind] * -1.0

# Cross-validated fraction of variance explained
#    fveind = fve-fve
#    denom = np.sum((g*x)**2)
#    for i in range(0,n):
#        for z in range(0,nk):
#            ind = np.where(wheretrain[:,z]==False)[0]
#            xind[:,ind] = xind[:,ind] + np.matmul(np.reshape(E[:,i,z],(-1,1)),np.reshape(Find[i,ind],(1,-1)))
#        fveind[i] = 1-np.sum((g*(x-xind))**2)/denom

#    temp = np.zeros(n)
#    temp[:] = fveind
#    for i in range(1,n):
#       fveind[i] = temp[i]-temp[i-1]
#

    return (E, F, sx, xclim, Find, Eproj, fve, lw, mu, cp, nu, Beta)


def cross(Ex,Fx,sx,Findx,Eprojx,Ey,Fy,sy,Findy,Eprojy,lw1='null',lw2='null',k=1,neof='null',docp=False,cp1='null',cp2='null'):

# Relates X and Y using their associated PCs Fx and Fy
# X and Y vary spatially (mx and my) and temporally (n)
#  -follows individual pca() calls
#  -performs k-fold cross-validation

# Author:  Erik Swenson (latest revision Feb 2020)

# >>> import cvsvd
# >>> Px, Rx, Rxind, Urho1, Py, Ry, Ryind, Vrho1, cor1, cor2 = cvsvd.cross(Ex,Fx,sx,Findx,Eprojx,Ey,Fy,sy,Findy,Eprojy,lw1,lw2,k,neof,docp,cp1,cp2)


# Use only truncated data
    if neof=='null':
        neof = min(Fx.shape[0],Fy.shape[0])-k

    if lw1=='null':
        lw1 = 1

    if lw2=='null':
        lw2 = 1

    if cp1=='null':
        cp1 = 1

    if cp2=='null':
        cp2 = 1

    Ex = Ex[:,0:neof,:]; Ey = Ey[:,0:neof,:]
    Fx = Fx[0:neof,:,:]; Fy = Fy[0:neof,:,:]
 
    mx= Ex.shape[0]
    my= Ey.shape[0]
    n = Fx.shape[1]
    nk = int(n/k)
    nt = n-k

    nlim = min(neof,n-k-1)
    nsign = nlim
    signtol = 0.5

    cor1 = np.zeros(nsign)
    cor2 = np.zeros(nsign)

    sx = sx[0:neof,:]; sy = sy[0:neof,:]

    Px= np.zeros((mx,neof,nk+1))
    Py= np.zeros((my,neof,nk+1))
    Rx= np.zeros((neof,n,nk+1))
    Ry= np.zeros((neof,n,nk+1))
    Rxind= np.zeros((nlim,n))
    Ryind= np.zeros((nlim,n))
    
# location of training sample for each iteration
# of cross-validation; assigns False to location of 
# independent samples and True to location of training samples
    wheretrain = np.ones((nk,k,nk+1),dtype=bool)
    for z in range(1,nk+1):
        wheretrain[z-1,:,z] = False
    
    wheretrain = np.reshape(wheretrain,(n,nk+1))
     
    for z in range(0,nk+1):
        train = np.where(wheretrain[:,z])[0]; nt = len(train)
        nlim = neof
        if z>0:
            nlim = np.min([neof,n-k-1])

        exk = (sx[0:nlim,z]**2)/nt
        eyk = (sy[0:nlim,z]**2)/nt
        mux = np.sum(exk)/mx
        muy = np.sum(eyk)/my
# Ridge
        sxk = sx[0:nlim,z]/np.sqrt((1-lw1)*exk+lw1*mux)
        syk = sy[0:nlim,z]/np.sqrt((1-lw2)*eyk+lw2*muy)
# Continuum power
        if docp:
            sxk = exk**(1-cp1); nux = mux*mx/np.sum(sxk)
            sxk = sx[0:nlim,z]/np.sqrt(nux*sxk)
            syk = eyk**(1-cp2); nuy = muy*my/np.sum(syk)
            syk = sy[0:nlim,z]/np.sqrt(nuy*syk)
        Exk = Ex[:,0:nlim,z] * np.reshape(np.repeat(1/sxk,mx),(nlim,mx)).T
        Eyk = Ey[:,0:nlim,z] * np.reshape(np.repeat(1/syk,my),(nlim,my)).T
        Fxk = Fx[0:nlim,train,z] * np.reshape(np.repeat(sxk,nt),(nlim,nt))
        Fyk = Fy[0:nlim,train,z] * np.reshape(np.repeat(syk,nt),(nlim,nt))
        covk = np.matmul(Fxk,(Fyk).T)
        Urho, cc, Vrho = np.linalg.svd(covk,full_matrices=False)
        Px[:,0:nlim,z] = np.matmul(Exk,Urho)
        Py[:,0:nlim,z] = np.matmul(Eyk,Vrho.T)
        Rx[0:nlim,train,z] = np.matmul(Urho.T,Fxk)
        Ry[0:nlim,train,z] = np.matmul(Vrho,Fyk)
# Independent data
        if z>0:
            ind = np.where(wheretrain[:,z]==False)[0]
            Findxk = Findx[0:nlim,ind] * np.reshape(np.repeat(sxk,k),(nlim,k))
            Findyk = Findy[0:nlim,ind] * np.reshape(np.repeat(syk,k),(nlim,k))
            Rxind[:,ind] = np.matmul(Urho.T,Findxk)
            Ryind[:,ind] = np.matmul(Vrho,Findyk)
# Normalize
        srx = np.sqrt(np.diag(np.matmul(Rx[0:nlim,train,z],Rx[0:nlim,train,z].T))/nt)
        sry = np.sqrt(np.diag(np.matmul(Ry[0:nlim,train,z],Ry[0:nlim,train,z].T))/nt)
        Px[:,0:nlim,z] = Px[:,0:nlim,z] * np.reshape(np.repeat(srx,mx),(nlim,mx)).T
        Py[:,0:nlim,z] = Py[:,0:nlim,z] * np.reshape(np.repeat(sry,my),(nlim,my)).T
        Rx[0:nlim,train,z] = Rx[0:nlim,train,z] * np.reshape(np.repeat(1/srx,nt),(nlim,nt))
        Ry[0:nlim,train,z] = Ry[0:nlim,train,z] * np.reshape(np.repeat(1/sry,nt),(nlim,nt))
        if z==0:
            Sx = np.reshape(np.repeat(sxk,mx),(nlim,-1)).T
            Srx = np.reshape(np.repeat(1/srx,mx),(nlim,-1)).T
            Pprojx = np.matmul(Sx*Eprojx[:,0:nlim,z],Urho)*Srx
            Sy = np.reshape(np.repeat(syk,my),(nlim,-1)).T
            Sry = np.reshape(np.repeat(1/sry,my),(nlim,-1)).T
            Pprojy = np.matmul(Sy*Eprojy[:,0:nlim,z],Vrho.T)*Sry
        if z>0:
            Rxind[:,ind] = Rxind[:,ind] * np.reshape(np.repeat(1/srx,k),(nlim,k))
            Ryind[:,ind] = Ryind[:,ind] * np.reshape(np.repeat(1/sry,k),(nlim,k))

# Modify sign of leading patterns/variates if variates have significantly
# negative correlation with those computed with all data 
    for z in range(1,nk+1):
        train = np.where(wheretrain[:,z])[0]; nt = len(train)
        ind = np.where(wheretrain[:,z]==False)[0]
        for zz in range(0,nsign):
# If correlation value significantly negative
            valx = np.corrcoef(Rx[zz,train,z],Rx[zz,train,0])[0,1]
            valy = np.corrcoef(Ry[zz,train,z],Ry[zz,train,0])[0,1]
            if (valx < (signtol * -1.0)) & (valy < (signtol * -1.0)):
                Px[:,zz,z] = Px[:,zz,z] * -1.0
                Py[:,zz,z] = Py[:,zz,z] * -1.0
                Rx[zz,train,z] = Rx[zz,train,z] * -1.0
                Ry[zz,train,z] = Ry[zz,train,z] * -1.0
                Rxind[zz,ind] = Rxind[zz,ind] * -1.0
                Ryind[zz,ind] = Ryind[zz,ind] * -1.0

    for z in range(0,nsign):
        cor1[z] = np.corrcoef(Rx[z,:,0],Ry[z,:,0])[0,1]
        cor2[z] = np.corrcoef(Rxind[z,:],Ryind[z,:])[0,1]

    return (Px, Rx, Rxind, Pprojx, Py, Ry, Ryind, Pprojy, cor1, cor2)

