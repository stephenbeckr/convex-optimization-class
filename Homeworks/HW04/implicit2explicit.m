function A = implicit2explicit(Afun,m,n)
%IMPLICIT2EXPLICIT takes a linear function Afun(x) and builds the corresponding matrix
%   Makes an explicit matrix using the linear function
%   in the function handle "Afun", where the domain is R^n
%   and the range is in R^m
%
% Usage: implicit2explicit(Afun,m,n)
%
%   If n = [n1,n2], the domain is the space of n1 x n2 matrices
%       Output of Afun should always be a m x 1 column vector
%
% Stephen Becker, stephen.becker@colorado.edu, 2/13/2017

if nargin < 3, n = m; end

A = zeros(m,prod(n));
if numel(n) == 1
    e = zeros(n,1);
else
    if numel(n) ~= 2, error('bad value for size of domain'); end
    e = zeros(n(1),n(2));
end
for j = 1:prod(n)
    e(j) = 1;
    A(:,j) = Afun(e);
    e(j) = 0;
end
