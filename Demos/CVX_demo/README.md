# Demos for using CVX (Matlab) and CVXPY (Python)

## Step 1: get introduced to CVX/CVXPY

- For Matlab, see [cvx_demo.mlx](cvx_demo.mlx) or its PDF version [cvx_demo.pdf](cvx_demo.pdf)
  - On Macs, if you get errors opening mex files like "...mexmaci64" cannot be opened because the developer cannot be verified." then follow instructions analogous to [here](https://www.fieldtriptoolbox.org/faq/mexmaci64_cannot_be_opened_because_the_developer_cannot_be_verified/), e.g., (1) `sudo xattr -r -d com.apple.quarantine LOCATION_OF_CVX` followed by (2) `sudo find LOCATION_OF_CVX -name \*.mexmaci64 -exec spctl --add {} \;`
- For Python, see [cvxpy_intro.ipynb](cvxpy_intro.ipynb) (which has link to colab or use [direct link](https://colab.research.google.com/github/stephenbeckr/convex-optimization-class/blob/master/Demos/CVX_demo/cvxpy_intro.ipynb)) or its PDF version [cvxpy_intro.pdf](cvxpy_intro.pdf)
  - Or just look at the documentation from the software, which is pretty good

## Step 2: try filling out the worksheet

[Handout2_cvx_tutorial.pdf](Handout2_cvx_tutorial.pdf)

## Step 3: check your answers

- For Matlab, [tutorialSolutions.m](tutorialSolutions.m)
- For Python, [tutorialSolutions.py](tutorialSolutions.py) (this uses an older version of cvxpy and python) or the (newer) Jupyter notebook  [tutorialSolutions.ipynb](tutorialSolutions.ipynb)

## Step 4: if you are super fast and finish everything...
- Try my "least squares challenge" in either [python](https://github.com/stephenbeckr/ML-theory-class/blob/main/Code/LeastSquaresChallenge.ipynb) or [matlab](https://github.com/stephenbeckr/ML-theory-class/blob/main/Code/LeastSquaresChallenge.m).
  - [Solutions are here](https://github.com/stephenbeckr/ML-theory-class/tree/solutions/Code)
