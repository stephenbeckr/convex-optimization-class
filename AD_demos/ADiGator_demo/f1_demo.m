function [] = f1_demo()
   %function [y] = f1(x,scale)
   %% Like the simple example we used in class.
   %% https://en.wikipedia.org/wiki/Automatic_differentiation
   %
   %   y = scale*(x(1)*x(2) + sin(x(1)));
   % 
   %end

   % print source
   type f1
   fprintf('\n');
   
   % Set up inputs (and optionally parameters)
   x = adigatorCreateDerivInput([2 1], 'x');
   aux = adigatorCreateAuxInput([1 1]);
   
   % Generate the derivative function file
   opt = adigatorOptions('overwrite', 1); % overwrite existing generated AD sources
   adigator('f1', {x, aux}, 'Df1', opt);

   % Call the derivative
   x = [1; 2];
   scale = 1;
   x_ad = struct('f', x, 'dx', ones([2 1]));
   y = Df1(x_ad, scale)
   fprintf('Derivative with ADiGator:\n');
   y.dx
   
   fprintf('Check derivative with analytic derivative:\n');
   Df1_check(x, scale)

end

function [dx] = Df1_check(x, scale)
   
   dx = scale*[x(2) + cos(x(1)); x(1)];
   
end
