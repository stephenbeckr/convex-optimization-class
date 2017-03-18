function y = project_l1(x, tau)
% y = project_l1( x, tau )
%   projects x onto the scaled l1 ball, ||x||_1 <= tau
%   If tau is not provided, default is tau = 1.
%
% Stephen Becker and Emmanuel Candes, 2009/2010
% Crucial bug fix: 3/17/2017

if nargin < 2, tau = 1; end

absx = abs(x);
s   = sort(absx(:),'descend');
cs  = cumsum(s);
if cs(end) <= tau
    % x is already feasible
    % y = s; % Bug!  Found 3/17/2017
    y = x;
    return;
end
n = length(s);

% Check some "discrete" levels of shrinkage, e.g. [s(2:end),0]
% This lets us discover which indices will be nonzero
i_tau   = find(cs - (1:n)'.* [s(2:end) ; 0] >= tau,   1);

% Now that we know which indices are involved, it's a very simple problem:
thresh  = (cs(i_tau) - tau)/i_tau;

% Shrink x by the amount "thresh":
y       = sign(x).*max( absx - thresh , 0 );
