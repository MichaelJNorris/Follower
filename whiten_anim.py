"""/Users/michaelnorris/Python/anim_test8
A simple example of an animated plot
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#import matplotlib.animation as animation

class Distrib_1D(object):
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
        self.xvar  = move(self.xvar,(X-xmean)**2.0,self.kdev)
        kM = np.sqrt(3*self.xvar)/((self.nP+1)*self.nQ)
        kV = self.M/(2*self.nQ)
        dv = X - self.V
        self.V += kV*(np.sign(dv) + 2*self.PV - 1)
        dm = np.abs(dv)-self.M
        self.M += kM*(np.sign(dm) + 4/(self.nP+1) - 1)

    def whiten(self,X):
        # find bin
        iX = np.sum(self.V>X)
        iX = min([self.nP-1,iX])
        iX = max([1,iX])
        y = (iX+(X-self.V[iX-1])/(self.V[iX]-self.V[iX-1]))/(self.N+1)
        return y
        
    def run(self,Xes):
        for X in Xes:
            self.adapt(X)
        #plt.plot(1.0/np.diff(self.V))
        #plt.show()

ndat = 0
datsel = 0
def data(N):
    global ndat
    global datsel
    if ndat<400:
        ndat += 1
    else:
        ndat = 0
        datsel = int(np.random.rand()*4)
        if datsel < 0.5:
            print("exp")
        elif datsel < 1.5:
            print("sum")
        elif datsel < 2.5:
            print("step")
        elif datsel < 3.5:
            print("sin")
    if datsel < 0.5:
        X = np.exp(10*np.random.rand(N)+1)
    elif datsel < 1.5:
        X = 10*(np.random.rand(N)+np.random.rand(N))
    elif datsel < 2.5: 
        X = np.random.rand(N) - 0.5
        X *= (10-1)*(X>0) + 1
    elif datsel < 3.5: 
        X = 30*np.sin(10*np.random.rand(N)*np.pi)
    return X

def move(a,b,p):
    return a*(1-p)+p*b

N = 40
D = Distrib_1D(N,1000)

fig, ax = plt.subplots()
x = np.arange(1, N)        # x-array 1 to N-1 to plot diff
line, = ax.plot(x, np.sin(x))

Ndata = 10000
#data = (np.sin(np.random.rand(Ndata)*2*np.pi)+1)*(Nbins/2)
Dat = data(Ndata)

def animate(X):
    D.run(data(500))
    Y = 1/(0.2+np.abs(np.diff(D.V)))
    Y *= 0.4
    Y -= 1.0
    line.set_ydata(Y)  # update the data
    #print("min=",np.min(Y)," ; max=",np.max(Y))
    return line,

#Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

#    interval=25, blit=False)
ani = animation.FuncAnimation(fig, animate, Dat, init_func=init,
    interval=20, blit=False)
plt.show()

