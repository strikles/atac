#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for writing music in Python.

@author: khe
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

plt.style.use('seaborn-dark')


def get_piano_notes():
    '''
    Get the frequency in hertz for all keys on a standard piano.

    Returns
    -------
    note_freqs : dict
        Mapping between note name and corresponding frequency.

    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs


def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    '''
    Get pure sine wave. 

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    duration : float
        Time in seconds.
    sample_rate : int, optional
        Wav file sample rate. The default is 44100.
    amplitude : int, optional
        Peak Amplitude. The default is 4096.

    Returns
    -------
    wave : TYPE
        DESCRIPTION.

    '''
    t = np.linspace(0, duration, int(sample_rate*duration))
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave


def apply_overtones(frequency, duration, factor, sample_rate=44100, amplitude=4096):
    '''
    Return fundamental note with overtones applied. 

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    duration : float
        Time in seconds.
    factor : list
        List of floats as fraction of the fundamental amplitude for amplitudes 
        of the overtones.
    sample_rate : int, optional
        Wav file sample rate. The default is 44100.
    amplitude : int, optional
        Peak Amplitude. The default is 4096.

    Returns
    -------
    fundamental : ndarray
        Output note of `float` type.

    '''
    assert abs(1-sum(factor)) < 1e-8
    
    frequencies = np.minimum(np.array([frequency*(x+1) for x in range(len(factor))]), sample_rate//2)
    amplitudes = np.array([amplitude*x for x in factor])
    
    fundamental = get_sine_wave(frequencies[0], duration, sample_rate, amplitudes[0])
    for i in range(1, len(factor)):
        overtone = get_sine_wave(frequencies[i], duration, sample_rate, amplitudes[i])
        fundamental += overtone
    return fundamental


def get_adsr_weights(frequency, duration, length, decay, sustain_level, sample_rate=44100):
    '''
    ADSR(attack, decay, sustain, and release) envelop generator with exponential
    weights applied.

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    duration : float
        Time in seconds.
    length : list
        List of fractions that indicates length of each stage in ADSR.
    decay : list
        List of float for decay factor to be used in each stage for exponential
        weights. 
    sustain_level : float
        Amplitude of `S` stage as a fraction of max amplitude.
    sample_rate : int, optional
        Wav file sample rate. The default is 44100.

    Returns
    -------
    weights : ndarray

    '''
    assert abs(sum(length)-1) < 1e-8
    assert len(length) ==len(decay) == 4
    
    intervals = int(duration*frequency)
    len_A = np.maximum(int(intervals*length[0]),1)
    len_D = np.maximum(int(intervals*length[1]),1)
    len_S = np.maximum(int(intervals*length[2]),1)
    len_R = np.maximum(int(intervals*length[3]),1)
    
    decay_A = decay[0]
    decay_D = decay[1]
    decay_S = decay[2]
    decay_R = decay[3]
    
    A = 1/np.array([(1-decay_A)**n for n in range(len_A)])
    A = A/np.nanmax(A)
    D = np.array([(1-decay_D)**n for n in range(len_D)])
    D = D*(1-sustain_level)+sustain_level
    S = np.array([(1-decay_S)**n for n in range(len_S)])
    S = S*sustain_level
    R = np.array([(1-decay_R)**n for n in range(len_R)])
    R = R*S[-1]
    
    weights = np.concatenate((A,D,S,R))
    smoothing = np.array([0.1*(1-0.1)**n for n in range(5)])
    smoothing = smoothing/np.nansum(smoothing)
    weights = np.convolve(weights, smoothing, mode='same')
    
    weights = np.repeat(weights, int(sample_rate*duration/intervals))
    tail = int(sample_rate*duration-weights.shape[0])
    if tail > 0:
        weights = np.concatenate((weights, weights[-1]-weights[-1]/tail*np.arange(tail)))
    return weights


def apply_pedal(note_values, bar_value):
    '''
    Press and hold the sustain pedal throughout the bar.

    Parameters
    ----------
    note_values : list
        List of note duration.
    bar_value : float
        Duration of a measure in seconds.

    Returns
    -------
    new_values : list
        List of note duration with sustain.

    '''
    assert sum(note_values) % bar_value == 0
    new_values = []
    start = 0
    while True:
        cum_value = np.cumsum(np.array(note_values[start:]))
        end = np.where(cum_value == bar_value)[0][0]
        if end == 0:
            new_values += [note_values[start]]
        else:
            this_bar = np.array(note_values[start:start+end+1])
            new_values += [bar_value-np.sum(this_bar[:i]) for i in range(len(this_bar))]
        start += end+1
        if start == len(note_values):
            break
    return new_values


def get_song_data(music_notes, note_values, bar_value, factor, length,
                  decay, sustain_level, sample_rate=44100, amplitude=4096):
    '''
    Generate song from notes. 

    Parameters
    ----------
    music_notes : list
        List of note names. 
    note_values : list
        List of note duration.
    bar_value: float
        Duration of a bar. 
    factor : list
        Factor to be used to generate overtones.
    length : list
        Stage length to be used to calculate ADSR weights.
    decay : list
        Stage decay to be used to calculate ADSR weights.
    sustain_level : float
        Amplitude of `S` stage as a fraction of max amplitude.
    sample_rate : int, optional
        Wav file sample rate. The default is 44100.
    amplitude : int, optional
        Peak Amplitude. The default is 4096.

    Returns
    -------
    song : ndarray

    '''
    note_freqs = get_piano_notes()
    frequencies = [note_freqs[note] for note in music_notes]
    new_values = apply_pedal(note_values, bar_value)
    duration = int(sum(note_values)*sample_rate)
    end_idx = np.cumsum(np.array(note_values)*sample_rate).astype(int)
    start_idx = np.concatenate(([0], end_idx[:-1]))
    end_idx = np.array([start_idx[i]+new_values[i]*sample_rate for i in range(len(new_values))]).astype(int)
    
    song = np.zeros((duration,))
    for i in range(len(music_notes)):
        this_note = apply_overtones(frequencies[i], new_values[i], factor)
        weights = get_adsr_weights(frequencies[i], new_values[i], length, 
                                   decay, sustain_level)
        song[start_idx[i]:end_idx[i]] += this_note*weights

    song = song*(amplitude/np.max(song))
    return song


def scale():
    # Define scale and piano characteristics
    scale = ['C4','D4','E4','F4','G4','A4','B4','C5']
    note_values = [0.5]*8
    factor = [0.68, 0.26, 0.03, 0.  , 0.03]
    length = [0.01, 0.6, 0.29, 0.1]
    decay = [0.05,0.02,0.005,0.1]
    sustain_level = 0.1

    # Without sustain (each note in separate bar)
    scale_plain = get_song_data(scale, note_values, bar_value=0.5,
                                    factor=factor, length=length, decay=decay, 
                                    sustain_level=sustain_level)
    scale_plain = scale_plain * (4096/np.max(scale_plain))
    wavfile.write('data/scale_plain.wav', 44100, scale_plain.astype(np.int16))

    # With sustain (all note in one bar)
    scale_sustain = get_song_data(scale, note_values, bar_value=4,
                                    factor=factor, length=length, decay=decay, 
                                    sustain_level=sustain_level)
    scale_sustain = scale_sustain * (4096/np.max(scale_sustain))
    wavfile.write('data/scale_sustain.wav', 44100, scale_sustain.astype(np.int16))


def twinkle_sine():
    """
    """
    right_hand_notes = ['C4', 'C4', 'G4', 'G4',
                       'A4', 'A4', 'G4',
                       'F4', 'F4', 'E4', 'E4',
                       'D4', 'D4', 'C4',
                       'G4', 'G4', 'F4', 'F4',
                       'E4', 'E4', 'D4',
                       'G4', 'G4', 'F4', 'F4',
                       'E4', 'E4', 'D4',
                       'C4', 'C4', 'G4', 'G4',
                       'A4', 'A4', 'G4',
                       'F4', 'F4', 'E4', 'E4',
                       'D4', 'D4', 'C4',]
    right_hand_duration = [0.5, 0.5, 0.5, 0.5,
                           0.5, 0.5, 1]*6
    #
    left_hand_notes = ['C3',
                      'A3',
                      'F3',
                      'D3', 'C3',
                      'G3', 'F3',
                      'E3', 'D3',
                      'G3', 'F3',
                      'E3', 'D3',
                      'C3', 'E3', 'G3', 'C4',
                      'A3', 'A3', 'G3',
                      'F3', 'B2', 'E3', 'C3',
                      'D3', 'D3', 'C3']
    #
    left_hand_duration = [2,
                          2,
                          2,
                          1, 1,
                          1, 1,
                          1, 1,
                          1, 1,
                          1, 1,
                          0.5, 0.5, 0.5, 0.5,
                          0.5, 0.5, 1,
                          0.5, 0.5, 0.5, 0.5,
                          0.5, 0.5, 1]
    #
    factor = [0.68, 0.26, 0.03, 0.  , 0.03]
    length = [0.01, 0.6, 0.29, 0.1]
    decay = [0.05,0.02,0.005,0.1]
    sustain_level = 0.1
    #
    right_hand = get_song_data(right_hand_notes, right_hand_duration, 2,
                                     factor, length, decay, sustain_level)
    factor = [0.73, 0.16, 0.06, 0.01, 0.02, 0.01  , 0.01]
    length = [0.01, 0.29, 0.6, 0.1]
    decay = [0.05,0.02,0.005,0.1]
    left_hand = get_song_data(left_hand_notes, left_hand_duration, 2,
                                     factor, length, decay, sustain_level)
    data = left_hand+right_hand
    data = data * (4096/np.max(data))
    #
    wavfile.write('data/twinkle_star.wav', 44100, data.astype(np.int16))


def midle():
    # Get middle C frequency
    note_freqs = get_piano_notes()
    frequency = note_freqs['C4']

    # Pure sine wave
    sine_wave = get_sine_wave(frequency, duration=2, amplitude=2048)
    wavfile.write('data/pure_c.wav', rate=44100, data=sine_wave.astype(np.int16))

    # Load data from wav file
    sample_rate, middle_c = wavfile.read('data/piano_c.wav')

    # Plot sound wave
    plt.plot(middle_c[500:2500])
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sound Wave of Middle C on Piano')
    plt.grid()
    plt.savefig('data/piano_sound_wave.jpg')

    # FFT
    t = np.arange(middle_c.shape[0])
    freq = np.fft.fftfreq(t.shape[-1])*sample_rate
    sp = np.fft.fft(middle_c) 

    # Plot spectrum
    plt.plot(freq, abs(sp.real))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Spectrum of Middle C Recording on Piano')
    plt.xlim((0, 2000))
    plt.grid()
    plt.savefig('data/spectrum.jpg')

    # Get positive frequency
    idx = np.where(freq > 0)[0]
    freq = freq[idx]
    sp = sp[idx]

    # Get dominant frequencies
    sort = np.argsort(-abs(sp.real))[:100]
    dom_freq = freq[sort]

    # Round and calculate amplitude ratio
    freq_ratio = np.round(dom_freq/frequency)
    unique_freq_ratio = np.unique(freq_ratio)
    amp_ratio = abs(sp.real[sort]/np.sum(sp.real[sort]))
    factor = np.zeros((int(unique_freq_ratio[-1]), ))
    for i in range(factor.shape[0]):
        idx = np.where(freq_ratio==i+1)[0]
        factor[i] = np.sum(amp_ratio[idx])
    factor = factor/np.sum(factor)

    # Construct harmonic series
    note = apply_overtones(frequency, duration=2.5, factor=factor)

    # Apply smooth ADSR weights
    weights = get_adsr_weights(frequency, duration=2.5, length=[0.05, 0.25, 0.55, 0.15],
                            decay=[0.075,0.02,0.005,0.1], sustain_level=0.1)

    # Write to file
    data = note*weights
    data = data*(4096/np.max(data)) # Adjusting the Amplitude 
    wavfile.write('data/synthetic_c.wav', sample_rate, data.astype(np.int16))


def consonance():
    note_freqs = get_piano_notes()

    ##############################################################################
    # Perfect Consonance (Octave)
    ##############################################################################
    C4 = get_sine_wave(note_freqs['C4'], 2, amplitude=2048)  # Middle C
    C5 = get_sine_wave(note_freqs['C5'], 2, amplitude=2048)  # C one octave above
    wavfile.write('data/octave.wav', rate=44100, data=((C4+C5)/2).astype(np.int16))

    plt.figure(figsize=(12,4))
    plt.plot(C4[:2500], label='C4')
    plt.plot(C5[:2500], label='C5')
    plt.plot((C4+C5)[:2500], label='Octave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Perfect Consonance (Octave)')
    plt.grid()
    plt.legend()
    plt.savefig('data/octave.jpg')

    ##############################################################################
    # Imperfect Consonance (Major Thirds)
    ##############################################################################
    C4 = get_sine_wave(note_freqs['C4'], 2, amplitude=2048)  # Middle C
    E4 = get_sine_wave(note_freqs['E4'], 2, amplitude=2048)  # E just above
    wavfile.write('data/major_thirds.wav', rate=44100, data=((C4+E4)/2).astype(np.int16))

    plt.figure(figsize=(12,4))
    plt.plot(C4[:2500], label='C4')
    plt.plot(E4[:2500], label='E4')
    plt.plot((C4+E4)[:2500], label='Thirds')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Perfect Consonance (Major Thirds)')
    plt.grid()
    plt.legend()
    plt.savefig('data/major_thirds.jpg')

    ##############################################################################
    # Dissonance (Minor Seconds)
    ##############################################################################
    C4 = get_sine_wave(note_freqs['C4'], 2, amplitude=2048)  # Middle C
    c4 = get_sine_wave(note_freqs['c4'], 2, amplitude=2048)  # C sharp/D flat
    wavfile.write('data/minor_seconds.wav', rate=44100, data=((C4+c4)/2).astype(np.int16))

    plt.figure(figsize=(12,4))
    plt.plot(C4[:2500], label='C4')
    plt.plot(c4[:2500], label='c4')
    plt.plot((C4+c4)[:2500], label='Seconds')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Perfect Consonance (Minor Seconds)')
    plt.grid()
    plt.legend()
    plt.savefig('data/minor_seconds.jpg')