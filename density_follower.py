# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 01:18:08 2014

@author: michaelnorris
"""

import numpy as np

#import matplotlib.animation as animation

class Density_1D(object):
    def __init__(self,nP,nQ):
        self.nP = nP # number of quantiles in distribution
        self.nQ = nQ # estimate quantiles of this many points of history
        #self.xmean = 0
        self.xvar = 1
        self.PV = np.arange(1.0/(nP+1.0),1.0,1.0/(nP+1.0))
        self.M = self.PV.copy()*0.0+1.0/self.nP
        self.V = self.PV.copy()
        self.kdev = 1/self.nQ

    def adapt(self,X): # adapt to next data point X
        #self.xmean = move(self.xmean,X,self.kdev)
        xmean = np.mean(self.V) # not mean of data, but mean of approx
        # to force adapting faster when there is more error
        self.xvar  = self.xvar * (1-self.kdev) + \
                    (X-xmean)**2.0 * self.kdev
        kM = np.sqrt(3*self.xvar)/((self.nP+1)*self.nQ)
        kV = self.M/(2*self.nQ)
        dv = X - self.V
        self.V += kV*(np.sign(dv) + 2*self.PV - 1)
        dm = np.abs(dv)-self.M
        self.M += kM*(np.sign(dm) + 4/(self.nP+1) - 1)

    def whiten(self,X):
        # find bin but don't adapt
        iX = np.sum(self.V>X)
        iX = min([self.nP-1,iX])
        iX = max([1,iX])
        y = (iX+(X-self.V[iX-1])/(self.V[iX]-self.V[iX-1]))/(self.N+1)
        return y