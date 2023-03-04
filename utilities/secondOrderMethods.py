#!/usr/bin/env python3
"""
secondOrderMethods module
    Mostly for APPM 5630 at CU Boulder, but others may find it useful too
    The main routine is NewtonsMethod(...)
    Calls firstOrderMethods.py for linesearch and such
    Note: not very well documented, but hopefully simple enough that you can figure
        things out
        I spent about 5 minutes testing this, so it's not very robust code! use at your own risk!
    The main module depends heavily on numpy
    
    Stephen Becker, March 3 2023, stephen.becker@colorado.edu
    
    Released under the Modified BSD License:
Copyright (c) 2023, Stephen Becker. All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the Stephen Becker nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL STEPHEN BECKER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
"""
import numpy as np
from scipy import linalg
import firstOrderMethods

def NewtonsMethod(f,grad,Hess,x0,tol=1e-6,maxIters=1e2,printEvery=1,
                     errorFunction=None, saveHistory=False,stronglyConvex=True):
  """
  NewtonsMethod with either fixed stepsize or backtracking linesearch
  f         is objective function
  grad      returns gradient of objective function
  x0        is initial starting point
  tol       stopping tolerance
  maxIters  maximum number of iterations
  printEvery        prints out information every printEvery steps; set to 0 for quiet
  errorFunction     if provided, will evaluate errorFunction(x) at every iteration
  saveHistory       whether to save function and error history
  stronglyConvex            if True, then assumes Hessian matrix is positive definite

  Outputs:
  x         final iterate
  data      dictionary with detailed info. Keys include: 
    'steps', 'fcnHistory', 'errHistory', 'flag', 'fx'
  """
  x   = np.asarray(x0).copy()
  fx  = f(x)
  t   = 1 # initial guess for stepsize used for linesearch
  maxIters = int(maxIters)
  fcnHistory = []
  errHistory = []

  if stronglyConvex is True:
    HessType = 'pos'
    # For some reason, scipy.linalg.solve doesn't have a semidefinite option
  else:
    HessType = 'sym' # if complex, would need to change to 'her'

  ## Fancy stuff, not essential
  if printEvery == 0  or  np.isinf(printEvery):
    # Users has requested no output
    # The "pprint" function does nothing
    def pprint(*args, **kwargs):
      pass
    display = False
  else:
    display = True
    pprint = print  # pprint is now a synonym for "print" function
    if errorFunction is not None:
      pprint("Iter.  Objective Stepsize  Error")
      pprint("-----  --------- --------  -------")
    else:
      pprint("Iter.  Objective Stepsize")
      pprint("-----  --------- --------")

  ## Main loop
  flag = "Quitting due to reaching max iterations"
  for k in range(maxIters+1):
    ## Actual math:
    g   = grad(x)
    H   = Hess(x)
    p   = - linalg.solve(H,g,assume_a=HessType) # Newton step
    
    xNew,t,fNew, linesearchIter = firstOrderMethods.backtrackingLinesearch(f,x,p,g,1,fx)
    if t == 0:
        flag = "Quitting at iter",k,"since linesearch failed"
        pprint(flag)
        break
    
    ### Now book-keeping, etc.

    # Save data, record error
    if errorFunction is not None:
      err = errorFunction(xNew)
      if saveHistory:
        errHistory.append(err)
    if saveHistory:
      fcnHistory.append(fNew)
    
    if display and (not k % printEvery) :  # modulo
      if errorFunction is not None:
        print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}  {err:.2e}")
      else:
        print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}")
    
    # Check for convergence
    # If we wanted to get fancier, we could have separate tolerance variables
    #   for each kind of check.
    if np.abs(fx-fNew) < tol:
      flag = "Quitting due to stagnating objective value"
      pprint(flag)
      break
    if np.linalg.norm(g) < tol:
      flag = "Quitting due to norm of gradient being small"
      pprint(flag)
      break
    # since xNew - x = stepsize*g, the following check is very similar
    #   to the norm(g) check. The main difference is that it uses both
    #   relative and absolute tolerances; another difference is that it
    #   checks each entry (like l_inf norm) rather than
    #   Euclidean norm.  Suggested by Cooper
    if np.allclose(xNew,x,rtol=tol, atol=1e-3*tol):
      flag = "Quitting due to successive iterates being close together"
      pprint(flag)
      break
    
    # Get ready for next iteration
    fx = fNew
    x  = xNew
  
  data = {'steps':k, 'fcnHistory':np.asarray(fcnHistory), 
          'errHistory':np.asarray(errHistory),
          'flag':flag, 'fx':fx }
  return xNew, data