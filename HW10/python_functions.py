import numpy as np
import scipy.sparse, scipy.fftpack

def project_l1(x, tau=1.):
    """
    project_l1(x, tau) -> y
      projects x onto the scaled l1 ball, ||x||_1 <= tau
      If tau is not provided, the default is tau = 1.

    Stephen Becker and Emmanuel Candes, 2009/2010.
    Crucial bug fix: 3/17/2017, SRB
    """
    absx = np.abs(x)
    s = np.sort(absx)[::-1] # sort in descending order
    cs = np.cumsum(s)

    if cs[-1] <= tau:
        # x is already feasible, so no thresholding needed
        return x

    # Check some "discrete" levels of shrinkage, e.g. [s(2:end),0]
    # This lets us discover which indices will be nonzero
    n = x.size
    i_tau = np.where(cs -
        np.arange(1,n+1)*np.concatenate((s[1:],0), axis=None) >= tau)[0][0]

    # Now that we know which indices are involved, it's a very simple problem
    thresh = (cs[i_tau]-tau) / (i_tau+1)

    # Shrink x by the amount "thresh"
    return np.sign(x)*np.maximum(absx - thresh, 0)

def forwardShortTimeDCT(y, win=None):
    """
    forwardShortTimeDCT(y, win=None) -> coeff (, win)

    Applies the Modified DCT to the signal y
    This is a linear function.
    Assumes y is a vector of length N
    This code then uses a lapped (50% overlapping)
    DCT on segments of y of length blockSize.

    Note: this function zero-pads y to be an even multiple of blockSize.

    An example window that we recommend, so that the transpose of this
    function is its pseudo-inverse is

    win = np.sin(np.pi*(np.arange(1,blockSize+1)+0.5)/blockSize)
    (a typical value of blockSize = 1024)

    On input, if win is not specified, we return (coeff, win) so the
    caller has access to the window we used.

    This satisfies the Princen-Bradley conditions, meaning that we can
    guarantee  win**2+np.roll(win, int(blockSize/2))**2 == 1.

    Stephen Becker, 3/18/2017
    See also adjointShortTimeDCT
    """
    # Make a window if not provided by the user
    if win is None:
        blockSize = 1024
        win = np.sin(np.pi*(np.arange(1,blockSize+1)+0.5)/blockSize)
        return_win = True
    else:
        blockSize = win.size
        return_win = False

    # Zero-pad y so it is a multiple of blockSize
    N = y.size
    nBlocks = int(np.ceil(float(N)/blockSize))
    y = np.concatenate((y, np.zeros(nBlocks*blockSize-N)))

    # Apply DCT to aligned blocks
    Win = scipy.sparse.spdiags(win, [0], blockSize, blockSize)
    Y = np.reshape(y, (blockSize, nBlocks), order='f')
    C = scipy.fftpack.dct(Win*Y, axis=0, norm='ortho')

    # Apply DCT to 50% shifted blockSize
    Y = np.reshape(np.roll(y, int(-blockSize/2)), (blockSize, nBlocks),
        order='f')
    C2 = scipy.fftpack.dct(Win*Y, axis=0, norm='ortho')

    coeff = np.concatenate((C.ravel(order='f'), C2.ravel(order='f')))

    if return_win: return coeff, win
    else: return coeff

def adjointShortTimeDCT(coeff, win, Ntrue=None):
    """
    adjointShortTimeDCT(coeff, win, Ntrue=None) -> y

    Applies the adjoint/transpose Modified DCT to the coefficients coeff.
    This is also the pseudo-inverse of the forward MDCT.

    If Ntrue=N_original, where N_original is the original length of
    the signal y (i.e., before zero-padding in forwardShortTimeDCT),
    we truncate the padded zeros and return the original y.

    See forwardShortTimeDCT for an example of the window win.

    Stephen Becker, 3/18/2017
    See also forwardShortTimeDCT
    """
    if coeff.size % 2:
        raise ValueError("""coeff should have an even number of elements.
            Did you compute coeff with forwardShortTimeDCT?""")
    N = int(coeff.size/2)

    blockSize = win.size
    nBlocks = int(np.ceil(float(N)/blockSize))

    if Ntrue is not None and Ntrue > N:
        raise ValueError("""The specified value of Ntrue ({}) is too big
            for the number of coefficients in coeff ({})""".format(
            Ntrue, N))

    Win = scipy.sparse.spdiags(win, [0], blockSize, blockSize)

    C = np.reshape(coeff[0:N], (blockSize, nBlocks), order='f')
    Y = Win*scipy.fftpack.idct(C, axis=0, norm='ortho')
    y = Y.ravel(order='f')

    C2 = np.reshape(coeff[N:], (blockSize, nBlocks), order='f')
    Y2 = Win*scipy.fftpack.idct(C2, axis=0, norm='ortho')
    y2 = np.roll(Y2.ravel(order='f'), int(blockSize/2))
    y += y2

    if Ntrue:
        y = y[0:Ntrue]

    return y

def my_upsample(y, sampleSet, n):
    """
    my_upsample(y, sampleSet, n) -> x
    Returns x of length n such that x[sampleSet] = y
    """
    if y.ndim == 1:
        x = np.zeros(n)
        x[sampleSet] = y
    else:
        x = np.zeros((n, y.shape[1]))
        x[sampleSet,:] = y
    return x
