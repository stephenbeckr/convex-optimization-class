function test_adjoint( A, At, sz, nRep )
% TEST_ADJOINT( A, At, sz )
%   tests whether the function handles A and At are
%   adjoints (= conjugate transpose) of each other.
%   
%   sz should be the size of the domain, e.g.,
%       sz = n  for domain to be n x 1 column vectors
% 
%       sz = [n1,n2] for the domain to be n1 x n2 matrices
%
% TEST_ADJOINT( A, At, sz, nRep )
%   controls how many tests to perform (default: 10)
%
% Stephen.Becker@Colorado.edu, 2/13/2017

if nargin < 4, nRep = 10; end

for rep = 1:nRep
    
    if numel(sz) == 1
        n   = sz;
        x   = randn(n,1);
    else
        x   = randn(sz); % could be a matrix
    end
    
    Ax  = A(x);
    y   = randn( size(Ax) );
    Aty = At(y);
    
    er  = dot( Ax, y ) - dot( x, Aty );
    fprintf('Error in adjoint: %.2g\n', abs(er)/sqrt(norm(x)*norm(y)) );
end
