function x = my_upsample( y, sampleSet, n )
% x = my_upsample( y, sampleSet, n )
%   returns x of length n such that x(sampleSet) = y
x   = zeros(n,size(y,2));
x(sampleSet,:)  = y;
