%{
Compare the speed of matrix multiplication, of my simple C for loop
 vs using Matlab's version (which calls Intel's MKL BLAS)

%}

% Compile, if not already done:
% mex multiplyMatrices.c -O

% First, convince you that my function gives the right answer
A   = randn(50,51);
B   = randn(51,52);  % pick rectangular, helps find bugs
C   = multiplyMatrices(A,B);
err = norm( C - A*B, 'fro' )/norm( A*B, 'fro' );
fprintf('Error is: %g\n', err );

%% Now, try some speed tests

nList   = [50,100,500,800,1e3,1.2e3,1.5e3];
nReps   = 3;
[results1,results2] = deal( zeros( nReps,length(nList) ) );
for ni = 1:length(nList)
    n   = nList(ni);
    A   = randn(n);
    B   = randn(n);
    
    for rep = 1:nReps
        tic;
        C   = multiplyMatrices( A, B );
        t   = toc;
        
        results1(rep,ni)    = t;
        
        tic;
        C   = A*B;
        t   = toc;
        
        results2(rep,ni)    = t;
    end
end

%% Plot
figure(1); clf;
loglog( nList, mean(results1), 'o--', 'linewidth', 2,'markersize',10 );
hold all
loglog( nList, mean(results2), '*--', 'linewidth', 2,'markersize',10 );
set(gca,'fontsize',20);
legend('My implementation','Matlab''s implementation','location','northwest');
title('Time to multiply n x n matrices');
ylabel('Time (s)');
xlabel('Dimension n');
xlim([50,1.6e3]);
text( 100,.5,  'At n=1500, C code took 27 sec, Matlab took 0.17 sec' );
export_fig 'MultiplyMatrices_C' '-pdf' '-transparent'