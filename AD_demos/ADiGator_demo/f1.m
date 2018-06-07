function [y] = f1(x,scale)
% Like the simple example we used in class.
% https://en.wikipedia.org/wiki/Automatic_differentiation

   y = scale*(x(1)*x(2) + sin(x(1)));

end
