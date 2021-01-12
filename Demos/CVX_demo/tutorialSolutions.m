%{
For CVX in-class tutorial, CCIMI short-course at Cambridge,
 June 2018, Becker
%}
%% Setup the matrix:
% rng(0);
n   = 10;
m   = 5;
A   = reshape( mod( (1:m*n)-1, 11 )+1, m, n )
y   = (1:m)'

% Make global changes to CVX parameters
cvx_precision best
cvx_quiet true
%% Exercise 1
cvx_begin
  variable x(n)
  minimize norm(x)
  subject to
    norm( A*x-y ) <= .1
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 2
cvx_begin
  variable x(n)
  minimize sum_square(x)
  subject to
    norm( A*x-y ) <= .1
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 3
cvx_begin
  variable x(n)  
  minimize norm(x,1)
  subject to
    norm( A*x-y ) <= .1
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 4
cvx_begin
  variable x(n)
  dual variable lambda
  minimize norm(x)
  subject to
    norm( A*x-y ) <= .1 : lambda
cvx_end
% Now, resolve
cvx_begin
  variable xx(n)
  minimize norm(xx) + lambda*norm( A*xx - y )
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
fprintf(' Discrepanct via two methods is %g\n', norm(xx-x)/norm(x) );

%% Exercise 5: matrix problem
% Note: the simple solution, sum(norms(A-x*o',2))
%   doesn't work in CVX "Version 3.0beta, Build 1183 (dda2109)"
o = ones(n,1);
cvx_begin
  variable x(m)
  minimize sum(norms( A - x*o', 2 ))
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 6: matrix problem
cvx_begin
  variable x(m)
  minimize norm( A - x*o')
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 7: matrix problem
cvx_begin
  variable X(m,n)
  minimize norm( X - A, 'fro')
  subject to
    ones(1,m)*X*ones(n,1) == 1
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );
%% Exercise 8: matrix problem
B   = A(:,1:5);
cvx_begin
  variable X(m,m) symmetric
  minimize norm( X - B, 'fro')
  subject to
    X == semidefinite(m)
cvx_end
fprintf('CVX status is "%s", optimal value is %g\n', cvx_status, cvx_optval );