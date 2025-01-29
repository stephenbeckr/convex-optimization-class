
import numpy as np # np.array (and used internally in cvxpy)
import cvxpy as cvx
import argparse
import time

def get_vars():
   A = np.array([[1, 6,11, 5,10, 4, 9, 3, 8, 2],
                 [2, 7, 1, 6,11, 5,10, 4, 9, 3],
                 [3, 8, 2, 7, 1, 6,11, 5,10, 4],
                 [4, 9, 3, 8, 2, 7, 1, 6,11, 5],
                 [5,10, 4, 9, 3, 8, 2, 7, 1, 6]])

   y = np.array([1,2,3,4,5]).T

   return A, y

def print_status(prob, x):
   print("Problem status: ", prob.status)
   print("Optimal value:  ", prob.value)
   print("Optimal var:\n", x.value)


def problem1():
   A, y = get_vars()
   x = cvx.Variable(10) # column vector with 10 elements
   
   obj = cvx.Minimize(cvx.norm(x)) # cvx.norm defaults to the 2-norm
   constraints = [cvx.norm(A*x-y) <= 0.1] # specify a list of constraints

   prob = cvx.Problem(obj, constraints)
   prob.solve()
   
   print_status(prob, x)

def problem2():
   A, y = get_vars()
   x = cvx.Variable(10)
   
   obj = cvx.Minimize(cvx.norm(x)**2) # cvxpy objects implement the standard python ops
   constraints = [cvx.norm(A*x-y) <= 0.1]

   prob = cvx.Problem(obj, constraints)
   prob.solve()

   print_status(prob, x)

def problem3():
   A, y = get_vars()
   x = cvx.Variable(10)
   
   obj = cvx.Minimize(cvx.norm(x, p=1))
   constraints = [cvx.norm(A*x-y) <= 0.1]

   prob = cvx.Problem(obj, constraints)
   prob.solve()

   print_status(prob, x)

def problem4():
   def get_problem1_dual_value():
      obj = cvx.Minimize(cvx.norm(x))
      constraints = [cvx.norm(A*x-y) <= 0.1]

      prob = cvx.Problem(obj, constraints)
      prob.solve()
      
      return constraints[0].dual_value
   
   A, y = get_vars()
   x = cvx.Variable(10)
   
   # resolve problem 1 and return dual value for the constraint
   l = get_problem1_dual_value()
   print("dual variable: ", l)
   
   obj = cvx.Minimize(cvx.norm(x) + l*cvx.norm(A*x-y))
   
   prob = cvx.Problem(obj)
   prob.solve()
   
   # note that the solution is the same, but the optimal value is different,
   # since for problem 1 we form the Lagrangian \|x\|_2 + \lambda(\|Ax-y\|_2-0.1)
   print_status(prob, x)

   # the optimal value for problem 1 should be
   print("problem 1 optimal value: ", prob.value - 0.1*l)


def problem5():
   A, y = get_vars()
   x = cvx.Variable(5)
   ones = np.ones((10,1))

   obj = cvx.Minimize(sum(cvx.norm(A-x*ones.T, axis=0))) # cvx.norm behaves like np.linalg.norm

   prob = cvx.Problem(obj)
   prob.solve()

   print_status(prob, x)

def problem6():
   A, y = get_vars()
   x = cvx.Variable(5)
   ones = np.ones((10,1))
   
   obj = cvx.Minimize(cvx.norm(A-x*ones.T))

   prob = cvx.Problem(obj)
   #prob.solve(verbose=True) # ~1e-7 duality gap, but CVXOPT gets a singular KKT system
   prob.solve(verbose=True, kktsolver='robust')
   #prob.solve(verbose=True, solver='SCS')

   print_status(prob, x)
  
def problem7():
   A, y = get_vars()
   X = cvx.Variable(5,10)

   obj = cvx.Minimize(cvx.norm(X-A, 'fro'))
   constraints = [ np.ones((5,)).T*X*np.ones((10,)) == 1. ]

   prob = cvx.Problem(obj, constraints)
   prob.solve()

   print_status(prob, X)

def problem8():
   A, y = get_vars()
   B = A[:,0:5]
   X = cvx.Variable(5,5) # could use Semidef or Symmetric here instead
   
   obj = cvx.Minimize(cvx.norm(X-B, 'fro'))
   constraints = [ X == X.T, X >> 0 ] # X is PSD

   prob = cvx.Problem(obj, constraints)
   prob.solve()

   print_status(prob, X)

def problem9():
   A, y = get_vars()
   print('Rerun Problem 1 without parameterizing ...')
   x = cvx.Variable(10)
   obj = cvx.Minimize(cvx.norm(x))
   constraints = [cvx.norm(A@x - y) <= 0.1]
   prob = cvx.Problem(obj, constraints)
   t = time.time()
   prob.solve()
   elapsed = time.time() - t
   print(f"  Elapsed time: {elapsed} seconds.")
   print('Now parameterize y ...')
   b = cvx.Parameter(5)
   obj = cvx.Minimize(cvx.norm(x))
   constraints = [cvx.norm(A@x - b) <= 0.1]
   prob = cvx.Problem(obj, constraints)

   for i in range(10):
      b.value = np.random.rand(5)
      t = time.time()
      prob.solve()
      elapsed = time.time() - t
      print(f"  {i=}, Elapsed time: {elapsed} seconds.")

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('num', type=int, help='number of problem to run', default=1)
   args = parser.parse_args()
   
   num = args.num
   if num < 1 or num > 9:
      raise argparse.ArgumentError('Problem number should be in [1..9]')
   
   problem_funs = [eval('problem'+str(i)) for i in range(1,10)]
   problem_funs[num-1]()
   

# vim: set ts=3 sw=3 sts=3 et :
