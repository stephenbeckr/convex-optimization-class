#!/usr/bin/env python3
"""
firstOrderMethods module
    Mostly for APPM 5630 at CU Boulder, but others may find it useful too

    The main routine is gradientDescent(...) which can also do proximal/projected
        gradient descent as well as Nesterov acceleration (i.e., it can do FISTA)

    Also includes lassoSolver(...) which is a wrapper around gradientDescent(...)
        to solve the lasso problem min_x .5||Ax-b||^2 + tau ||x||_1

    Other routines:

        createTestProblem(...) and runAllTestProblems() have some test problems,
            including least-squares, lasso, and logistic regression

        backtrackingLinesearch(...) and LipschitzLinesearch(...) as well as
        powerMethod(...) are utilities

    Note: not very well documented, but hopefully simple enough that you can figure
        things out

    The test problems rely on cvxpy, and the logistic problem relies on scipy.special
    The main module depends heavily on numpy

    Finally, if you run this file from the command line, it will execute the tests

    Features to add:
        (1) adaptive restarts. Done, 4/26/23
        (2) take advantage of functions that give you function value and gradient
            at the same time (since it's often possible to share some computation;
            e.g., f(x) = 1/2||Ax-b||^2, grad(x) = A'*(Ax-b), the residual Ax-b
            only needs to be computed once. [Along with this, make a class for
            fcn/grad computation that records total # of fcn calls]

    Stephen Becker, April 1 2021, stephen.becker@colorado.edu
    Updates (Douglas-Rachford, bookkeeper) April 2023
    TODO:
      incorporate the bookkeeper class into the gradient descent code
        (this makes the actual algorithm itself more clear)
      in gradient descent code, is the function value properly updated? May affect linesearches
    
    Released under the Modified BSD License:

Copyright (c) 2023, Stephen Becker. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the Stephen Becker nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL STEPHEN BECKER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
"""
import numpy as np
from numpy.linalg import norm
from scipy import linalg


def as_column_vec(x):
  """ Input x is of size (n,) or (n,1) or (1,n)
  and output is always of size (n,1). This lets us be consistent """
  return np.reshape( x.ravel(), (-1,1) )

def print_status(prob, x):
  print("Problem status: ", prob.status); 
  print("Used the solver: ",
    prob.solver_stats.solver_name, "with",
    prob.solver_stats.num_iters, "iterations.")
  print("Optimal value: ", prob.value)





def backtrackingLinesearch(f,x,p,grad,t,fx=None,c=1e-6,rho=0.9,linesearchMaxIters = None):
  """"
  Backtracking linesearch, testing with the Armijo Condition
  f    is function to evaluate objective function
  x    is current point
  p    is search direction (often the negative gradient)
  grad is the gradient
  t    is the initial guess for a stepsize
  fx   is f(x) (for the value of x passed in) [optional]
  Returns:
    x,t,fx,iter   where x is new point, t is the stepsize used, fx=f(x)
  """
  if linesearchMaxIters is None:
    linesearchMaxIters = np.log(1e-14)/np.log(rho)
  linesearchMaxIters = int(linesearchMaxIters)
  if fx is None: # don't calculate if it was already calculated
    fx = f(x)  
  xNew = x + t*p  # NOT x-t*p since the negative is already in p
  fNew = f(xNew)
  const = c*np.vdot( grad, p )
  i = 0
  while fNew > fx + t*const  and  i < linesearchMaxIters:
    i += 1
    t *= rho
    xNew = x + t*p
    fNew = f(xNew)
  if fNew > fx + t*const:
    print(f"Warning: linesearch never succeeded after {i:d} iters. Stepsize is {t:.2e}")
    t = 0
  
  return xNew, t, fNew, i



def LipschitzLinesearch(f,x,grad,t,fx=None,prox=None,rho=0.9,linesearchMaxIters = None):
  """"
  Backtracking linesearch, should work if f is Lipschitz
    Note: if we are minimizing f + g via proximal gradient methods,
    then f should be just f, not f+g
  f    is function to evaluate objective function
  x    is current point
  grad is the gradient
  t    is the initial guess for a stepsize
  fx   is f(x) (for the value of x passed in) [optional]
  Returns:
    x,t,fx,iter   where x is new point, t is the stepsize used, fx=f(x)
  """
  if linesearchMaxIters is None:
    linesearchMaxIters = np.log(1e-14)/np.log(rho)
  linesearchMaxIters = int(linesearchMaxIters)
  if fx is None: # don't calculate if it was already calculated
    fx = f(x)
  if prox is None:
    prox = lambda x, stepsize : x

  xNew = prox(x - t*grad,t)
  fNew = f(xNew)
  i = 0
  while fNew > fx + np.vdot(grad,xNew-x)+1/(2*t)*norm(xNew-x)**2  and  i < linesearchMaxIters:
    i += 1
    t *= rho
    xNew = prox(x - t*grad,t)
    fNew = f(xNew)
  if fNew > fx + np.vdot(grad,xNew-x)+1/(2*t)*norm(xNew-x)**2:
    print(f"Warning: LipschitzLinesearch never succeeded after {i:d} iters. Stepsize is {t:.2e}")
    t = 0
  
  return xNew, t, fNew, i


def LipschitzLinesearch_stabler(f,x,g,t,fx=None,gx=None,prox=None,rho=0.9,linesearchMaxIters = None):
  """"
  Backtracking linesearch, should work if f is Lipschitz
    Note: if we are minimizing f + g via proximal gradient methods,
    then f should be just f, not f+g
  f    is function to evaluate objective function
  x    is current point
  g is the gradient (a function)
  t    is the initial guess for a stepsize
  fx   is f(x) (for the value of x passed in) [optional]
  gx   is grad(x) (for the value of x passed in) [optional]
  Returns:
    x,t,fx,iter   where x is new point, t is the stepsize used, fx=f(x)

  More stable version (for numerical rounding errors)
    but requires an additional gradient evaluation
  This is Eq (5.7) in https://amath.colorado.edu/faculty/becker/TFOCS.pdf
    (whereas the other LipschitzLinesearch is eq (5.6) )
    "Templates for Convex Cone Problems with Applications to Sparse Signal Recovery"
    by S. Becker, E. Candès, M. Grant. Mathematical Programming Computation, 3(3) 2011, pp 165–21
  """
  if linesearchMaxIters is None:
    linesearchMaxIters = np.log(1e-14)/np.log(rho)
  linesearchMaxIters = int(linesearchMaxIters)
  if fx is None: # don't calculate if it was already calculated
    fx = f(x)
  if gx is None: # don't calculate if it was already calculated
    gx = g(x)
  if prox is None:
    prox = lambda x, stepsize : x

  xNew = prox(x - t*gx,t)
  fNew = f(xNew)
  gNew = g(xNew)  # objective function
  i = 0
  while np.abs(np.vdot(x-xNew,gNew-gx)) > 1/(2*t)*norm(xNew-x)**2  and  i < linesearchMaxIters:
    i += 1
    t *= rho
    xNew = prox(x - t*gx,t)
    fNew = f(xNew)  # objective function
    gNew = g(xNew)  # gradient
  if  np.abs(np.vdot(x-xNew,gNew-gx)) > 1/(2*t)*norm(xNew-x)**2 :
    print(f"Warning: LipschitzLinesearch_stabler never succeeded after {i:d} iters. Stepsize is {t:.2e}")
    t = 0
  
  return xNew, t, fNew, i



def powerMethod(A, At=None, domainSize=None, x=None, iters=100, tol=1e-6, rng=None, quiet=False): 
  if not callable(A):
    Amatrix = A
    domainSize = Amatrix.shape[1]
    At = lambda x : Amatrix.conj().T@x
    A  = lambda x : Amatrix@x
    print(domainSize)
  elif At is None:
    raise ValueError("If A is a function handle, must supply adjoint fcn via At=... ")
  if x is None:
    if domainSize is None:
      raise ValueError("need domain size or x0 to be specified")
    if rng is None:
        rng = np.random.default_rng()
    x = rng.normal( size=domainSize )
  normalization = norm( x.ravel() ) # Euclidean/Frobenius norm 
  for k in range(iters):
    x = np.real_if_close( At(A(x)) )
    oldNormalization = normalization
    normalization = norm( x.ravel() )
    x /= normalization # do this in-place
    if abs(oldNormalization - normalization)/np.max( [1e-12,normalization] ) < tol:
      if not quiet:
        print("Reached tolerance after",k,"iterations.") 
      break
  return np.sqrt(normalization)



class bookkeeper:
    def __init__(self, printEvery, errorFunction, F, printStepsize = True, tol = 1e-6, 
            tolAbs = None, tolX = None, tolG = None, tolErr = -1, minIter = 1):
        self.printEvery = printEvery
        self.errFcn     = errorFunction
        self.objFcn     = F # objective function
        self.errHist    = []
        self.fcnHist    = []
        if self.printEvery == 0 or np.isinf( self.printEvery ):
            self.display = False
        else:
            self.display = True
        self.printStepsize = printStepsize
        self.stoppingFlag = 'Reached max iterations'
        self.tol = tol               # relative tolerance on objective value decrease
        if tolAbs is None: tolAbs = 1e-3*tol # absolute  tol on objective value
        if tolX is None: tolX = tol  # tolerance for succesive iterates
        if tolG is None: tolG = tol  # tolerance for norm of gradient 
        self.tolX = tolX
        self.tolG = tolG
        self.tolAbs = tolAbs
        self.tolErr = tolErr # if we have an oracle error function...
        self.minIter = minIter # min # of iterations before allowing stopping condition

    def printInitialization(self):
        if self.display:
            if self.objFcn is not None:
                if self.printStepsize:
                    if self.errFcn is not None:
                        print("Iter.  Objective Stepsize  Error")
                        print("-----  --------- --------  -------")
                    else:
                        print("Iter.  Objective Stepsize")
                        print("-----  --------- --------")
                else:
                    if self.errFcn is not None:
                        print("Iter.  Objective Error")
                        print("-----  --------- -------")
                    else:
                        print("Iter.  Objective")
                        print("-----  ---------")
            else:
                if self.printStepsize:
                    if self.errFcn is not None:
                        print("Iter.  Stepsize  Error")
                        print("-----  --------  -------")
                    else:
                        print("Iter.  Stepsize")
                        print("-----  --------")
                else:
                    if self.errFcn is not None:
                        print("Iter.  Error")
                        print("-----  -------")
                    else:
                        print("Iter.  ")
                        print("-----  ")
    def update_and_print(self, x, k, stepsize=None, ignorePrintEvery = False, Fx = None):
        """ x is current iterate, k is stepnumber, stepsize is stepsize """
        if Fx is not None:
            self.fcnHist.append( Fx )
        elif self.objFcn is not None:
            Fx = self.objFcn( x )
            self.fcnHist.append( Fx )
        if self.errFcn is not None:
            err = self.errFcn( x )
            self.errHist.append( err )
        if self.display and ( (not k % self.printEvery) or ignorePrintEvery ):
            if self.objFcn is not None:
                if self.printStepsize and stepsize is not None:
                    if self.errFcn is not None:
                        print(f"{k:5d}  {Fx:7.2e}  {stepsize:6.2e}  {err:.2e}")
                    else:
                        print(f"{k:5d}  {Fx:7.2e}  {stepsize:6.2e}")
                else:
                    if self.errFcn is not None:
                        print(f"{k:5d}  {Fx:7.2e}  {err:.2e}")
                    else:
                        print(f"{k:5d}  {Fx:7.2e}")
            else:
                if self.printStepsize and stepsize is not None:
                    if self.errFcn is not None:
                        print(f"{k:5d}  {stepsize:6.2e}  {err:.2e}")
                    else:
                        print(f"{k:5d}  {stepsize:6.2e}")
                else:
                    if self.errFcn is not None:
                        print(f"{k:5d}  {err:.2e}")
                    else:
                        print(f"{k:5d}")
    
    def finalize(self, x, k, stepsize=None): # fix Fx  
        if self.objFcn:
            fx = self.fcnHist[-1]
        else:
            fx = np.nan
        if self.display:
            self.update_and_print(x,k,stepsize,ignorePrintEvery=True, Fx = fx)
            print('== ', self.stoppingFlag, ' ==')
        # assume that k (steps) is 0-based
        data = {'steps':k+1, 'fcnHistory':np.asarray(self.fcnHist), 
            'errHistory':np.asarray(self.errHist),
            'flag':self.stoppingFlag, 'fx':fx }
        return data
    
    def checkStoppingCondition(self, x, xOld=None, iteration=np.Inf, gradient=None, stepsize = None):
        stop = False
        if iteration > self.minIter:
            if self.objFcn is not None:
                if np.abs( self.fcnHist[-1] - self.fcnHist[-2] ) < self.tol*np.abs(self.fcnHist[-1]) + self.tolAbs:
                    stop = True
                    self.stoppingFlag = "Quitting due to stagnating objective value"
            if self.errFcn is not None:
                if self.errHist[-1] < self.tolErr:
                    stop = True
                    self.stoppingFlag = "Quitting due to error reaching threshold"
            if gradient is not None:
                if np.linalg.norm( gradient.ravel() ) < self.tolG:
                    # Euclidean norm
                    stop = True
                    self.stoppingFlag = "Quitting due to norm of gradient being small"
            if xOld is not None:
                if np.allclose(x,xOld,rtol=self.tolX, atol=1e-3*self.tolX):
                    # Relative and abs tolerance, and uses l_inf norm
                    stop = True
                    self.stoppingFlag = "Quitting due to successive iterates being close together"
            if stepsize is not None:
                if stepsize == 0:
                    stop = True
                    self.stoppingFlag = "Quitting since linesearch failed"
                  
        return stop




# ======= Algorithms ============
def DouglasRachford( prox1, prox2, y0, gamma = 1, F=None,overrelax = 1, tol  = 1e-6,
         maxIters = 500, printEvery = 10, errorFunction = None ):
    """ Douglas Rachford algorithm to minimize F(x) = f1(x) + f2(x)"""
    maxIters = int(maxIters)
    if printEvery is None:
        printEvery = int( maxIters/20 )
    if overrelax < 0 or overrelax > 2:
        raise ValueError('Over-relaxation parameter "overrelax" must be in range (0,2)')
    if gamma <= 0:
        raise ValueError('Scaling gamma must be in range (0,inf)')
    
    book =  bookkeeper( printEvery, errorFunction, F, printStepsize = False, tol=tol )
    book.printInitialization()

      
    y   = np.asarray(y0).copy()
    x   = None
    for k in range(maxIters):
        xOld = x
        x   = prox2(y,gamma)
        z   = prox1( 2*x - y, gamma)
        y  += overrelax*(z-x)

        book.update_and_print( x, k )
        stop = book.checkStoppingCondition( x, xOld, k)
        if stop:
            break
    
    data = book.finalize( x, k )
    return x, data


def gradientDescent(f,grad,x0,prox=None, prox_obj=None,stepsize=None,tol=1e-6,
                    maxIters=1e4,printEvery=None, linesearch=False,
                    stepsizeOptimism = 1.1, errorFunction=None, 
                    ArmijoLinesearch = None, LipschitzStable = True,
                    saveHistory=False,acceleration=True,restart=-5,
                    **kwargs):
  """
  (Proximal) gradient descent with either fixed stepsize or backtracking linesearch
  Minimizes F(x) := f(x) + g(x), where f is differentiable and f has an easy proximity operator
    (if g=0 then this reduces to gradient descent)

  f                 is smooth part of the objective function
  grad              returns gradient of f
  x0                is initial starting point
  prox              proximity operator for a function g,  prox(y,t) = argmin_x g(x) + 1/(2*t)||x-y||^2
  prox_obj          aka g(x), this is when we solve min_x f(x) + g(x)
  stepsize          either a scalar or if None (default) then uses backtracking linesearch
  linesearch        if True then uses backtracking linesearch (default: true if stepsize is None)
  ArmijoLinesearch  if True, uses Armijo backgracking linesearch (default: true, if no prox and no acceleration, otherwise false)
  LipschitzStable   if not using Armijo linesearch, then use the stable (slightly more expensive) linesearch
  tol               stopping tolerance
  maxIters          maximum number of iterations
  printEvery        prints out information every printEvery steps; set to 0 for quiet
  stepsizeOptimism  how much to multiply old stepsize by when guessing new stepsize (linesearch only)
  errorFunction     if provided, will evaluate errorFunction(x) at every iteration
  saveHistory       whether to save function and error history
  acceleration      Nesterov acceleration (default: True)
  restart           How often to restart acceleration; if negative, then adaptive restart

  Outputs:
  x         final iterate
  data      dictionary with detailed info. Keys include: 
    'steps', 'fcnHistory', 'errHistory', 'flag', 'fx'

    Stephen Becker, University of Colorado Boulder, March 2021 and April 2023
  """
  x   = np.asarray(x0).copy()
  
  if stepsize is None:
    t   = 1 # initial guess for stepsize used for linesearch
    linesearch = True
  else:
    t = stepsize
  if maxIters is None: maxIters = 1e4
  maxIters = int(maxIters)
  if restart is None: 
    restart = np.Inf
  else:
    restart = int(restart)

  ## Fancy stuff, not essential
  if printEvery is None:
    printEvery = int( maxIters/20 )
  if printEvery == 0  or  np.isinf(printEvery):
    def pprint(*args, **kwargs):
      pass  # The "pprint" function does nothing
    display = False
  else:
    display = True
    pprint = print
  
  if ArmijoLinesearch is None:
    if (prox is None) and (not acceleration):
      ArmijoLinesearch = True
    else:
      ArmijoLinesearch = False
  
  # Allow both plain gradient descent and proximal gradient descent
  if prox is None:
    prox     = lambda x, stepsize : x
    prox_obj = lambda x : 0
    F    = f
    if linesearch and ArmijoLinesearch:
      pprint("WARNING: Armijo linesearch not recommended for proximal gradient descent")
  else:
    F       = lambda x : f(x) + prox_obj(x)


  if linesearch and acceleration and ArmijoLinesearch:
      pprint("WARNING: Armijo linesearch not recommended for Nesterov acceleration")

  book =  bookkeeper( printEvery, errorFunction, F, printStepsize = True, tol=tol )
  book.printInitialization()

  y   = x.copy() # for Nesterov acceleration, y and x will be different
  g   = grad(x)
  fx  = F(x)
  fy  = fx
  if not np.array_equal( g.shape, x.shape ):
    # this will cause inadvertent broadcasting if we do x - g
    if g.size is not x.size:
      print("g.shape and size are", g.shape, g.size)
      print("x.shape and size are", x.shape, x.size)
      raise ValueError('Output of gradient does not match size of x0')
    # redefine gradient
    print("Warning, redefining size of gradient to match size of x0")
    grad = lambda x : np.reshape( grad(x), x.shape)


  ## Main loop
  kk = 0  # for Nesterov
  linesearchIter = 1
  for k in range(maxIters+1):
    ## Actual math:
    #g   = grad(x)  # Now doing this at end of loop
    
    ### Take the update, either fixed stepsize or via a linesearch
    if not linesearch:
      # Plain update
      xNew = prox(y - t*g,t)
      fNew = F(xNew)
    else: # doing a linesearch
      if linesearchIter == 0:
          # This means we didn't have to backgrack previously, so our guess was likely too conservative
          tPredicted  = stepsizeOptimism*t  # guess for stepsize
      else:
          tPredicted  = t  # use old guess for stepsize

      if ArmijoLinesearch:
          # Not recommended for Acceleration or Proximal methods
          xNew = prox(y - tPredicted*g,tPredicted)  # y = x if not using Nesterov acceleration
          p    = xNew - y  # this reduces to p = -tPredicted*g if prox=I
          if fy is None: fy = F(y)
          xNew,t,fNew,linesearchIter = backtrackingLinesearch(F,y,p,g,1,fy,**kwargs) # t=1. Uses F = f + prox_obj
          t    *= tPredicted # since t was scaled to [0,1]
      elif LipschitzStable:
          xNew,t,fNew,linesearchIter =  LipschitzLinesearch_stabler(f,y,grad,tPredicted,gx=g,prox=prox)
          fNew += prox_obj(xNew) # added 4/26/23, fixing bug
      else:
          # todo, save fy value to save time (and rename fy and Fy)
          # and also if this is not doing Nesterov, then we can pass in fx 
          xNew,t,fNew,linesearchIter = LipschitzLinesearch(f,y,g,tPredicted,prox=prox)
          fNew += prox_obj(xNew)
      
    
    ### Now book-keeping, etc.
    book.update_and_print( xNew, k, Fx = fNew, stepsize=t )
    stop = book.checkStoppingCondition( xNew, xOld=y, iteration=k, stepsize = t, gradient = g)
    if stop:
        break

    
    ### Get ready for next iteration
    if acceleration:
      kk += 1
      if kk > restart: kk = 0
      if restart < 0 and kk > -restart and fNew > np.mean( book.fcnHistory[restart:-1] ): kk = 0 # adaptive restart, 4/26/23
      y = xNew + kk/(kk+3)*(xNew-x) # Nesterov acceleration
      #fy = F(y)
      fy = None  # Not usually needed (except with Armijo search, not usual in Nesterov case), so don't request unless needed
      x  = xNew.copy() # not sure if needed, but just to be safe
    else:
      y  = xNew.copy() # not sure if needed, but just to be safe
      fy = fNew
    ### Request gradient at new point:
    fx = fNew
    g  = grad(y)

  data = book.finalize( xNew, k, stepsize=t )
  return xNew, data


# ======== Algorithms specialized for certain problems ==========
def lassoSolver_DouglasRachford(A,b,tau,At=None,x=None,**kwargs):
  """ not yet tested as of 4/25/23 """
  if not callable(A):
    # A is a matrix
    f     = lambda x : norm(A@x-b)**2/2
    n     = A.shape[1]
    if x is None:
      x = A.conj().T@b # ought to be the right size
    H     = A.conj().T@A
    prox1    = lambda x, t : np.sign(x)*np.maximum( 0, np.fabs(x) - tau*t )
    def prox2(y,t):
      x = linalg.solve( t*H + np.eye(n), y + t* A.conj().T@b, assume_a = 'pos' )
      return x
    F     = lambda x : f(x) + tau*norm(x,ord=1) 
  else:
      raise ValueError('Not currently implemented')
  xNew, data =  DouglasRachford( prox1, prox2, x, F=F, **kwargs )
  return xNew, data

   
def lassoSolver(A,b,tau,At=None,x=None,L=None,**kwargs):
  """
lassoSolver( A, b, tau )
    solves min_x .5||Ax-b||^2 + tau||x||_1
    calling gradientDescent()
    You can pass through extra options here that will be sent to gradientDescent;
    this is just a convenient wrapper that makes the gradient and proximity
    operator for you

    Optional parameters
        At=... must be specified if A is a function handle. Then At
            should be a function handle that computes the adjoint operation of A
        x=... is a starting guess (if not supplied, At(b) will be used)
  """

  if not callable(A):
    # A is a matrix
    f     = lambda x : norm(A@x-b)**2/2
    grad  = lambda x : A.conj().T@( A@x - b )
    n     = A.shape[1]
    if L is None:
      L     = np.linalg.norm(A,ord=2)**2
    if x is None:
      x = A.T@b # ought to be the right size
  else:
    # A is a linear operator
    if At is None:
      raise ValueError('Need to specify the adjoint of A if its an implicit linear operator')
    if x is None:
      x = At(b) # ought to be the right size
    f     = lambda x : norm(A(x)-b)**2/2
    grad  = lambda x : At( A(x) - b )
    if L is None:
      L     = 1.2*powerMethod(A, At=At,x=x, iters=10, tol=1e-3)**2
  
  prox  = lambda x, t : np.sign(x)*np.maximum( 0, np.fabs(x) - tau*t )
  prox_fcn = lambda x : tau*norm(x,ord=1) 

  xNew, data = gradientDescent(f,grad,x,stepsize=1/L,
                  prox=prox, prox_obj=prox_fcn, **kwargs )
  return xNew, data

def createLogisticProblem(A,b,tau=0):
    """ Creates the function/gradient/Hessian for a logistic regression problem,
    assuming data A and labels b, where labels b are +/- 1
    Optionally regularize with tau/2||w||^2 if requested """
    
    import scipy.special
    from functools import partial
    
    n = A.shape[1]
    L     = np.linalg.norm(A,ord=2)**2/4 + tau

    # For logistic function
    def f_logistic_general(w,X=None,y=None):
      """ sum log( 1 + e^{-y x_i^T w} ) """
      ww = as_column_vec(np.asarray(w))  # Python details
      return np.sum( np.logaddexp(-y*(X@ww), 0) ) + tau/2*norm(w)**2

    f = partial(f_logistic_general,X=A,y=as_column_vec(b))

    # For its gradient
    sigmoid = scipy.special.expit   # if we want to avoid overflow warnings

    def gradient_logistic_general(w,X=None,y=None):
      """ uses X and y from parent workspace """
      mu = as_column_vec( sigmoid( -as_column_vec(y)*(X@as_column_vec(np.asarray(w)) ) ) )
      return X.T@(-y*mu).ravel() + tau*w.ravel() # convert from col vector to just 1D array

    grad = partial(gradient_logistic_general,X=A,y=as_column_vec(b))

    # mu    = lambda w : as_column_vec( sigmoid( -as_column_vec(b)*(A@as_column_vec(np.asarray(w)) ) ) )
    # Hess  = lambda x : A.T@((mu(x)*(1-mu))*A) + tau*np.eye(n) # NOT TESTED

    def create_Hessian_logistic(X,y):
      yy=as_column_vec(np.asarray(y))
      def H(w):
        ww = as_column_vec(np.asarray(w))
        mu = as_column_vec( sigmoid( yy*(X@ww) ) )
        s  = mu*(1-mu)
        return X.T@(s * X ) + tau*np.eye(n)  # broadcasts
      return H
    Hess = create_Hessian_logistic(A,b)

    return f, grad, Hess, L

def createTestProblem( problemName, n=10, rng=None, m = None, tau = None):
  """ Creates some standard test problems:
    quadratic/regression, lasso/l1, logistic-regression """

  if rng is None:
    rng   = np.random.default_rng()
  print("Creating test problem for problem type", problemName)
  if type(problemName) == str :
    problemName = problemName.lower()

  if problemName == 'quadratic' or problemName == 0:
    if m is None:
      m = int(1.5*n)
    A     = rng.random((m,n))
    b     = rng.random(m)
    f     = lambda x : norm(A@x-b)**2/2
    grad  = lambda x : A.T@( A@x - b )
    L     = np.linalg.norm(A,ord=2)**2
    xTrue,resids,_,_ = np.linalg.lstsq(A,b,rcond=None)
    fTrue = np.sum(resids)/2
    if m > n:
      nameString = 'quadratic (underdetermined)'
    else:
      nameString = 'quadratic (overdetermined)'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'L':L, 
            'name':nameString, 'n':n, 'prox':None, 'prox_obj':None,'unique_soln': n <= m }
  
  if problemName == 'lasso' or problemName == 1:
    import cvxpy as cvx
    if m is None:
      m = int(1.5*n)
    A     = rng.random((m,n))
    b     = rng.random(m)
    f     = lambda x : norm(A@x-b)**2/2
    grad  = lambda x : A.conj().T@( A@x - b )
    H     = A.conj().T@A
    Hess  = lambda x : H
    L     = np.linalg.norm(A,ord=2)**2
    if tau is None:
      tau = 2
    prox  = lambda x, t : np.sign(x)*np.maximum( 0, np.fabs(x) - tau*t )
    prox_fcn = lambda x : tau*norm(x,ord=1) 

    x     = cvx.Variable(n)
    obj   = cvx.Minimize( cvx.sum_squares(A@x-b)/2 + tau*cvx.norm(x,p=1) )
    prob  = cvx.Problem(obj)
    #highPrecision = {'solver':cvx.ECOS,'max_iters':400,'abstol':1e-13,'reltol':1e-13}
    highPrecision = {'solver':cvx.ECOS,'max_iters':5000,'abstol':1e-16,'reltol':1e-16,'feastol':1e-16,'verbose':False}
    prob.solve(**highPrecision)
    xTrue = x.value 
    fTrue = prob.value
    fTrue = f(xTrue) + prox_fcn(xTrue)

    # Improve on that solution
    xNesterov, data = lassoSolver(A,b,tau,x=xTrue,L=L,acceleration=True,tol=1e-20,linesearch=False,maxIters=1e2,printEvery=0)
    fx = f(xNesterov) + prox_fcn(xNesterov)
    # If we did improve, then use that
    if fx < fTrue:
       #print('Using the first-order refinement of ECOS solution')
       fTrue = fx
       xTrue = xNesterov


    nameString = 'lasso'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'L':L, 'Hess':Hess,
            'name':nameString, 'n':n, 'prox':prox, 'tau':tau, 'prox_obj':prox_fcn,
            'A':A,'b':b,'unique_soln':True}

  if problemName == 'logistic' or problemName == 2:
    import cvxpy as cvx
    if m is None:
      m = int(5*n) # if m is too small, no unique solution
  
    tau   = .001  # make it strongly convex, guarantee unique solution
    A     = rng.random((m,n))  # uniform in [0,1]
    b     = rng.random(m) # usually this is +1 or -1; if not, some of the tricks may not work
    b     = np.sign(b) # force it to be -1 and 1

    f, grad, Hess, L = createLogisticProblem(A,b,tau)

    # Get answer from CVXPY
    x     = cvx.Variable(n)
    #ff    = -cvx.sum(cvx.multiply(b.ravel(), A @ x) - cvx.logistic(A @ x) )  # cvx.logistic(a)=log(1+exp(a))
    ff    = cvx.sum(cvx.logistic(cvx.multiply(-b, A @ x))) + tau*cvx.sum_squares(x)/2
    prob  = cvx.Problem(cvx.Minimize(ff))
    highPrecisionECOS = {'solver':cvx.ECOS,'max_iters':5000,'abstol':1e-15,'reltol':1e-15,'feastol':1e-14,'verbose':False}
    #highPrecisionSCS = {'solver':cvx.SCS,'eps':1e-8,'use_indirect':False,'verbose':False}
    prob.solve(**highPrecisionECOS)
    xTrue = x.value 
    fTrue = prob.value
    # print_status(prob,x) # optional
    nameString = 'logistic'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'Hess':Hess,
            'L':L, 'name':nameString, 'n':n, 'prox':None, 'prox_obj':None,'unique_soln':True}

  if problemName == 'logistic_noCVXPY' or problemName == 3:
    # logistic, but let's manufacture an interpolating solution so we don't have to rely on CVXPY
    # The downside is that there may not be a unique solution
    if m is None:
      m = int(5*n) # if m is too small, no unique solution
    # create a problem that may not have a unique solution, but we at least know f^* = 0
    A     = rng.standard_normal((m,n))
    xTrue = rng.standard_normal((n,))
    b     = np.sign( A@xTrue )
    tau   = 0

    f, grad, Hess, L = createLogisticProblem(A,b,tau)

    fTrue = 0
    # print_status(prob,x) # optional
    nameString = 'logistic, non-unique solution'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'Hess':Hess,
            'L':L, 'name':nameString, 'n':n, 'prox':None, 'prox_obj':None, 'unique_soln':False }

  raise ValueError('The problem type you specified is not implemented')


def runAllTestProblems():
    rng = np.random.default_rng(1)
    import importlib # https://stackoverflow.com/a/14050282 to check if cvxpy exists
    for problemNumber in range(3):
      print(80*'=')

      if ( problemNumber == 0 ) or ( importlib.util.find_spec("cvxpy") is not None ):

          prob = createTestProblem( problemNumber, rng=rng )
          print("Problem type:",prob['name'])
          xTrue = prob['xTrue']
          errFcn= lambda x : norm(x-xTrue)/norm(xTrue)
          x0  = np.zeros(prob['n'])
          L   = prob['L']
          print('')

          if problemNumber == 1:
            # The lasso problem. We can solve via Douglas-Rachford
            print("  (Douglas-Rachford algorithm)")
            xNew,data = lassoSolver_DouglasRachford(prob['A'], prob['b'], prob['tau'],
                            printEvery = 0, tol = 1e-10, maxIters = int(1e3), errorFunction = errFcn )
            print(f"  Error in x: {errFcn(xNew):.2e}, after {data['steps']} steps")
            print("  Stopping flag is:", data['flag'])
            print('')

          for linesearch in (False,True):
            for acceleration in (False,True):
              print("  (Linesearch:",linesearch," Nesterov acceleration:", acceleration,")")
              xNew, data = gradientDescent(prob['f'],prob['grad'],x0,stepsize=1/L,
                          prox=prob['prox'], prox_obj=prob['prox_obj'],
                          errorFunction = errFcn, tol=1e-10, saveHistory=True, printEvery=0,
                          linesearch = linesearch,acceleration=acceleration, restart=100,
                          maxIters=1e4,ArmijoLinesearch = False, LipschitzStable=True)
              print(f"  Error in x: {errFcn(xNew):.2e}, after {data['steps']} steps")
              print("  Stopping flag is:", data['flag'])
              print('')
      else:
          print("Skipping problem number",problemNumber+1, "since it requires CVXPY installation to find reference solution")




if __name__ == "__main__":
    runAllTestProblems()
