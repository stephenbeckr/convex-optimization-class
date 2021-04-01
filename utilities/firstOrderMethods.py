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

    Stephen Becker, April 1 2021, stephen.becker@colorado.edu
"""
import numpy as np
from numpy.linalg import norm


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
    print(f"Warning: linesearch never succeeded after {i:d} iters. Stepsize is {t:.2e}")
    t = 0
  
  return xNew, t, fNew, i



def powerMethod(A, At=None, domainSize=None, x=None, iters=100, tol=1e-6): 
  if not callable(A):
    Amatrix = A
    domainSize = Amatrix.shape[1]
    At = lambda x : Amatrix.conj().T@x
    A  = lambda x : Amatrix@x
    print(domainSize)
  if x is None:
    if domainSize is None:
      raise ValueError("need domain size or x0 to be specified")
    x = rng.normal( size=domainSize )
  normalization = norm( x.ravel() ) # Euclidean/Frobenius norm 
  for k in range(iters):
    x = np.real_if_close( At(A(x)) )
    oldNormalization = normalization
    normalization = norm( x.ravel() )
    x /= normalization # do this in-place
    if abs(oldNormalization - normalization)/np.max( [1e-12,normalization] ) < tol:
      print("Reached tolerance after",k,"iterations.") 
      break
  return np.sqrt(normalization)



def gradientDescent(f,grad,x0,prox=None, prox_obj=None,stepsize=None,tol=1e-6,
                    maxIters=1e4,printEvery=None, linesearch=False,
                    stepsizeOptimism = 1.1, errorFunction=None, 
                    ArmijoLinesearch = None,
                    saveHistory=False,acceleration=True,restart=500,
                    **kwargs):
  """
  (Proximal) gradient descent with either fixed stepsize or backtracking linesearch

  f         is objective function; we're trying to solve min_x f(x)
  grad      returns gradient of objective function
  x0        is initial starting point
  prox      proximity operator for a function h, 
              prox(y,t) = argmin_x h(x) + 1/(2*t)||x-y||^2
  prox_obj  aka h(x), this is when we solve min_x f(x) + h(x)
  stepsize  either a scalar or if None (default) then uses backtracking linesearch
  linesearch  if True then uses backtracking linesearch (default: true if stepsize is None)
  ArmijoLinesearch  if True, uses Armijo backgracking linesearch (default:
    true, if no prox and no acceleration, otherwise false)
  tol       stopping tolerance
  maxIters  maximum number of iterations
  printEvery        prints out information every printEvery steps; set to 0 for quiet
  stepsizeOptimism  how much to multiply old stepsize by when guessing new stepsize (linesearch only)
  errorFunction     if provided, will evaluate errorFunction(x) at every iteration
  saveHistory       whether to save function and error history
  acceleration      Nesterov acceleration (default: True)
  restart           How often to restart acceleration

  Outputs:
  x         final iterate
  data      dictionary with detailed info. Keys include: 
    'steps', 'fcnHistory', 'errHistory', 'flag', 'fx'

    Stephen Becker, University of Colorado Boulder, March 2021
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
  fcnHistory = []
  errHistory = []

  ## Fancy stuff, not essential
  if printEvery is None:
    printEvery = int( maxIters/20 )
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
  
  if ArmijoLinesearch is None:
    if (prox is None) and (not acceleration):
      ArmijoLinesearch = True
    else:
      ArmijoLinesearch = False

  # Allow both plain gradient descent and proximal gradient descent
  if prox is None:
    prox = lambda x, stepsize : x
    prox_obj = lambda x : 0
    F    = f
    if linesearch and ArmijoLinesearch:
      pprint("WARNING: Armijo linesearch not recommended for proximal gradient descent")
  else:
    F       = lambda x : f(x) + prox_obj(x)

  if linesearch and acceleration and ArmijoLinesearch:
      pprint("WARNING: Armijo linesearch not recommended for Nesterov acceleration")

  y   = x.copy() # for Nesterov acceleration, y and x will be different
  g   = grad(y)
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
  flag = "Quitting due to reaching max iterations"
  kk = 0  # for Nesterov
  linesearchIter = 1
  for k in range(maxIters+1):
    ## Actual math:
    #g   = grad(x)  # Now doing this at end of loop
    
    if linesearch:
      if linesearchIter == 0:
        tPredicted  = stepsizeOptimism*t  # guess for stepsize
      else:
        tPredicted  = t  # use old guess for stepsize

      if ArmijoLinesearch:
        # Not recommended for Acceleration or Proximal methods
        xNew = prox(y - tPredicted*g,tPredicted)  # y = x if not using Nesterov acceleration
        p    = xNew - y  # this reduces to p = -tPredicted*g if prox=I
        xNew,t,fNew,linesearchIter = backtrackingLinesearch(F,y,p,g,1,fy,**kwargs) # t=1
        t    *= tPredicted # since t was scaled to [0,1]
      else:
        # todo, save fy value to save time (and rename fy and Fy)
        xNew,t,fNew,linesearchIter = LipschitzLinesearch(f,y,g,tPredicted,prox=prox)
        fNew += prox_obj(xNew)
      if t == 0:
        flag = "Quitting since linesearch failed"
        pprint("Iter",k,flag)
        break
    else:
      xNew = prox(y - t*g,t)
      fNew = F(xNew)
    
    ### Now book-keeping, etc.

    # Save data, record error
    if errorFunction is not None:
      err = errorFunction(xNew)
      if saveHistory:
        errHistory.append(err)
    if saveHistory:
      fcnHistory.append(fNew)
    
    if display and (not k % printEvery) :  # modulo
      if fNew is None: fNew = f(xNew)
      if errorFunction is not None:
        print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}  {err:.2e}")
      else:
        print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}")
    
    # Check for convergence
    # If we wanted to get fancier, we could have separate tolerance variables
    #   for each kind of check.
    if np.abs(fx-fNew) < tol*np.abs(fx) + 1e-3*tol:
      flag = "Quitting due to stagnating objective value"
      pprint("Iter",k,flag)
      break
    if np.linalg.norm(g) < tol:
      flag = "Quitting due to norm of gradient being small"
      pprint("Iter",k,flag)
      break
    # since xNew - x = stepsize*g, the following check is very similar
    #   to the norm(g) check. The main difference is that it uses both
    #   relative and absolute tolerances; another difference is that it
    #   checks each entry (like l_inf norm) rather than
    #   Euclidean norm.
    if np.allclose(xNew,x,rtol=tol, atol=1e-3*tol):
      flag = "Quitting due to successive iterates being close together"
      pprint("Iter",k,flag)
      break
    
    # Get ready for next iteration
    if acceleration:
      kk += 1
      if kk > restart: kk = 0
      y = xNew + kk/(kk+3)*(xNew-x)
      fy = F(y)
      x  = xNew.copy() # not sure if needed, but just to be safe
    else:
      y = xNew
      if fNew is None: fNew = f(xNew)
      fy = fNew
      x  = xNew
    fx = fNew
    g  = grad(y)


  if display and (k % printEvery) :  # modulo
    if errorFunction is not None:
      print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}  {err:.2e}")
    else:
      print(f"{k:5d}  {fNew:7.2e}  {t:6.2e}")
  if fx is None: fx = f(xNew)
  data = {'steps':k, 'fcnHistory':np.asarray(fcnHistory), 
          'errHistory':np.asarray(errHistory),
          'flag':flag, 'fx':fx }
  return xNew, data



def lassoSolver(A,b,tau,At=None,x=None,**kwargs):
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
    # Get a rough estimate, and make it a bit larger to account for uncertainty:
    L     = 1.2*powerMethod(A, domainSize=n, x=x, iters=10, tol=1e-3)**2
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
    L     = 1.2*powerMethod(A, At=At,x=x, iters=10, tol=1e-3)**2
  
  prox  = lambda x, t : np.sign(x)*np.maximum( 0, np.fabs(x) - tau*t )
  prox_fcn = lambda x : tau*norm(x,ord=1) 

  xNew, data = gradientDescent(f,grad,x,stepsize=1/L,
                  prox=prox, prox_obj=prox_fcn, **kwargs )
  return xNew, data


def createTestProblem( problemName, n=10, rng=None, m = None, tau = None):

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
            'name':nameString, 'n':n, 'prox':None, 'prox_obj':None }
  
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
    highPrecision = {'solver':cvx.ECOS,'max_iters':400,'abstol':1e-13,'reltol':1e-13}
    prob.solve(**highPrecision)
    xTrue = x.value 
    fTrue = prob.value
    nameString = 'lasso'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'L':L, 'Hess':Hess,
            'name':nameString, 'n':n, 'prox':prox, 'tau':tau, 'prox_obj':prox_fcn,
            'A':A,'b':b}

  if problemName == 'logistic' or problemName == 2:
    import scipy.special
    import cvxpy as cvx
    if m is None:
      m = int(5*n) # if m is too small, no unique solution
    tau   = .001  # make it strongly convex, guarantee unique solution
    A     = rng.random((m,n))
    b     = rng.random(m)
    L     = np.linalg.norm(A,ord=2)**2/4 + tau

    # For logistic function
    def f_logistic_general(w,X=None,y=None):
      """ sum log( 1 + e^{-y x_i^T w} ) """
      ww = as_column_vec(np.asarray(w))  # Python details
      return np.sum( np.logaddexp(-y*(X@ww), 0) ) + tau/2*norm(w)**2

    from functools import partial
    f = partial(f_logistic_general,X=A,y=as_column_vec(b))

    # For its gradient
    import scipy.special
    sigmoid = scipy.special.expit   # if we want to avoid overflow warnings

    def gradient_logistic_general(w,X=None,y=None):
      """ uses X and y from parent workspace """
      mu = as_column_vec( sigmoid( -as_column_vec(y)*(X@as_column_vec(np.asarray(w)) ) ) )
      return X.T@(-y*mu).ravel() + tau*w.ravel() # convert from col vector to just 1D array

    from functools import partial
    grad = partial(gradient_logistic_general,X=A,y=as_column_vec(b))

    mu    = lambda w : as_column_vec( sigmoid( -as_column_vec(b)*(A@as_column_vec(np.asarray(w)) ) ) )
    Hess  = lambda x : A.T@((mu(x)*(1-mu))*A) + tau*np.eye(n) # NOT TESTED

    # Get answer from CVXPY
    x     = cvx.Variable(n)
    #ff    = -cvx.sum(cvx.multiply(b.ravel(), A @ x) - cvx.logistic(A @ x) )  # cvx.logistic(a)=log(1+exp(a))
    ff    = cvx.sum(cvx.logistic(cvx.multiply(-b, A @ x))) + tau*cvx.sum_squares(x)/2
    prob  = cvx.Problem(cvx.Minimize(ff))
    highPrecisionECOS = {'solver':cvx.ECOS,'max_iters':1000,'abstol':1e-13,'reltol':1e-13,'verbose':False}
    highPrecisionSCS = {'solver':cvx.SCS,'eps':1e-8,'use_indirect':False,'verbose':False}
    prob.solve(**highPrecisionECOS)
    xTrue = x.value 
    fTrue = prob.value
    # print_status(prob,x) # optional
    nameString = 'logistic'
    return {'f':f, 'grad':grad, 'xTrue':xTrue, 'fTrue':fTrue, 'Hess':Hess,
            'L':L, 'name':nameString, 'n':n, 'prox':None, 'prox_obj':None}

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

          for linesearch in (False,True):
            for acceleration in (False,True):
              print("  (Linesearch:",linesearch," Nesterov acceleration:", acceleration,")")
              xNew, data = gradientDescent(prob['f'],prob['grad'],x0,stepsize=1/L,
                          prox=prob['prox'], prox_obj=prob['prox_obj'],
                          errorFunction = errFcn, tol=1e-15, saveHistory=True, printEvery=0,
                          linesearch = linesearch,acceleration=acceleration,restart=100,
                          maxIters=1e4)
              print(f"  Error in x: {errFcn(xNew):.2e}, after {data['steps']} steps")
              print('')
      else:
          print("Skipping problem number",problemNumber+1, "since it requires CVXPY installation to find reference solution")




if __name__ == "__main__":
    runAllTestProblems()
