"""/Users/michaelnorris/Python/anim_test8
A simple example of an animated plot
"""
from density_follower import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

N = 40
D = Density_1D(N,1000)

fig, ax = plt.subplots()
x = np.arange(1, N)        # x-array 1 to N-1 to plot diff
line, = ax.plot(x, np.sin(x))

Ndata = 10000
#data = (np.sin(np.random.rand(Ndata)*2*np.pi)+1)*(Nbins/2)
Dat = data(Ndata)

def animate(X):
    [D.adapt(x) for x in data(500)]
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
def run():
    ani = animation.FuncAnimation(fig, animate, Dat, init_func=init,
        interval=20, blit=False)
    plt.show()

