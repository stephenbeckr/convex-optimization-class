%{
For HW 10 to demonstrate listening to the "Handel" audio file

Stephen Becker, 3/18/2017
%}

load handel.mat  % loads y, Fs

%% Play the sound
playerObj = audioplayer(y,Fs);
play( playerObj )
%% Play the down-sampled sound (by a factor of 2)
playerObj = audioplayer(y(1:2:end),Fs/2);
play( playerObj )
%% Play the down-sampled sound (by a factor of 4)
playerObj = audioplayer(y(1:4:end),Fs/4);
play( playerObj )
%% Filter-then-downsample to avoid aliasing
% first low-pass filter it
Rp  = 1e-3;      % for peak-to-peak ripple
Rst = 1e-3;      % for stopband attenuation
ordr= 100;       % filter order
eqnum   = firceqrip( ordr, 1/4, [Rp Rst], 'passedge');
% fvtool(eqnum, 'Fs',Fs ); % Visualize the filter's frequency response
lowpassFIR = dsp.FIRFilter('Numerator',eqnum);
yFiltered  = lowpassFIR( y );

% playerObj = audioplayer(yFiltered,Fs);
playerObj = audioplayer(yFiltered(1:4:end),Fs/4);
play( playerObj )

%% Plot spectrograms
% Use pwelch estimate instead of "spectrogram" function
blockSize   = 1e3;
win         = window( @barthannwin, blockSize );
figure(1);
subplot(2,2,1);
pwelch( y, win, [], [], Fs ); title('Original signal');
subplot(2,2,2);
pwelch( y(1:4:end), win, [], [], Fs/4 ); title('Downsampled (aliased)');
subplot(2,2,3);
pwelch( yFiltered, win, [], [], Fs ); title('Filtered');
subplot(2,2,4);
pwelch( yFiltered(1:4:end), win, [], [], Fs/4 ); title('Filtered-then-downsampled');


%% and a time-frequency plot
figure(3);
spectrogram( y, 5e2, [], [], Fs )
title('Spectrogram');