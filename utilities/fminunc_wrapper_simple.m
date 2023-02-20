function [f,g,h] = fminunc_wrapper_simple(x,F,G, H)
% [f,g] = fminunc_wrapper_simple( x, F, G  )
% for use with Matlab's "fminunc"
% and also compatible with Mark Schmidt's minFunc package
%
% Example usage:
%   F = @(x) norm(A*x-b)^2/2  % this is our objective
%   G = @(x) A'*(A*x-b)     % this is the gradient of F(x)
%   options = optimoptions('fminunc','SpecifyObjectiveGradient',true);
%   func    =  @(x)fminunc_wrapper_simple(x,F,G);
%   x0      = randn(size(A,2),1);
% 
%   fminunc_wrapper_simple();        % zero-out history
%   x = fminunc( func, x0, options ) % Matlab's solver
%   hist1   = fminunc_wrapper_simple();     % record history
%   x = minFunc(func, x0 )           % Mark Schmidt's minFunc solver
%   hist2   = fminunc_wrapper_simple();     % record history
%   xTrue   = A\b;                   % true solution known in closed-form
%   fTrue   = F(xTrue);

%   semilogy( hist1 - fTrue ); hold all
%   semilogy( hist2 - fTrue ); legend('fminunc','minFunc');
%
% [fHist] = fminunc_wrapper()
%       will return the function history
%       and reset the history to zero.
%
% ... = fminunc_wrapper( x, F, G, H )
%   will also compute the Hessian H if provided and requested
%
% Stephen Becker, Stephen.Becker@Colorado.edu  2/17/2017

persistent fcnHist
if nargin == 0
   f = fcnHist;
   fcnHist = [];
   return;
end


f = F(x);
fcnHist(end+1)  = f; % not efficient in terms of memory allocation

if nargout > 1
    g = G(x);
end
if nargin > 3 && ~isempty(H) && nargout > 2
    h = H(x);
end
