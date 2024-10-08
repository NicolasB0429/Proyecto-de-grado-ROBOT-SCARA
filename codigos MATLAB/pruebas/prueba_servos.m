clear all
close all
clc

a=arduino();
s1=servo(a,'D10');
s2=servo(a,'D11');
l1 = 10;
l2 = 10;

writePosition(s1,0);
writePosition(s2,0);

%Punto 1
Px1 = 20;
Py1 = 0;
[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Px1,Py1);

%Punto 2
Px2 = input('Digite la coordenada X \n');
Py2 = input('Digite la coordenada Y \n');
[theta1_P2, theta2_P2] = CI_Funcion_2R(l1,l2,Px2,Py2);

theta1P1_P2 = linspace(theta1_P1,theta1_P2,10);
theta2P1_P2 = linspace(theta2_P1,theta2_P2,10);

for i=1:length(theta2P1_P2)
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2(i),theta2P1_P2(i));
    writePosition(s1,theta1P1_P2(i)/pi);
    writePosition(s2,theta2P1_P2(i)/pi);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end