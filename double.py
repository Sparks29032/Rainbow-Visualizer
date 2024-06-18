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


def angle(v1, v2):
  cp = v1[0] * v2[1] - v1[1] * v2[0]
  sa = cp / np.sqrt(v1[0]**2+v1[1]**2) / np.sqrt(v2[0]**2+v2[1]**2)
  return np.arcsin(sa)


def rotate(v, t):
  vr = [0, 0]
  vr[0] = np.cos(t) * v[0] - np.sin(t) * v[1]
  vr[1] = np.sin(t) * v[0] + np.cos(t) * v[1]
  return np.array(vr)


def update(val):
  h = hslider.val

  ax[0].clear()
  ax[1].clear()
  ax[0].add_patch(drop)
  
  for pair in reversed(colors):
    n = pair[0]
    c = pair[1]
    d = 0.0001*r

    # Incoming beam
    y = h
    x = -np.sqrt(r**2-y**2)
    ax[0].plot([-wz*r, x], [y, y], c='k')

    # Raindrop beam
    pos = np.array([x, y])
    alpha = angle(pos, [-x - wz*r, 0])
    beta = np.arcsin(np.sin(alpha) / n)
    vel = rotate(-pos, beta)
    dx = vel[0] / np.abs(vel[0]) * d
    dy = vel[1] / np.abs(vel[0]) * d
    x = x + dx
    y = y + dy
    X = [x]
    Y = [y]
    while x**2 + y**2 <= (r + d)**2:
      x += dx
      y += dy
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # First reflected beam
    pos = np.array([x, y])
    vel = rotate(-vel, 2*beta)
    dx = vel[0] / np.abs(vel[0]) * d
    dy = vel[1] / np.abs(vel[0]) * d
    x = x + dx
    y = y + dy
    X = [x]
    Y = [y]
    while x**2 + y**2 <= (r + d)**2:
      x += dx
      y += dy
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Second reflected beam
    pos = np.array([x, y])
    vel = rotate(-vel, 2*beta)
    dx = vel[0] / np.abs(vel[0]) * d
    dy = vel[1] / np.abs(vel[0]) * d
    x = x + dx
    y = y + dy
    X = [x]
    Y = [y]
    while x**2 + y**2 <= (r + 2*d)**2:
      x += dx
      y += dy
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Outgoing beam
    pos = np.array([x, y])
    vel = rotate(pos, -alpha)
    dx = vel[0] / np.abs(vel[0]) * d
    dy = vel[1] / np.abs(vel[0]) * d
    x = x + dx
    y = y + dy
    X = [x]
    Y = [y]
    while abs(x) < wz * r:
      x += dx
      y += dy
      X.append(x)
      Y.append(y)
    ax[0].plot(X, Y, c=c, linewidth=1)

    # Height-Angle relation
    def f_alpha(hc):
      return np.arctan(hc / np.sqrt(r**2 - hc**2))
    def f_beta(hc):
      return np.arcsin(np.sin(f_alpha(hc)) / n)
    H = np.linspace(-l*r, l*r, int(1/d))
    ax[1].plot(H, (-np.pi/2 + 6*f_beta(H) - 2*f_alpha(H)) % np.pi - np.pi/2, c=c, linewidth=1)
    ax[1].scatter([h], [np.arctan(dy / dx)], c=c, s=1)

  ax[0].set_xlim(-wz*r, wz*r)
  ax[0].set_ylim(-wz*r, wz*r)

hslider.on_changed(update)
plt.show()
