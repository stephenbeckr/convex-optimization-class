function y = project_l1(x, tau)
% y = project_l1( x, tau )
%   projects x onto the scaled l1 ball, ||x||_1 <= tau
%   If tau is not provided, default is tau = 1.
%
%   If x is a matrix, the operation is performed along
%   each column.
%
% Stephen Becker and Emmanuel Candes, 2009/2010
% Crucial bug fix: 3/17/2017

if nargin < 2, tau = 1; end

row_vec = 0;
if size(x,1) == 1 && size(x,2) > 1
   row_vec = 1;
   x = x(:);
end

absx = abs(x);
s   = sort(absx, 1, 'descend');
cs  = cumsum(s, 1);

I = find(cs(end,:) > tau);
% If in I, then x is not feasible, and we must project;
% if not in I, then x is already feasible.
% Bug found by SRB on 3/17/2017
y = x;

% Do projections where needed
for i=1:numel(I)
   ind = I(i);
   
   % JMF 27/03/2017: There's probably a slicker way to do this.
   thresh = get_vector_thresh(x(:,i), tau, s(:,i), cs(:,i));
   y(:,i) = sign(x(:,i)).*max(absx(:,i) - thresh, 0);
end

if row_vec % restore size
   y = y.';
end

end

function [thresh] = get_vector_thresh(x, tau, s, cs)
   % Check some "discrete" levels of shrinkage, e.g. [s(2:end),0]
   % This lets us discover which indices will be nonzero
   i_tau   = find(cs - (1:numel(x))'.* [s(2:end) ; 0] >= tau,   1);
   
   % Now that we know which indices are involved, it's a very simple problem:
   thresh  = (cs(i_tau) - tau)/i_tau;
end
