function y = adjointShortTimeDCT( coeff, win, Ntrue )
% y = adjointShortTimeDCT( coeff, win )
%   applies the adoint/transpose MDCT to the coefficients "coeff"
%   This is also the pseudo-inverse of the forward MDCT
%
% y = adjointShortTimeDCT( coeff, win, N_original )
%   should be used when the forward MDCT is applied to signals
%   of length N_original. We need to know N_original so we can
%   undo the zero-padding (which is done when N_original is not
%   a multiple of the blockSizez)
%
% see forwardShortTimeDCT.m for an example of the window "win"
%
% Stephen Becker, 3/18/2017
% See also forwardShortTimeDCT.m


N           = length(coeff)/2;
blockSize   = length(win);
nBlocks     = ceil( N/blockSize );
if nargin >= 3
    assert( Ntrue <= N );
else
    Ntrue = [];
end

Win         = spdiags(win(:),0,blockSize,blockSize);

C           = reshape( coeff(1:N), blockSize, nBlocks );
Y           = Win*idct( C );
y           = Y(:);

C           = reshape( coeff(N+1:end), blockSize, nBlocks );
Y2          = Win*idct( C );
y2          = circshift(Y2(:),blockSize/2);

y           = y + y2;

if ~isempty(Ntrue)
    y   = y(1:Ntrue);
end
