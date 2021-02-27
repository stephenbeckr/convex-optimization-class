# Syllabus for APPM 5630 Advanced Convex Optimization

Spring 2021, Instructor: Stephen Becker

This semester, the class is taught remotely some of the time due to COVID-19

Since there is no established optimization curriculum at CU Boulder, we will attempt to cover a lot of material in just one semester. We can divide topics into four broad categories:
- **Analysis**: Basic theory (convex analysis, optimality, duality)
- **Methods**: Standard methods, both classical and modern, and standard classifications. The idea is to give students a toolkit of standard approaches to solve actual problems.
- **Convergence**: Convergence theory (ellipsoid, Nesterov, etc.). This involves some very beautiful mathematics (and is also useful!)
- **Applications**: Often in signal processing and machine learning

The course investigates landmark convex optimization algorithms and their complexity results. We aim to cover both key theory, such as polynomial time algorithms for linear programming and the optimality of Nesterov’s method, while also surveying current practical state-of-the-art methods.

### Official course description
Investigates landmark convex optimization algorithms and their complexity results. Studies both theory while also surveying current practical state-of-the-art methods. Topics may include Fenchel-Rockafellar duality, KKT conditions, proximal methods, and Nesterov acceleration.


### Related courses at CU
This course is similar to the CS department's [CSCI 5254](http://spot.colorado.edu/~lich1539/cvxopt.html) but goes a bit farther.

Here's a list of [optimization classes taught at CU](https://sites.google.com/colorado.edu/optimization)



### Principal Topics
convex sets, convex analysis, Fenchel-Legendre conjugates, Fenchel-Rockafellar and Lagrangian duality, KKT and Slater’s conditions, conic optimization, (stochastic) gradient descent, calculating gradients, proximal methods, constrained optimization

### Learning Goals/Outcomes
[//]: # ( Not testable; high-level )
[//]: # ( Learning Objectives, i.e., quantifiable outcomes )
[//]: # ( Something measurable )
Students will learn the mathematics behind convex analysis, and why convexity is useful in optimization problems. Students will understand the setup and optimality of optimization problems, and how math can be used to provide explicit certificates of sub-optimality as well as implicit certificates via worst-case convergence rates. Students will know how to program core methods, applied to a few examples, and learn to construct programs in a modular, debuggable fashion. Students will synthesis their knowledge by producing a final project demonstrating application of optimization to real-world problems



# Detailed list/schedule of Lectures/Topics

| |Mon|Wed|Fri|
|-|-|-|-|
|Week 1: Jan 11-15| No class | No class | 1 |
|Week 2: Jan 18-22| No class | 2 | 3 |
|Week 3: Jan 25-29 | 4*  | 5  | 6  (HW 1-2 due)|
|Week 4: Feb 1-5   | 7**  | 8  | 9  |
|Week 5: Feb 8-12   | 10  | 11  | 12  (HW 3-4 due)|
|Week 6: Feb 15-19   | 13  | No class  | 14  |
|Week 7: Feb 22-26   | 15  | 16  |  17 (HW 5-6 due)|
|Week 8: Mar 1-5   |  18 | 19  | 20  |
|Week 9: Mar 8-12   | 21  | 22  | 23 |
|Week 10: Mar 15-19   | 24  | 25  | 26  (HW 7-8 due)|
|Week 11: Mar 22-26 "spring pause" | 27  | 28***  | 29  |
|Week 12: Mar 29-Apr 2   | 30  | 31  | 32  (HW 9-10 due)|
|Week 13: Apr 5-9   | 33  |  34 | 35  |
|Week 14: Apr 12-16   | 36  |  37 | 38  (no HW, work on projects)|
|Week 15: Apr 19-23   |  39 | 40  | 41  |
|Week 16: Apr 26-30   | 42  | 43  |  No class  |

Legend: * means last day to add a class (without instructor approval), ** is last day to drop a class (without a W), *** is last day to withdraw from a class (student receives a W)

HW 1-2 is due early, but I don't want to push the due-date back farther because I want students to get feedback on a homework before they have to decide about withdrawing from the class (Feb 1, lecture #7).

### Fall 2018
Here's what we did in Fall 2018.  Spring 2021 will be somewhat similar.

1.	Intro
2.	Intro
3.	Convex Sets [BV04 ch 2]
4.	`cvx`, `cvxpy` tutorial
5.	Convex sets, PSD cone, separating hyperplanes [BV04 ch2]
6.	Convex functions [BV04 ch 3]
7.	Convex functions, subgradients, commuting addition and subgradients [BC11]
8.	subgradients, more on convex fcn not from [BV04], strong/strict convexity; see handout on Lipschitz bounds
9.	Convex functions, sections 3.1--3.3 in [BV04] (Fenchel-Legendre conjugate functions)
10.	3.3 in [BV04], convex relaxation f^** [BC11], Fenchel-Young
11.	convex relaxation f^** [BC11], [Luc10]; existence/uniqueness of minimizers [BC11 ch 11]; proximity operator [BC11, CP11]
12.	prox, Moreau envelope [CW05]
13.	prox, Moreau envelope [CW05]; Convex Optimization [BV04 ch 4]; gradient descent
14.	convergence of gradient descent [Van16]; fire drill!
15.	worst-case counter-example for 1st order methods [Nes04]
16.	Convex Optimization [BV04 ch 4.2]
17.	Convex Optimization, LP/QP/SOCP/SDP [BV04 ch 4.2-3, 4.6]
18.	SDP/LMI [BV04 ch 4.6], Duality and Lagrangians [BV04 ch 5.1]
19.	LP duality [Van08], sensible rules for remembering duals (SOB) [Ben95], Slater
20.	Slater and strong duality [BV04 ch5.2], geometric interpretation [BV04 ch5.3]
21.	Game theory [BV04 ch 5.2.5; 5.4.3], saddle point interpretation [BV04 ch 5.4]; some Fenchel-Rockafellar duality
22.	Fenchel-Rockafellar duality [BC11, chs15,18-19]
23.	Optimality and KKT conditions [BV04 ch5.5], perturbation and sensitivity [BV04 ch5.6]
24.	perturbation and sensitivity [BV04 ch5.6], generalized inequalities (eg. SDP) [BV04 ch5.9]
25.	Interlude on proximal [CW05][Van16] and accelerated (Nesterov) gradient methods [Nes04][Van16][BT10]; convergence rates
26.	Fast/fancy algorithms for unconstrained optimization [NW05]: Nesterov, Newton, linear/non-linear conjugate gradient
27.	Fast/fancy algorithms for unconstrained optimization [NW05]: quasi-Newton and L-BFGS
28.	Fast/fancy algorithms for unconstrained optimization [NW05]: inexact/matrix-free Newon (Newton-CG), non-linear least-squares and Gauss-Newton, Levenberg-Marquardt, active-set methods
29.	Constrained optimization [NW05]: penalty methods, augmented Lagrangian
30.	derivatives; some thms from [BC11], [Ber99]
31.	derivatives, automatic differentiation [NW05]
32.	adjoint-state method
33.	Newton's method, self-concordant [BV04 ch 9]
34.	Newton's method, self-concordant [BV04 ch 9]
35.	Newton for equality constraints [BV04 ch 10], interior-point methods [BV04 ch 11]
36.	interior-point methods [BV04 ch 11]
37.	First order methods: proximal pt, subgradient descent, conditional gradient aka Frank-Wolfe
38.	First order methods: ADMM [Boyd10], Douglas-Rachford [BC17], [CP11]
39.	Primal-dual method [Con13][CBS14][CCPV14][ChPo11]
40.	Simplex method [NW05]
41.	Complexity of LP and Simplex [Nem16], smoothed analysis, integer linear programming [Van08]; LP in fixed dimension [DMW97]
42.	STUDENT PRESENTATIONS
43.	STUDENT PRESENTATIONS
44.	STUDENT PRESENTATIONS

**References (books)**
-	[BV04]	S. Boyd and L. Vandenberghe, “Convex Optimization” (Cambridge U. Press, 2004). [Free electronic version](http://www.stanford.edu/~boyd/cvxbook/)
-	[NW05]	J. Nocedal and S. Wright, “Numerical Optimization” (Springer, 2005). We have free electronic access at [SpringerLink](https://link.springer.com/book/10.1007%2F978-0-387-40065-5)
-	[Nem16]	A. Nemirovski, Introduction to Linear Optimization, [lecture notes](http://www2.isye.gatech.edu/~nemirovs/OPTI_LectureNotes2016.pdf)
-	[Van08]	R. Vanderbei, “Linear Programming.” (2008) Free download at [Vanderbei's website](http://www.princeton.edu/~rvdb/LPbook/) and also via SpringerLink. 				
-	[BC11]	H. Bauschke and P. Combettes, “Convex Analysis and Monotone Operator Theory in Hilbert Spaces”, 1st ed, Springer 2011, available electronically via [SpringerLink](https://link.springer.com/book/10.1007%2F978-1-4419-9467-7)
-	[BC17]	H. Bauschke and P. Combettes, “Convex Analysis and Monotone Operator Theory in Hilbert Spaces”, 2nd ed, Springer 2017, available electronically via [SpringerLink](https://link.springer.com/book/10.1007/978-3-319-48311-5)
-	[Ber99]	D. Bertsekas, "Nonlinear Programming", 2nd ed, Athena Scientific, 1999.				
-	[Ber16]	D. Bertsekas, "[Nonlinear Programming](http://www.athenasc.com/nonlinbook.html)", 3rd ed, Athena Scientific, 2016.			
-	[Nes04]	Y. Nesterov, "Introductory Lectures on Convex Optimization" (2004); [Springer](http://www.springer.com/us/book/9781402075537)  
    - A new version is out, "[Lectures On Convex Optimization](https://www.springer.com/gp/book/9783319915777)" Nesterov 2018, but it has rearranged the chapters a bit, so you need to adjust the numbering quite a bit

**References (papers)**			
-	[Boyd10]	“[Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers](http://web.stanford.edu/~boyd/papers/pdf/admm_distr_stats.pdf)” by S. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein (2010);
-	[CP11]	P. L. Combettes and J.-C. Pesquet, “[Proximal splitting methods in signal processing](http://www4.ncsu.edu/~pcombet/prox.pdf),” 2011;  				
-	[Con13]	Laurent Condat “[A primal-dual splitting method for convex optimization involving Lipschitzian, proximable and linear composite terms](https://www.gipsa-lab.grenoble-inp.fr/~laurent.condat/publis/Condat-optim-JOTA-2013.pdf)”, 2011 (J. Optim. Theory and Appl. 2013). 			
-	[CBS14]	"[Convex Optimization for Big Data: Scalable, randomized, and parallel algorithms for big data analytics](http://dx.doi.org/10.1109/MSP.2014.2329397)", Volkan Cevher, Stephen Becker, Mark Schmidt, IEEE Signal Processing Magazine, vol. 31, no. 5, 2014; 				
-	[CCPV14]	"[A forward-backward view of some primal-dual optimization methods in image recovery](https://arxiv.org/abs/1406.5439)", Patrick L. Combettes, Laurent Condat, Jean-Christophe Pesquet, Bang Cong Vu (2014)				
-	[ChPo11]	"[A first-order primal-dual algorithm for convex problems with applications to imaging](https://hal.archives-ouvertes.fr/hal-00490826/document)", A Chambolle, T Pock (2011); 				
-	[Luc10]	"[What Shape Is Your Conjugate? A Survey of Computational Convex Analysis and Its Applications](https://doi.org/10.1137/100788458)", Yves Lucet, SIAM Review, 52(3) 2010
-	[CW05]	"[Signal recovery by proximal forward-backward splitting](http://www4.ncsu.edu/~pcombet/mms1.pdf)", PL Combettes, VR Wajs - Multiscale Modeling & Simulation, 2005; 				
-	[Van16]	[EE236C class, lecture on gradient methods](http://www.seas.ucla.edu/~vandenbe/236C/lectures/gradient.pdf), L. Vandenberghe, 2016; 				
-	[Ben95]	A. Benjamin, [Sensible rules for remembering duals](https://www.math.hmc.edu/~benjamin/papers/sob.pdf). SIAM Review (37)1 1995.				
-	[BT10]	A. Beck and M. Teboulle, "[Gradient-Based Algorithms with Applications in Signal Recovery Problems](http://www.math.tau.ac.il/~teboulle/papers/gradient_chapter.pdf)" (2010); 				
-	[DMW97]	M. Dyer, N. Megiddo, E. Welzl, "[Linear programming](http://www.inf.ethz.ch/personal/emo/PublFiles/LpSurvey03.pdf)" (chapter in Handbook of Discrete and Comp. Geometry, 1997) 				
-	[Dual]	"[Please explain intuition behind dual problem](https://math.stackexchange.com/q/223235/98783)" on math.stackexchange


# Resources

We will not follow a single textbook. The following resources (mostly available online) will be the **primary references**:

- [BV2004] S. Boyd and L. Vandenberghe, “Convex Optimization” (Cambridge U. Press, 2004). [Free electronic version](http://www.stanford.edu/~boyd/cvxbook/)  This is a standard text that gives some convex analysis background and focuses on interior-point methods and engineering applications. The books is very useful, and I recommend you buy a copy. We will follow the book closely at the beginning of the semester. The appendices A and C are also quite useful if you do not have an applied math background.
- [V_course] L. Vandenberghe’s [course notes for ee236b](http://www.seas.ucla.edu/~vandenbe/ee236b/ee236b.html) follow the book, while his course notes for [ee236c](www.seas.ucla.edu/~vandenbe/ee236c.html) contain more details on proofs and advanced topics.
- [NW05] J. Nocedal and S. Wright, “Numerical Optimization” (Springer, 2005). We have free electronic
access at CU via [SpringerLink](http://link.springer.com/book/10.1007/978-0-387-40065-5). This is the go-to reference for implementing a standard method.
- [Beck17] Amir Beck, “First-Order Methods in Optimization” (SIAM, 2017). A more advanced text than
Beck’s 2014 text; free on campus at [SIAM eBooks](https://epubs.siam.org/doi/book/10.1137/1.9781611974997)
- [BC17]	H. Bauschke and P. Combettes, “Convex Analysis and Monotone Operator Theory in Hilbert Spaces”, 2nd ed, Springer 2017, available electronically via [SpringerLink](https://link.springer.com/book/10.1007/978-3-319-48311-5). A nice collection of results, best as a reference and not as a step-by-step textbook. Sometimes we refer to the 2011 1st edition.

Some supplemental resources:

- Lijun Chen teaches a similar optimization course in the CS department, [CSCI 5254](http://spot.colorado.edu/~lich1539/cvxopt.html). That course uses the Boyd and Vandenberghe book.  See also a [list of optimization courses at CU](https://sites.google.com/colorado.edu/optimization)

- [Encyclopedia of Optimization](https://link.springer.com/referencework/10.1007/978-0-387-74759-0), 2009 Edition edited by C. A. Floudas and P. M. Pardalos is very comprehensive and has many articles on detailed topics. There are many other books that have similar names ("handbook of optimization", etc) but most of those are somewhat random in content (usually compiled after a conference). In contrast, this encylopedia really is what you hope it might be.

- Ben Recht's [CS 726: Nonlinear Optimization I at Wisconsin 2012](http://pages.cs.wisc.edu/~brecht/cs726.html)
- Sebastian Bubeck's [ORF523: The complexities of optimization](https://blogs.princeton.edu/imabandit/orf523-the-complexities-of-optimization/) at Princeton (blog style) and his [monograph on the same topic, "Convex Optimization: Algorithms and Complexity"](https://arxiv.org/abs/1405.4980) (pdf, published in Foundations and Trends in Machine Learning, Vol. 8: No. 3-4, pp 231-357, 2015); another [link](http://research.microsoft.com/en-us/um/people/sebubeck/Bubeck15.pdf)
More advanced resources:

- Ben Recht's [Convex Optimization and Approximation: Optimization for Modern Data Analysis EECS 227C/STAT 260
Spring 2016](https://people.eecs.berkeley.edu/~brecht/eecs227c.html) and his [CS294 - The Mathematics of Information and Data](https://people.eecs.berkeley.edu/~brecht/cs294.html)
- [Arkadi Nemirovski](http://www2.isye.gatech.edu/~nemirovs/) has many lecture notes on various topics, including linear programming.
  - His [Lectures on Modern Convex Optimization](http://www2.isye.gatech.edu/~nemirovs/Lect_ModConvOpt.pdf) with A. Ben-Tal may be the most relevant; the PDF notes are from 2013, and they have a 2001 [book from SIAM of the same title](http://epubs.siam.org/doi/book/10.1137/1.9780898718829)
  - For complexity and linear programming, see his [Introduction to Linear Optimization](https://www2.isye.gatech.edu/~nemirovs/OPTILectureNotes2016.pdf) from 2016
- John Duchi's [Introductory Lectures on Stochastic Optimization](https://stanford.edu/~jduchi/PCMIConvex/)
- Stephen Boyd’s [course notes for EE364a](http://www.stanford.edu/class/ee364a/), which follow his book.
- Amir Beck, “Introduction to Nonlinear Optimization: Theory, Algorithms, and Applications with MATLAB” (SIAM, 2014, $89). This covers classical results but by a modern researcher aware of current research
- Stephen Wright, “Primal-Dual Interior-Point Methods” (SIAM 1997), available electronically from [SIAM](http://epubs.siam.org/doi/book/10.1137/1.9781611971453). Good summary of LP theory, and more practical/thorough IPM discussion than in [BV2004]
(e.g., includes Mehotra’s predictor-corrector method), though restricted to LP of course.
- R. Tyrrell Rockafellar, “Convex Analysis”, Princeton 1970 (reprinted 1997). Terry Rockafellar wrote the first, and definitive, book on the subject.
- D. Bertsekas, A. Nedic, A.E. Ozdaglar, “Convex Analysis and Optimization” (Athena Scientific).
- D. Bertsekas, “Convex Optimization Theory” (Athena Scientific). [Bertsekas has a lot of other books with useful information as well]
- J. M. Borwein and A. S. Lewis, “[Convex Analysis and Nonlinear Optimization](http://link.springer.com/book/10.1007/978-0-387-31256-9/page/1)” (Springer). A bit more mathematical
- J.B. Hiriart-Urruty and C. Lemarechal, “Convex Analysis and Minimization Algorithms” (Springer). More on analysis, less on optimization. Technical and a useful reference.
- D. Luenberger and Y. Ye, “[Linear and Nonlinear Programming](http://dx.doi.org/10.1007/978-0-387-74503-9)” (Springer). A bit more mathematical than [BV2004], slightly different topics.
- R. Tyrrell Rockafellar and Roger J. B. Wets, "[Variational Analysis](https://link.springer.com/book/10.1007/978-3-642-02431-3)" (Springer; via SpringerLink or Rockafellar's website), goes more into detail on the analysis portion; a good mathematical reference for researchers.

And a fun miscellaneous reference:
- Harvey Greenberg (UC Denver, emeritus), [Myths and counterexamples in mathematical programming](https://glossary.informs.org/myths/CurrentVersion/myths.pdf). Entertaining and informative




### Programming
Homeworks will involve by mathematical analysis and programming.

Students are expected to already know how to program.  We encourage using **Python** and **Matlab**; **Julia** is another good choice though we will not be using it explicitly.  For homework assignments, usually the deliverable is the outcome of some code, so therefore the student may choose any reasonable programming language. However, we will be doing demonstrations in Python and/or Matlab (and the instructor is best at debugging Python and Matlab).  Most of our demonstrations will be using [github](http://github.com) in conjunction with [python via colab](https://colab.research.google.com/).

For Matlab, we'll use [CVX](http://cvxr.com/cvx) (though [yalmip](https://yalmip.github.io/) is also good); for Python, we'll use [cvxpy](http://cvxpy.org/); for Julia, try [Convex.jl](http://convexjl.readthedocs.io/). These are all good prototyping packages.

Matlab and Python mainly rely on small third-party packages. Julia has more "official"-like packages. Most of them use the [JuMP](https://jump.dev/) framework, including big packages like [JuliaSmoothOptimizers / SolverTools.jl](https://github.com/JuliaSmoothOptimizers/SolverTools.jl) and [JuliaNLSolvers / Optim.jl](https://julianlsolvers.github.io/Optim.jl/stable/).  One of the nice things about Julia is that it has very good automatic differentiation support (see a [discussion of Julia AD packages](https://discourse.julialang.org/t/state-of-automatic-differentiation-in-julia/43083/3)). Other nice things about Julia: very active and friendly community that are eager to help if you post in the forums; code executes very rapidly (like C and Fortran); high-level programming like Python and Matlab; lots of packages, and increasing quickly (way behind Python overall, but catching up in terms of specialized numerics packages); easy to call Python libraries from within Julia.

We recommend use of an IDE or something like JupyterLab.

We do **not** recommend using C, C++ or Fortran for programming in this class; these languages take a lot longer to prototype in, and the performance can be fast but only if you do it right (and usually requires calling the right kind of libraries, like [NAG](https://www.nag.com/content/nag-library) or GLPK or using suites like PETSc, Trilinos, [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page), etc.)

For automatic differentiation in Matlab, try [ADiMat](https://www.sc.informatik.tu-darmstadt.de/res/sw/adimat/general/index.en.jsp); in Python, try [JAX](https://jax.readthedocs.io/en/latest/)

# More details on topics
We don't present the lectures in the following order (lectures intermingle topics more, so that students can get started on interesting homeworks right away), but thematically, the following is what we roughly cover:

Section 1: Background, duality, motivation
1. Intro
2. Convex Sets (ch 2 in [BV2004])
3. Convex Functions (ch 3 in [BV2004])
4. Convex Analysis, subdifferentials ([BauschkeCombettes])
5. Convex Optim. Problems (ch 4 in [BV2004])
6. Duality, optimality (ch 5 in [BV2004])
7. Some applications, ERM and machine learning, sparse recovery, image denoising, low-rank matrix
recovery
8. CVX, CVXPY, convex.jl tutorials

Section 2: Conic programs & relaxations
1. Linear programming
     - standard LP theory, duality ([WrightIPM])
     - simplex method, complexity, smoothed analysis ([Vanderbei_LP], [Nemirovski_LP])
     - IPM ([WrightIPM], [BV2004])
     - ellipsoid method (TBD, [Nemirovski_LP])
2. Integer Linear programming ([Vanderbei_LP])
3. SDP ([BV2004], Pataki?)
4. QP, convex and non-convex (S-procedure, relaxations) ([Nemirovski_LP],[BN_Modern], [BV2004])
5. MAXCUT relaxation ([Nemirovski_LP],[BN_Modern])
6. Polynomial optimization, SOS ([Nemirovski_LP],[BN_Modern])

Section 3: Algorithms
1. Gradient Descent ([V_course])
2. Accelerated and projected/proximal gradient descent, optimality ([V_course])
3. Classical methods ([NW05], Bertsekas, [Nesterov2004])
    - Subgradient descent
    - Newtons method, self-concordancy
    - Non-linear conjugate gradient d) quasi-Newton
    - Levenberg-Marquardt, Gauss-Newton f) Augmented Lagrangian
    - Sequential Quadratic Programming (SQP)
    - Step-size (Barzilai-Borwein), line search
3. Recent methods
    - Douglas-Rachford and ADMM
    - Primal-dual methods (e.g., Condat)
    - Conditional Gradient and Frank-Wolfe d) (Randomized) Coordinate Descent
    - Stochastic gradient descent
    - State-of-the-art variants (SDCA, SAGA, etc.)

Possible additional topics
1. Benders decomposition
2. Geometric Programming, linear-fractional
3. Online Convex Optimization
4. Mirror Descent
5. Bregman distances
6. Robust optimization
7. Randomized Kaczmarz method; Algebraic Reconstruction Technique (ART) for tomography
8. POCS (projection onto convex sets), best approximation, Dykstra’s algorithm
