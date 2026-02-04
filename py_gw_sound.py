#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 08:25:12 2026

@author: chrs
"""
from pesummary.gw.fetch import fetch_open_samples, fetch_open_strain
import matplotlib.pyplot as plt

# Next we generate the plus and cross polarizations in the time domain for the
# maximum likelihood sample
delta_t = 1. / 4096
f_low = 20.
approximant = "SEOBNRv4PHM"


probe = 'GW250114_082203-v1'
# probe = 'GW170817-v3'
# # First we download and read the publically available posterior samples
f = fetch_open_samples(probe)
f_samples = f.samples_dict
EOB2 = f_samples
ht2 = EOB2.maxL_td_waveform(approximant, delta_t, f_low, f_ref=f_low, project="H1")

fig = plt.figure()
plt.plot(ht2.times, ht2)



# WORKING data set
data = fetch_open_samples("GW150914")
samples = data.samples_dict
EOB = samples["C01:SEOBNRv4PHM"] 
approximant = "SEOBNRv4PHM"


ht = EOB.maxL_td_waveform(approximant, delta_t, f_low, f_ref=f_low, project="L1")


fig = plt.figure()
plt.plot(ht.times, ht)


# TEST this later => unpack error?
# path_to_directory = fetch_open_samples(
#     "GW190412", catalog="GWTC-2", unpack=True, read_file=False,
#     delete_on_exit=False, outdir="./"
# )


# # raw STRAIN data only - needs filering etc, not very usefull right away
# path = fetch_open_strain(
#     "GW190521", channel='L1:GWOSC-16KHZ_R1_STRAIN')

# fig = plt.figure()
# plt.plot(path)


# NEXT
# convert to audio ranges and test how it sounds
# use librosa to generate spectrogram
# use windows and filtering to generate different samples