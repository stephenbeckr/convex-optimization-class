function [hList, Errors,chng] = gradientCheck( f, grad, x0, scaling, numberPoints, FORCE_FINITE_DIFF )
% gradientCheck( f, grad, x0 )
%   runs several gradient checks at the point x0
% gradientCheck( f-and-grad, [], x0 )
%   assumes that f-and-grad is a combined function handle
%   that returns [f(x), gradient(x)] = f-and-grad(x)
%       i.e. fminunc style
%
% gradientCheck( ..., scaling, numberPoints, FORCE_FINITE_DIFF )
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
% After this output, it displays the decay rates
%   (variabe is "chng")
%
% Note: this decay in h is only until h reaches a certain level, and below
%   that size, roundoff error will make the approximation worse and worse.
%   The critical level of h is larger for the higher-order methods.
%   Use "scaling" to adjust the relative value of h.
%
% Stephen.Becker@Colorado.edu, 2/23/2017 (1/13/2018 update)

if nargin < 4, scaling = 1; end
if nargin < 5, numberPoints = 8; end
if nargin < 6 || isempty(FORCE_FINITE_DIFF), FORCE_FINITE_DIFF = false; end

n   = length(x0);

if n <= 50 || FORCE_FINITE_DIFF
    DO_FINITE_DIFFERENCES = true;
else
    % for large n, this is too expensive
    DO_FINITE_DIFFERENCES = false;
end

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
    fprintf('\nGradient Check code: type "help gradientCheck" to see what output should look like\n');
    fprintf('%s\n',repmat('-',1,112));
    if DO_FINITE_DIFFERENCES
      fprintf('h\t\tForward diff\tCentral diff\t1st order Taylor\t2nd order Taylor\t3rd order Taylor\n');
    else
      fprintf('h\t\t1st order Taylor\t2nd order Taylor\t3rd order Taylor\n');
    end
    fprintf('%s\n',repmat('-',1,112));
end
Errors = zeros( numberPoints, 3 + 2*DO_FINITE_DIFFERENCES );

ESTIMATE_ORDER = true;

counter = 0;
for h  = hList
    counter = counter + 1;
    
    if DO_FINITE_DIFFERENCES
        % This will be VERY slow if n is large
        
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
        er_fd   = norm(g - g0)/max(norm(g0),1e-10);
        er_cd   = norm(gc - g0)/max(norm(g0),1e-10);
    end
    
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
        if DO_FINITE_DIFFERENCES
            fprintf('%.1e\t\t%.1e\t\t%.1e\t\t%.1e\t\t\t%.1e\t\t\t%.1e\n',...
                h, er_fd, er_cd, Taylor1, Taylor2, err3 );
        else
            fprintf('%.1e\t\t%.1e\t\t\t%.1e\t\t\t%.1e\n',...
                h, Taylor1, Taylor2, err3 );
        end
    end
    if DO_FINITE_DIFFERENCES
        Errors(counter,:) = [er_fd, er_cd, Taylor1, Taylor2, err3];
    else
        Errors(counter,:) = [Taylor1, Taylor2, err3];
    end
end

if ESTIMATE_ORDER
    %df = diff( Errors )./Errors(1:end-1,:)
    df = Errors(2:end,:)./Errors(1:end-1,:);
    dh = hList(2:end)./hList(1:end-1);
%     dh/df
%     diag( dh )*(1./df)
    chng = diag( log10(dh) )*log10((df) );
    
    if nargout == 0
        fprintf('%s\n',repmat('-',1,112));
        fprintf('Order decrease (red = indication that gradient is correct; should have some reds)\n')
        fprintf('%s\n',repmat('-',1,112));
        for j = 1:length(hList)-1
            if DO_FINITE_DIFFERENCES
%                 fprintf('%.1fx\t\t%.1fx\t\t%.1fx\t\t%.1fx\t\t\t%.1fx\t\t\t%.1fx\n',...
%                     1, chng(j,1),chng(j,2),chng(j,3),chng(j,4),chng(j,5) );
                fprintf('%.1fx\t\t',1);
                if chng(j,1) > 0.9
                    fprintf(2,'%.1fx\t\t',chng(j,1) );
                else
                    fprintf(1,'%.1fx\t\t',chng(j,1) );
                end
                if chng(j,2) > 1.9
                    fprintf(2,'%.1fx\t\t',chng(j,2) );
                else
                    fprintf(1,'%.1fx\t\t',chng(j,2) );
                end   
                fprintf(1,'%.1fx\t\t\t',chng(j,3) ); % always O(1)
                if chng(j,4) > 1.9
                    fprintf(2,'%.1fx\t\t\t',chng(j,4) );
                else
                    fprintf(1,'%.1fx\t\t\t',chng(j,4) );
                end
                if chng(j,5) > 2.9
                    fprintf(2,'%.1fx ',chng(j,5) );
                else
                    fprintf(1,'%.1fx',chng(j,5) );
                end
                fprintf('\n');
            else
                fprintf('%.1fx\t\t%.1fx\t\t\t%.1fx\t\t\t%.1fx\n',...
                    1,chng(j,1),chng(j,2),chng(j,3));
            end
        end
    end
end
