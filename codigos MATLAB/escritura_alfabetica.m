clear all
close all
clc

global a l1 l2 Px Py s1 s2;
a=arduino();
s1=servo(a,'D10');
s2=servo(a,'D11');
l1 = 10;
l2 = 10;

writePosition(s1,0);
writePosition(s2,0);


palabra = input('Digite el NOMBRE a escribir: ','s');

%PUNTOS INICIALES
%Punto 1
Px1 = 20;
Py1 = 0;
[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Px1,Py1);

%Punto 2
Px = -13;
Py = 11; 
[theta1_P2, theta2_P2] = CI_Funcion_2R(l1,l2,Px,Py);

theta1P1_P2 = linspace(theta1_P1,theta1_P2,10);
theta2P1_P2 = linspace(theta2_P1,theta2_P2,10);

for i=1:length(theta2P1_P2)
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2(i),theta2P1_P2(i));
    writePosition(s1,theta1P1_P2(i)/pi);
    writePosition(s2,theta2P1_P2(i)/pi);
    hold on;
    plot(MTH.t(1),MTH.t(2));
end

if length(palabra) <= 9
    for i=1:length(palabra) %longitud de vector palabra
        [Pxf,Pyf] = Funcion_Abecedariot(palabra(i),Px, Py);
        Px = Pxf;
        Py = Pyf;
    end

else
   disp('Su nombre es muy Largo Mrs'); 
end

function [Pxf,Pyf] = Funcion_Abecedariot(palabra,x, y)

    global Px Py;
   
    if palabra == 'a' || palabra== 'A'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'b' || palabra== 'B'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'c' || palabra== 'C'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'd' || palabra== 'D'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'e' || palabra== 'E'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end 

    if palabra == 'f' || palabra== 'F'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end 

    if palabra == 'g' || palabra== 'G'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'h' || palabra== 'H'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'i' || palabra== 'I'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

if palabra == 'j' || palabra== 'J'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'k' || palabra== 'K'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(2, 1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-2, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(2, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'l' || palabra== 'L'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'm' || palabra== 'M'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'n' || palabra== 'N' || palabra == 'ñ' || palabra== 'Ñ'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(2, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'o' || palabra== 'O'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'p' || palabra== 'P'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'q' || palabra== 'Q'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, 1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'r' || palabra== 'R'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 's' || palabra== 'S'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 't' || palabra== 'T'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'u' || palabra== 'U'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'v' || palabra== 'V'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'w' || palabra== 'W'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'x' || palabra== 'X'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_diagonal(2, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, 1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(2, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(1,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'y' || palabra== 'Y'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_diagonal(2, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, 1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_diagonal(-1, -1,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end

    if palabra == 'z' || palabra== 'Z'
        Px1 = Px;
        Py1 = Py;
        [Pxf,Pyf] = linea_diagonal(2, 2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(-2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;        
        [Pxf,Pyf] = linea_diagonal(-2, -2,Px1, Py1);
        Px1 = Pxf;
        Py1 = Pyf;
        [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
        Px = Px1;
        Py = Py1;
    end
end

function [Pxf,Pyf] = linea_vertical(longitud,Px1, Py1)
    global l1 l2 s1 s2;

    Pxf = Px1; 
    Pyf = Py1 + longitud; 
        
    Px7_Pxf = Pxf;
    Py7_Pyf = linspace(Py1, Pyf, 6);
    
    for i=1:6
        [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf,Py7_Pyf(i));
        MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
        writePosition(s1,theta1/pi);
        writePosition(s2,theta2/pi);
        hold on;
        plot(MTH.t(1),MTH.t(2),'.r');
    end
end

function [Pxf,Pyf] = linea_horizantal(longitud,Px1, Py1)
    global l1 l2 s1 s2;

    Pxf = Px1 + longitud; 
    Pyf = Py1; 
        
    Px7_Pxf = linspace(Px1, Pxf, 6);
    Py7_Pyf = Pyf;
    
    for i=1:6
        [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf(i),Py7_Pyf);
        MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
        writePosition(s1,theta1/pi);
        writePosition(s2,theta2/pi);
        hold on;
        plot(MTH.t(1),MTH.t(2),'.r');
    end
end

function [Pxf,Pyf] = linea_diagonal(longitudx, longitudy,Px1, Py1)
    global l1 l2 s1 s2;

    Pxf = Px1 + longitudx; 
    Pyf = Py1 + longitudy; 
        
    Px7_Pxf = linspace(Px1, Pxf, 6);
    Py7_Pyf = linspace(Py1, Pyf, 6);
    
    for i=1:6
        [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf(i),Py7_Pyf(i));
        MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
        writePosition(s1,theta1/pi);
        writePosition(s2,theta2/pi);
        hold on;
        plot(MTH.t(1),MTH.t(2),'.r');
    end
end 
