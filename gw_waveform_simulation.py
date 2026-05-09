#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 06:08:47 2026

@author: chrs

this is aplayground to use a real gravitational wave as a basis and find a way to emulate a similar signal for later use in music

train of thought:
    - use base gw
    - decompose in some parameters (such as Fourier)
    - write emulation fuctions including (ADSR) envelopes which would be suitable for sound synthesis

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert

t, gw = np.load("GW150914_waveform.npy")

t[-1] - t[0]

plt.figure()
plt.plot(t, gw)

# introduce a new, normalized to 1 x-basis
x = np.linspace(0, 1, len(t))

# normalize signal to 1
gw_norm = (gw - gw.min()) / (gw.max() - gw.min())  
gw_norm -= np.mean(gw_norm)

plt.figure()
plt.plot(x, gw_norm)
plt.xlim(0.6,0.9)

# emulate simple sine with x-dependent phase

def emulate_gw(t, a,b, A = 1, f_base=440, f_range=50, delta=0):
    '''emulate a very basic GW signal -not scientifically accurate'''
    f_prog = (a * f_range*x**2 + b * f_range*x)
    f = f_base + f_prog
    phi = 2*np.pi * (x*f) + delta 
    y = A * np.sin(phi)
    return y, phi


def emulate_gw_2(t, a=10, b=2, A=1, f0=30, delta=0):

    dt = t[1] - t[0]

    # nonlinear chirp law
    tau = (t - t.min()) / (t.max() - t.min())

    f = f0 + a*tau**3 + b*tau**6

    # integrate frequency -> phase
    phi = 2*np.pi * np.cumsum(f) * dt + delta

    # simple amplitude growth
    amp = A * (0.2 + tau**2)

    y = amp * np.sin(phi)

    return y, phi

y_sim, phi = emulate_gw_2(x, a= 76, b = 40, f0 = 15, delta=2.8)

# base_T = 1 /440

plt.plot(x, y_sim/5)
plt.plot(x, gw_norm-0.5)
plt.xlim(0, 0.85)


# DEcomposition



analytic = hilbert(gw_norm)

amplitude = np.abs(analytic)

phase = np.unwrap(np.angle(analytic))

dt = x[1] - x[0]

inst_freq = np.gradient(phase, dt) / (2*np.pi)

plt.figure(figsize=(10,6))

plt.subplot(311)
plt.plot(x, gw_norm)
plt.title("Waveform")

plt.subplot(312)
plt.plot(x, amplitude)
plt.title("Amplitude Envelope")

plt.subplot(313)
plt.plot(x, inst_freq)
plt.title("Instantaneous Frequency")

plt.tight_layout()
plt.show()

plt.figure()
plt.plot(x[:2600], inst_freq[:2600])


inst_freq[inst_freq<= 0] = 1

np.min(inst_freq)

# possible fit model
def f_fit_inspiral(t, t_c=0.8, a=1, p=3):
    '''a rather simple inspiral approximation model'''
    f = a / (t_c - t)**p
    return f

plt.plot(x, f_fit_inspiral(x))

from scipy.optimize import curve_fit


popt, pcov = curve_fit(f_fit_inspiral, x[:2650], inst_freq[:2650])

plt.figure()
plt.plot(x, inst_freq, "or")
plt.plot(x, f_fit_inspiral(x,*popt))
plt.xlim(0,0.85)
plt.ylim(0,500)



