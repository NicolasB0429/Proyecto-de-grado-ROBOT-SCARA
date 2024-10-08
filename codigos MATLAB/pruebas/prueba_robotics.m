clear all
close all
clc

l1 = 7;
l2 = 9;

% ---------------------------------------------------------
Px = 16;
Py = 0;

%Theta2
b = sqrt(Px^2+Py^2);
cos_theta2 = (b^2-l2^2-l1^2)/(2*l2*l1);
sen_theta2 = sqrt(1-(cos_theta2)^2);
theta2 = atan2(sen_theta2,cos_theta2);
fprintf('Theta2 = %.3f \n', radtodeg(theta2));
%Theta1
alpha = atan2(Py,Px);
phi = atan2((l2*sen_theta2),(l1+l2*cos_theta2));
theta1 = alpha - phi;
fprintf('Theta1 = %.3f \n',rad2deg(theta1));
%-----------------------------------------------------------
q1 = theta1;
q2 = theta2;

q = [q1,q2];

R(1) = Link('revolute','d',0,'alpha',0,'a',l1,'offset',0);
R(2) = Link('revolute','d',0,'alpha',0,'a',l2,'offset',0);
Robot = SerialLink(R);

Robot.plot(q,'scale',1.0,'workspace',[-30 30 -30 30 -30 30]);
zlim([-10,20]);
Robot.teach(q);
Robot.fkine(q); 
