import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots(1, 2)

colors = [(1.331, 'red'), (1.332, 'orange'), (1.333, 'yellow'), (1.334, 'green'), (1.336, 'blue'), (1.338, 'purple')]

# Spherical raindrop
r = 1
wz = 1.5
drop = plt.Circle((0, 0), radius=r, color='cyan')

fig.subplots_adjust(bottom=0.25)
axs = fig.add_axes([0.25, 0.1, 0.65, 0.03])
l = 0.9999
hslider = Slider(ax=axs, label='Beam Height', valmin=-l*r, valmax=l*r, valinit=0)

def update(val):
  h = hslider.val

  ax[0].clear()
  ax[1].clear()
  ax[0].add_patch(drop)
  
  for pair in reversed(colors):
    n = pair[0]
    c = pair[1]
    dx = 0.0001*r

    # Incoming beam
    y = h
    x = -np.sqrt(r**2-y**2)
    ax[0].plot([-wz*r, x], [y, y], c='k')

    # Raindrop beam
    alpha = np.arctan(-y/x)
    beta = np.arcsin(np.sin(alpha)/n)
    slope_in = -np.tan(alpha - beta)
    X = [x]
    Y = [y]
    while x**2 + y**2 < (r + dx)**2:
      x += dx
      y += slope_in*dx
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Reflected beam
    gamma = np.arctan(y/x)
    slope_ref = np.tan(beta + gamma)
    x = x - dx
    y = y - dx*slope_ref
    X = [x]
    Y = [y]
    while x**2 + y**2 < (r + dx)**2:
      x -= dx
      y -= slope_ref*dx
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Outgoing beam
    delta = np.arctan(-y/x)
    slope_out = -np.tan(alpha + delta)
    X = [x]
    Y = [y]
    while x > -wz*r:
      x -= dx
      y -= slope_out*dx
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Height-Angle relation
    def f_alpha(hc):
      return np.arctan(hc / np.sqrt(r**2 - hc**2))
    def f_beta(hc):
      return np.arcsin(np.sin(f_alpha(hc)) / n)
    H = np.linspace(-l*r, l*r, int(1/dx))
    ax[1].plot(H, 4*f_beta(H) - 2*f_alpha(H), c=c, linewidth=1)
    ax[1].scatter([h], [np.arctan(slope_out)], c=c, s=1)

  ax[0].set_xlim(-wz*r, wz*r)
  ax[0].set_ylim(-wz*r, wz*r)

hslider.on_changed(update)
plt.show()
