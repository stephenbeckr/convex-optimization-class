%{
Demonstration of effect of memory/communication cost
 on performance

Stephen Becker, June 11 2018
%}

n   = 5e3;
A   = randn(n);
X   = randn(n);

blockSizes  = [1, 5, 10, 20, 100, 1e3, 5e3 ];
times       = zeros( length(blockSizes), 1 );

for i   = 1:length(blockSizes)
    fprintf('i is %d\n', i );
    block   = blockSizes( i );
    if block < 1e2
        reps    = round( 1e2/block );
    elseif block < 1e3
        reps    = round( 1e3/block );
    else
        reps    = round( 1e4/block );
    end
    % to get accurate timing, we'll repeat this
    t1 = tic;
    for trial = 1:reps
        y   = A*X(:,1:block);
    end
    tm  = toc(t1);
    tm  = tm/reps;
    times(i)    = tm;
end
%% Display results
figure(1); clf;
loglog( blockSizes, times, 'o--','markersize',12,'linewidth',2 )
set(gca,'fontsize',18);
xlabel('n');
ylabel('Time to multiply A*X(:,1:n)');
hold all
loglog( blockSizes, blockSizes*times(2)/blockSizes(2), ':','linewidth',2  )
loglog( blockSizes, blockSizes*times(5)/blockSizes(5), ':','linewidth',2  )
ylim([1e-2,10]);

%% Display them another way
figure(2); clf;
semilogx( blockSizes, times.*(n./blockSizes'), 'o--','markersize',12,'linewidth',2 )
set(gca,'fontsize',18);
xlabel('n');
ylabel('Time to multiply A*X');
hold all