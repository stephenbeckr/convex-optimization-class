"""
This is just a simple script to help test the python routines and ensure they
match the MATLAB routines.
"""
import numpy as np
import scipy, scipy.io
import pickle

from python_functions import *

def convert_handel():
    import pickle
    mat = scipy.io.loadmat('handel.mat')
    y = mat['y']
    Fs = mat['Fs']

    pickle.dump((y,Fs), open('handel.pkl', 'wb'))

    # load with
    y,Fs = pickle.load(open('handel.pkl', 'rb'))

def test_project_l1():
    x = np.random.randn(10,1)
    mat = scipy.io.loadmat('x.mat')
    x = mat['x'].ravel()

    y = project_l1(x, 1)

def test_STDCT():
    mat = scipy.io.loadmat('x.mat')
    x = mat['x'].ravel()
    coeff_ref = mat['coeff'].ravel()
    win_ref = mat['win'].ravel()

    coeff, win = forwardShortTimeDCT(x)

    xrec = adjointShortTimeDCT(coeff, win, x.size)
    print(np.linalg.norm(x-xrec))

def test_my_upsample():
    x = np.random.randn(10, 2)
    sampleSet = np.array([0, 2, 3, 4])
    y = x[sampleSet]
    print(x)
    print(my_upsample(y, sampleSet, x.size))

if __name__ == '__main__':
    #convert_handel()
    #test_project_l1()
    #test_STDCT()
    test_my_upsample()
