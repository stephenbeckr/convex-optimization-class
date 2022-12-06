The most useful module here is `firstOrderMethods.py`

The main routine is this:
- `gradientDescent` is proximal gradient descent
  - You can turn on "acceleration" (Nesterov acceleration, aka FISTA)
  - You can also enable line searches instead of a constant stepsize
  - It has a few features, like it can record error information

There are three high-level functions:
- `lassoSolver` is a wrapper to `gradientDescent` specialized for the lasso problem $\min_x .5\|\|Ax-b\|\|^2 + \tau\|\|x\|\|_1$
- `createTestProblem` creates some test problems for unit tests
  - it has 3 types of problems: (1) plain least-squares, (2) lasso, (3) logistic regression
  - it can use `cvxpy` to compute the exact solution, and also return the objects needed to test the code in this package
- you can run `runAllTestProblems` to run all the problems

And there are a few misc utility functions, such as:
- `backtrackingLinesearch` which uses the Armijo conditions
- `LipschitzLinesearch` suitable when the function is Lipschitz-gradient and convex
- `LipschitzLinesearch_stabler` is a variant based on the ideas we did in the TFOCS paper (it's more stable numerically)
- `powerMethod` for estimating the spectral norm of a matrix (useful for estimating Lipschitz constants)

TODO:
- Add an option for exact linesearch for lasso (following my [tech report](https://github.com/stephenbeckr/exactLASSOlinesearch))
- Add a solver for non-negative least squares
- Incorporate into something like [benchOpt](https://github.com/benchopt/)
