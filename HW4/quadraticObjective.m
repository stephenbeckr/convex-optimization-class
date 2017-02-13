function [f,g] = quadraticObjective(x,A,b, At)
% f = quadraticObjective( x, A, b )
%   computes f(x) = 1/2 || Ax-b ||^2
%   where "A" is a linear operator (either a matrix or a function handle)
%
% [f,g] = ...
%   also returns the gradient g(x) = \nabla f(x) = A'*(A*x-b)
%
% ... = quadraticObjective( x, A, b, At )
%   uses "At" for the adjoint of the linear operator "A".
%   This is only necessary if "A" is a function handle
%
% This form is suitable for most of Matlab's solvers
%   and for 3rd party packages like Mark Schmidt's minFunc
%
% Stephen.Becker@Colorado.edu, 2/13/2017

if ~isa( A, 'function_handle')
    At  = @(x) A'*x;
    A   = @(x) A*x; % overload notation
elseif nargin < 4
    error('If "A" is a function hande, need 4 inputs');
end

r   = A(x) - b; % residual
f   = norm( r )^2/2;
if nargout >= 2
    g   = At(r);
end