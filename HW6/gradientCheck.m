function [hList, Errors] = gradientCheck( f, grad, x0, scaling, numberPoints )
% gradientCheck( f, grad, x0 )
%   runs several gradient checks at the point x0
% gradientCheck( f-and-grad, [], x0 )
%   assumes that f-and-grad is a combined function handle
%   that returns [f(x), gradient(x)] = f-and-grad(x)
%       i.e. fminunc style
%
% gradientCheck( ..., scaling, numberPoints )
%   scales the stepsize and uses numberPoints values of h.
%
% [hList,Errors] = ...
%   returns the error values. In this format, nothing
%   is printed to the screen.
%
% Output: first column is h, the stepsize
%   Forward diff column:    expect to decay like O(h)
%   Central diff column:    expect to decay like O(h^2)
%   1st order Taylor:       expect to decay like O(h), regardless
%       of whether gradient is correct.
%   2nd order Taylor:       expect to decay like O(h^2)
%   3rd order Taylor:       expect to decay like O(h^3)
%
% Note: this decay in h is only until h reaches a certain level, and below
%   that size, roundoff error will make the approximation worse and worse.
%   The critical level of h is larger for the higher-order methods.
%   Use "scaling" to adjust the relative value of h.
%
% Stephen.Becker@Colorado.edu, 2/23/2017

if nargin < 4, scaling = 1; end
if nargin < 5, numberPoints = 8; end

n   = length(x0);

if isempty(grad)
    % [fcn,grad] = f(x) convention
    [f0,g0] = f(x0);
else
    f0  = f(x0);
    g0  = grad(x0);
end


hfinal  = log10(scaling*eps)/2+1;
hList = logspace( 7+hfinal, hfinal, numberPoints );
if nargout==0
    fprintf('%s\n',repmat('-',1,112));
    fprintf('h\t\tForward diff\tCentral diff\t1st order Taylor\t2nd order Taylor\t3rd order Taylor\n');
    fprintf('%s\n',repmat('-',1,112));
else
    Errors = zeros( numberPoints, 5 ); 
end
counter = 0;
for h  = hList
    counter = counter + 1;
    
    g = zeros(n,1);  % forward finite-differences
    gc= zeros(n,1);  % central differences
    e = zeros(n,1);
    hh  = h;
    for i = 1:n
        e(i)    = 1;
        f1      = f(x0 + hh*e);
        g(i)    = ( f1 - f0 )/hh;
        gc(i)   = ( f1 - f(x0-hh*e) )/(2*hh);
        e(i)    = 0;
    end
    er_fd   = norm(g - g0)/norm(g0);
    er_cd   = norm(gc - g0)/norm(g0);
    
    % Another test that doesn't require us to build the entire gradient
    % Pick any reasonably point: let's make it something of a similar
    % scale, and progressively closer
    %   We can average this if we like
    nReps    = 5;
    [Taylor1,Taylor2,err3] = deal(0);
    for reps = 1:nReps
        x1  = x0 + h*randn(size(x0))/sqrt(numel(x0))*norm(x0);
        f1  = f(x1);
        if isempty(grad)
            [~,g1]  = f(x1);
        else
            g1  = grad(x1);
        end
        
        % From dolfin-adjoint
        % http://www.dolfin-adjoint.org/en/latest/documentation/verification.html
        Taylor1     = Taylor1 + abs( f0 - f1 );                 % should be O(h)
        Taylor2     = Taylor2 + abs( f0 + dot(g0,x1-x0) - f1 ); % should be O(h^2)
        
        % Try an O(h^3) method
        err3  = err3 + abs(abs(dot(g0+g1,x1-x0) -2*(f1-f0))); % should be little-oh of h^2 at least
    end
    Taylor1 = Taylor1/nReps;
    Taylor2 = Taylor2/nReps;
    err3    = err3/nReps;
    
    if nargout == 0
        fprintf('%.1e\t\t%.1e\t\t%.1e\t\t%.1e\t\t\t%.1e\t\t\t%.1e\n',...
            h, er_fd, er_cd, Taylor1, Taylor2, err3 );
    else
        Errors(counter,:) = [er_fd, er_cd, Taylor1, Taylor2, err3];
    end
end
