function x = gradientDescent_Nesterov( fcn, x, varargin )
% x = gradientDescent_Nesterov( fcn, x )
%   solves min_x f(x)
%   where [f,g] = fcn(x) returns f(x) and \nabla f(x)
%
% x = gradientDescent_Nesterov( fcn, x, 'parameter','value', 'parmeter2','value2',... )
%   allows control of options (see code for a list, e.g., 'linesearch');
%
% in particular, using 'prox', @(x,t)proxFcn(x,t)
%   allows this to solve (accelerated) proximal gradient descent,
%   i.e., FISTA "A Fast Iterative Shrinkage-Thresholding Algorithm for
%   Linear Inverse Problems" by Beck and Teboulle 2009
%       http://dl.acm.org/citation.cfm?id=1658364
%
% Other available parameters are:
%   linesearch          if true, does backtracking linesearch
%                           (out of laziness, this is not possible in
%                           proximal mode, but that could easily be fixed)
%   backtrack_c, backtrack_rho      backtracking parameters
%   initialStepsize     stepsize (if linesearch is false, this stepsize is
%                           used for all iterations)
%   maxIts              max number of iterations
%   printEvery          how often to print (printEvery=10 means print output to 
%                           screen every 10 iterations)
%   tol                 relative tolerance in the objective
%   tolX                relative tolerance in ||x_{k} - x_{k-1}||
%   acceleration        whether to use Nesterov acceleration (default:
%                           true)
%   restart             how often to restart the momentum term used in
%                           Nesterov's acceleration -- see
%                           "Adaptive Restart..." arxiv.org/abs/1204.3982
%
% Stephen.Becker@Colorado.edu, 3/13/2017


prs = inputParser;
addParameter(prs,'linesearch',true);
addParameter(prs,'acceleration',true);
addParameter(prs,'initialStepsize',1); % e.g. 1/L
addParameter(prs,'backtrack_c',1e-4);
addParameter(prs,'backtrack_rho',0.9);
addParameter(prs,'maxIts',1e4);
addParameter(prs,'printEvery',1);
addParameter(prs,'tol',1e-6);
addParameter(prs,'tolX',1e-6);
addParameter(prs,'prox',[]);
addParameter(prs,'restart',Inf);
parse(prs,varargin{:});
linesearch      = prs.Results.linesearch;
initialStepsize = prs.Results.initialStepsize;
c               = prs.Results.backtrack_c;
rho             = prs.Results.backtrack_rho;
maxIts          = prs.Results.maxIts;
printEvery      = prs.Results.printEvery;
tol             = prs.Results.tol;
tolX            = prs.Results.tolX;
acceleration    = prs.Results.acceleration;
restart         = prs.Results.restart;
prox            = prs.Results.prox;
if isempty(prox)
    DO_PROX     = false;
    prox        = @(x,t) x; 
else
    DO_PROX     = true;
end
if isempty(restart), restart = Inf; end

t       = initialStepsize;
fOld    = Inf;
counter = 0;
if acceleration
    y   = x;
    if linesearch
        error('not yet implemented');
    end
end
kk  = 0;
for k = 1:maxIts
    kk = kk + 1;
    if acceleration
        [f,g]   = fcn(y);
    else
        [f,g]   = fcn(x);
    end
    
    if linesearch  % simple backtracking linesearch
        if DO_PROX
            error('Have not implemented line search for proximal gradient descent yet');
        end
        if counter == 0 && k > 1
            t       = 2*t; % be aggressive
        end
        counter = 0;
        while fcn(x - t*g) > f - t*c*norm(g)^2
            counter = counter + 1;
            t       = rho*t;
        end
    end
    
    if acceleration
        x_new   = prox(y - t*g,t);
        y   = x_new + kk/(kk+3)*(x_new-x);
    else
        x_new   = prox(x - t*g,t);
    end
    if ~isinf(restart) && ~mod(k,restart)
        % reset the counter used in the momentum term
        kk  = 0;
    end
    
    
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