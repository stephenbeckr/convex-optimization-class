% This file uses both MATLAB finite differences as well as adigator in order
% to compute derivatives of the fit.m function. The user can change m and n
% to change to problem size.
% Copyright 2011-2014 Matthew J. Weinstein and Anil V. Rao
% Distributed under the GNU General Public License version 3.0
m = 8;
n = 100;
TOL = 1e-5;

x = floor(rand(n,1)*1000)/1000;
d = floor(rand(n,1)*1000)/1000;
numeval = 25;

% Create the Jacobian file
tic
gx = adigatorCreateDerivInput([n,1],'x');
adigatorGenJacFile('fit',{gx,d,m});
gentime = toc;


% Use the ADiGator generated Jacobian file
tic
for i = 1:numeval
  [J,p] = fit_Jac(x,d,m);
end
adigatortime = toc/numeval;


% numerically compute the Jacobian using FD
tic
for i = 1:numeval
  dpdx2 = numjac(@(t,x)fit4numjac(t,x,d,m),0,x,p,TOL*ones(n,1),[],0);
end
fdtime = toc/numeval;


fprintf('Derivatives of fit function:\n');
fprintf(['m = %1.0f, n = %1.0f, TOL = ',num2str(TOL),'\n'],m,n);
fprintf(['ADiGator File Generation Time: ',num2str(gentime),'\n']);
fprintf(['ADiGator Average Eval Time:    ',num2str(adigatortime),'\n']);
fprintf(['F Diff Average Eval Time:      ',num2str(fdtime),'\n']);
