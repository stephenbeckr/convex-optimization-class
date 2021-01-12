function coeff = forwardShortTimeDCT( y, win )
% coeff = forwardShortTimeDCT( y, win )
%   applies the Modified DCT to the signal y
%   This is a linear function.
%   Assumes y is a column vector of length N
%   The blockSize is encoded in the length of win
%   This code then uses a lapped (50% overlapping)
%   DCT on segments of y of length blockSize.
%
%   Note: this function zero-pads y to be an even multiple of blockSize
%
% An example window that we recommend, so that
%   the transpose of this function is its pseudo-inverse,
%   is:
%   win         = sin( pi*( (1:blockSize) + 1/2)/(blockSize) );
%   (a typical value of blockSize = 1024)
%   This satisifes the Princen-Bradley conditions, meaning that
%   we can guarantee   win.^2 + circshift( win, blockSize/2).^2  =  1
%
% Stephen Becker, 3/18/2017
% See also adjointShortTimeDCT.m

N           = length(y);
blockSize   = length(win);
% Make y be a multiple of the blockSize by zero-padding
nBlocks     = ceil( N/blockSize );
y           = [y; zeros(blockSize*nBlocks-N,1) ];

Win         = spdiags(win(:),0,blockSize,blockSize);

Y           = reshape( y, blockSize, nBlocks );
C           = dct( Win*Y );

% and 50% shift
Y           = reshape( circshift(y,-blockSize/2), blockSize, nBlocks );
C2          = dct( Win*Y );

coeff       = [ C(:); C2(:) ];
% or instead, intersperse
% coeff       = [C;C2]; coeff = coeff(:);
