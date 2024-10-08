clear all
close all
clc

l1 = 10; %9.5
l2 = 10; %10.8

theta1P1_P2 = 0;
theta2P1_P2 = linspace(0,pi,10);
for i=1:10
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2,theta2P1_P2(i));
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end

theta1P2_P3 = 0;
theta2P2_P3 = linspace(pi,0,10);
for i=1:10
    MTH = CD_Funcion_2R(l1,l2,theta1P2_P3,theta2P2_P3(i));
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end

theta1P3_P4 = linspace(0,pi,10);
theta2P3_P4 = 0;
for i=1:10
    MTH = CD_Funcion_2R(l1,l2,theta1P3_P4(i),theta2P3_P4);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end

theta1P4_P5 = pi;
theta2P4_P5 = linspace(0,pi,10);
for i=1:10
    MTH = CD_Funcion_2R(l1,l2,theta1P4_P5,theta2P4_P5(i));
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end
