function x = gradientDescent( fcn, x, varargin )
% x = gradientDescent( fcn, x )
%   solves min_x f(x)
%   where [f,g] = fcn(x) returns f(x) and \nabla f(x)
%
% x = gradientDescent( fcn, x, 'parameter','value', 'parmeter2','value2',... )
%   allows control of options (see code for a list, e.g., 'linesearch');
%
% Available parameters are:
%   linesearch          if true, does backtracking linesearch
%   backtrack_c, backtrack_rho      backtracking parameters
%   initialStepsize     stepsize (if linesearch is false, this stepsize is
%                           used for all iterations)
%   maxIts              max number of iterations
%   printEvery          how often to print (printEvery=10 means print output to 
%                           screen every 10 iterations)
%   tol                 relative tolerance in the objective
%   tolX                relative tolerance in ||x_{k} - x_{k-1}||
%
% Stephen.Becker@Colorado.edu, 2/28/2017


prs = inputParser;
addParameter(prs,'linesearch',true);
addParameter(prs,'initialStepsize',1); % e.g. 1/L
addParameter(prs,'backtrack_c',1e-4);
addParameter(prs,'backtrack_rho',0.9);
addParameter(prs,'maxIts',1e4);
addParameter(prs,'printEvery',1);
addParameter(prs,'tol',1e-6);
addParameter(prs,'tolX',1e-6);
parse(prs,varargin{:});
linesearch      = prs.Results.linesearch;
initialStepsize = prs.Results.initialStepsize;
c               = prs.Results.backtrack_c;
rho             = prs.Results.backtrack_rho;
maxIts          = prs.Results.maxIts;
printEvery      = prs.Results.printEvery;
tol             = prs.Results.tol;
tolX            = prs.Results.tolX;

t       = initialStepsize;
fOld    = Inf;
counter = 0;
for k = 1:maxIts
    
    [f,g]   = fcn(x);
    
    if linesearch  % simple backtracking linesearch
        if counter == 0 && k > 1
            t       = 2*t; % be aggressive
        end
        counter = 0;
        while fcn(x - t*g) > f - t*c*norm(g)^2
            counter = counter + 1;
            t       = rho*t;
        end
    end
    x_new   = x - t*g;
    
    
    dx      = norm(x_new - x )/norm(x);
    df      = abs(f-fOld)/abs(f);
    x       = x_new;
    
    if k>1 && df < tol
        fprintf('Stopping due to convergence in objective\n');
        break
    end
    
    if dx < tolX
        fprintf('Stopping due to convergence in variable\n');
        break
    end
    if ~mod(k,printEvery)
        fprintf('Iter %4d, f is %.2e, norm(g) is %.2e, linesearch steps %2d \n', k, f, norm(g), counter );
    end
end
