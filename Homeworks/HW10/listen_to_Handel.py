"""
For HW 10 to demonstrate listening to the "Handel" audio filename
Stephen Becker, 3/18/2017
"""
import numpy as np
import pickle
import scipy.io.wavfile
import scipy.signal as sig

def save_wav(filename, data, Fs=44100):
    # assume we're working with floats
    # rescale to [-1,1]
    _data = 2*data/(data.max() - data.min())
    scipy.io.wavfile.write(filename, int(Fs), _data.astype(np.float32))

def listen():
    y,Fs = pickle.load(open('handel.pkl', 'rb'))
    y = y.ravel() # want a vector, not (n,1) array
    Fs = Fs[0][0] # want a scalar, not a (1,1) array
    sounds = []
    do_plots = True
    if do_plots: import matplotlib.pyplot as plt

    # The original signal
    save_wav('handel.wav', y, Fs)
    sounds.append(('Handel', 'handel.wav'))

    # Naive downsample by a factor of 2
    y2 = y[::2]; fn = 'handel_dec2.wav'
    save_wav(fn, y2, Fs/2)
    sounds.append(('Handel Downsampled by a factor of 2', fn))

    # Naive downsample by a factor of 4
    y4 = y[::4]; fn = 'handel_dec4.wav'
    save_wav(fn, y4, Fs/4)
    sounds.append(('Handel Downsampled by a factor of 4', fn))

    # Anti-alias (lowpass) filter then downsample
    # Use Parks-McClellan to design a lowpass filter with:
    #  * a passband from 0*Nyquist to 0.25*Nyquist
    #  * a stopband from 0.3*Nyquist to 0.5*Nyquist
    filt = sig.remez(100, [0, 0.125, 0.15, 0.5], [1, 0])
    if do_plots: # Plot filt's frequency response
        w, h = sig.freqz(filt)
        fig = plt.figure()
        plt.title('Anti-alias Frequency Response')
        plt.plot(w/np.pi*Fs/2, 20 * np.log10(abs(h)), 'b')
        plt.ylabel('Amplitude [dB]', color='b')
        plt.xlabel('Frequency [Hz]')

    # perform the filtering with the filter we designed above
    yFiltered = sig.lfilter(filt, np.array([1]), y)
    fn = 'handel_lp.wav'
    save_wav(fn, yFiltered, Fs)
    sounds.append(('Handel Lowpass Filtered', fn))

    # It should now be safe to downsample by a factor of 4
    yFiltered4 = yFiltered[::4]; fn = 'handel_lp_dec4.wav'
    save_wav(fn, yFiltered4, Fs/4)
    sounds.append(('Handel Lowpass Filtered and Downsampled by a factor of 4', fn))

    # Print some info
    print('You should play the following files with your preferred media player')
    for desc, fn in sounds:
        print('{}:\n --> {}'.format(desc, fn))

    if do_plots: # estimate PSD
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        f, Pxx = sig.welch(y, fs=Fs, window='barthann', nperseg=1024,
            scaling='density')
        ax1.plot(f, 10*np.log10(Pxx))
        ax1.set_title('Original signal')

        f, Pxx = sig.welch(y4, fs=Fs/4, window='barthann', nperseg=128,
            scaling='density')
        ax2.plot(f, 10*np.log10(Pxx))
        ax2.set_title('Downsampled (x4) (aliased)')

        f, Pxx = sig.welch(yFiltered, fs=Fs, window='barthann', nperseg=1024,
            scaling='density')
        ax3.plot(f, 10*np.log10(Pxx))
        ax3.set_title('Filtered')

        f, Pxx = sig.welch(yFiltered4, fs=Fs/4, window='barthann', nperseg=128,
            scaling='density')
        ax4.plot(f, 10*np.log10(Pxx))
        ax4.set_title('Filtered then Downsampled')

        for ax in (ax1, ax2, ax3, ax4):
            ax.set_xlabel('Frequency [Hz]')
            ax.set_ylabel('Power Spectral Density [dB/Hz]')

    if do_plots: # time-frequency raster
        fig = plt.figure()
        f, t, Sxx = sig.spectrogram(y, fs=Fs, window='barthann', nperseg=512,
            scaling='density')
        plt.pcolormesh(f, t, 10*np.log10(Sxx.T))
        plt.colorbar()
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Time [sec]')

    if do_plots: plt.show()

if __name__ == '__main__':
    listen()
