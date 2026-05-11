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
from scipy.optimize import curve_fit


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

# def emulate_gw(t, a,b, A = 1, f_base=440, f_range=50, delta=0):
#     '''emulate a very basic GW signal -not scientifically accurate'''
#     f_prog = (a * f_range*x**2 + b * f_range*x)
#     f = f_base + f_prog
#     phi = 2*np.pi * (x*f) + delta 
#     y = A * np.sin(phi)
#     return y, phi


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
def f_fit_inspiral(t, t_c=0.82, a=1, p=3, b=1, q=2):
    '''a rather simple inspiral approximation model'''
    f = a / (t_c - t)**p + b / (t_c - t)**q 
    return f

plt.plot(x, f_fit_inspiral(x))
plt.ylim(0, 2000)

popt, pcov, = curve_fit(f_fit_inspiral, x[:2600], inst_freq[:2600])

plt.figure()
plt.plot(x, inst_freq, "or")
plt.plot(x, f_fit_inspiral(x,*popt))
plt.xlim(0.2,0.9)
plt.ylim(0,400)


# plot error
plt.figure()
plt.plot(inst_freq - f_fit_inspiral(x,*popt))
plt.ylim(2,-2)




# find t_c from fitted amplitude
t_c_pos = np.argmax(amplitude)
t_c_fit = x[np.argmax(amplitude)]

f_fitted_all = f_fit_inspiral(x,*popt)

# get the index where the fitted signal is NaN => estimated t_c?
f_nan = np.where(np.isnan(f_fitted_all))[0][0]


# get the highest pitch at the merger
np.max(f_fitted_all[0:f_nan-23])
np.mean(f_fitted_all[0:int(len(f_fitted_all)/2)])

# maybe alter t_c from fit here or don't fit t_c in the first place...just use estimate from amplitude?

# build a GW emulation with fitted frequency (chirp/inspiral only)

def sig_merger(t, f, A=1, f0=30, delta=0):

    dt = t[1] - t[0]

    # # nonlinear chirp law
    tau = (t - t.min()) / (t.max() - t.min())

    # f = f0 + a*tau**3 + b*tau**6

    # integrate frequency -> phase
    phi = 2*np.pi * np.cumsum(f) * dt + delta

    # simple amplitude growth
    amp = A * (0.25 + 0.4 * tau**2)

    y_m = amp * np.sin(phi)

    return y_m

plt.figure()
plt.plot(x, gw_norm)
plt.plot(x[:t_c_pos], sig_merger(x[:t_c_pos], f_fit_inspiral(x[:t_c_pos],*popt), delta=-4))
plt.xlim(0.5, 0.83)


def f_ring_down(t):
    f_r = 1
    return f_r

def sig_ring_down(t, t_c):
    y_r = 1
    return y_r
