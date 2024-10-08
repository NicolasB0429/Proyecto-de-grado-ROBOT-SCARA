%%Contorno de toda el área de trabajo
clear all
close all
clc

load("contorno.mat");

l1 = 10; % Eslabon 1
l2 = 10; % Eslabon 2

% theta1P1_P2 = 0;
% theta2P1_P2 = linspace(pi,0,10);
% x1y1 = zeros(length(theta2P1_P2), 2);
% for i=1:length(theta2P1_P2)
%     MTH = CD_Funcion_2R(l1,l2,theta1P1_P2,theta2P1_P2(i));
%     x1y1(i,1) = MTH.t(1);
%     x1y1(i,2) = MTH.t(2);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*');
% end
% 
% theta1P2_P3 = linspace(0,pi/2,10);
% theta2P2_P3 = 0;
% x2y2 = zeros(length(theta2P2_P3), 2);
% for i=1:length(theta1P2_P3)
%     MTH = CD_Funcion_2R(l1,l2,theta1P2_P3(i),theta2P2_P3);
%     x2y2(i,1) = MTH.t(1);
%     x2y2(i,2) = MTH.t(2);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*');
% end
% 
% theta1P3_P4 = linspace(pi/2,pi,10);
% theta2P3_P4 = 0;
% x3y3 = zeros(length(theta2P3_P4), 2);
% for i=1:length(theta1P3_P4)
%     MTH = CD_Funcion_2R(l1,l2,theta1P3_P4(i),theta2P3_P4);
%     x3y3(i,1) = MTH.t(1);
%     x3y3(i,2) = MTH.t(2);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*');
% end
% 
% theta1P4_P5 = pi;
% theta2P4_P5 = linspace(0,pi,10);
% x4y4 = zeros(length(theta2P4_P5), 2);
% for i=1:length(theta2P4_P5)
%     MTH = CD_Funcion_2R(l1,l2,theta1P4_P5,theta2P4_P5(i));
%     x4y4(i,1) = MTH.t(1);
%     x4y4(i,2) = MTH.t(2);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*');
% end

%DESDE ACÁ SE COMPARA
xu = -20;
yu = 0;


flag1 = 0; %Comparación sección derecha
flag2 = 0; %Comparación sección izquierda

for i=1:length(x1y1) %Derecha abajo
    if x1y1(i,1) >= xu 
        if x1y1(i,2) <= yu
            disp("1.cumple x y y");
            %disp(i);
            flag1 = flag1 + 1; 
            break
        else
            disp("1.solo cumple x");
            %disp(i);
            break
        end
    end
    %disp(i);
end

for i=1:length(x2y2) %Derecha arriba
    if x2y2(i,1) <= xu 
        if x2y2(i,2) >= yu
            disp("2.cumple x y y");
            %disp(i);
            flag1 = flag1 + 1;
            break
        else
            disp("2.solo cumple x");
            %disp(i);
            break
        end
    end
    %disp(i);
end

if flag1 == 2
    disp("Esta dentro del rango de la sección derecha");
else
    disp("No esta dentro del rango de la sección derecha");
end

for i=1:length(x3y3) %Izquierda arriba
    if x3y3(i,1) <= xu 
        if x3y3(i,2) >= yu
            disp("3.cumple x y y");
            %disp(i);
            flag2 = flag2 + 1; 
            break
        else
            disp("3.solo cumple x");
            %disp(i);
            break
        end
    end
    %disp(i);
end

for i=1:length(x4y4) %Izquierda abajo
    if x4y4(i,1) >= xu 
        if x4y4(i,2) <= yu
            disp("4.cumple x y y");
            %disp(i);
            flag2 = flag2 + 1;
            break
        else
            disp("4.solo cumple x");
            %disp(i);
            break
        end
    end
    %disp(i);
end

if flag2 == 2
    disp("Esta dentro del rango de la sección izquierda");
else
    disp("No esta dentro del rango de la sección izquierda");
end

%% Secciones dónde se van a dibujar las imagenes
clear all
close all
clc

l1 = 10; % Eslabon 1
l2 = 10; % Eslabon 2

% % SECCIÓN DE IMAGEN HORIZONTAL
% x1 = -10;
% y1 = 16.5; 
% x2 = 10;
% y2 = 16.5; % Y no cambia
% 
% pxf = linspace(x1,x2,10);
% pyf = y2;
% 
% for i=1:length(pxf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% x3 = 10; % X no cambia
% y3 = 10.5; 
% 
% pxf = x3;
% pyf = linspace(y2,y3,10);
% 
% for i=1:length(pyf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% x4 = -10;
% y4 = 10.5; % Y no cambia
% 
% pxf = linspace(x3,x4,10);
% pyf = y4;
% 
% for i=1:length(pxf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% pxf = x4;
% pyf = linspace(y4,y1,10);
% 
% for i=1:length(pyf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end

% % SECCIÓN DE IMAGEN CUADRADA
% x1 = -10;
% y1 = 15; 
% x2 = 0;
% y2 = 15; % Y no cambia
% 
% pxf = linspace(x1,x2,10);
% pyf = y2;
% 
% for i=1:length(pxf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% x3 = 0; % X no cambia
% y3 = 5; 
% 
% pxf = x3;
% pyf = linspace(y2,y3,10);
% 
% for i=1:length(pyf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% x4 = -10;
% y4 = 5; % Y no cambia
% 
% pxf = linspace(x3,x4,10);
% pyf = y4;
% 
% for i=1:length(pxf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end
% 
% pxf = x4;
% pyf = linspace(y4,y1,10);
% 
% for i=1:length(pyf)
%     [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
%     MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%     %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
%     hold on;
%     plot(MTH.t(1),MTH.t(2),'*r');
% end

% SECCIÓN DE IMAGEN VERTICAL

x1 = -15;
y1 = 10; 
x2 = -5;
y2 = 10; % Y no cambia

pxf = linspace(x1,x2,10);
pyf = y2;

for i=1:length(pxf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end
 
x3 = -5; % X no cambia
y3 = -5; 

pxf = x3;
pyf = linspace(y2,y3,10);

for i=1:length(pyf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end

x4 = -15;
y4 = -5; % Y no cambia

pxf = linspace(x3,x4,10);
pyf = y4;

for i=1:length(pxf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf(i),pyf);
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end

pxf = x4;
pyf = linspace(y4,y1,10);

for i=1:length(pyf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,pxf,pyf(i));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    %PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end

%% REDIMENCIONAR IMAGEN hyundai

clc;
clear all;
close all;

l1 = 14;
l2 = 11;

% Cargar la imagen
imagen = imread('hyundai.jpg');

% Plotear la imagen
% imshow(imagen);

imagen_gris = rgb2gray(imagen);
imagen_binaria = imbinarize(imagen_gris);

% Obtener los contornos de los objetos en la imagen binaria
[contornos, L, n] = bwboundaries(imagen_binaria);

%Estudiar Arreglar los y
offset = 820;
contornos{1,1}(:,1) = contornos{1,1}(:,1)*(-1) + offset; %Y del contorno 1
contornos{2,1}(:,1) = contornos{2,1}(:,1)*(-1) + offset; %Y del contorno 1
contornos{3,1}(:,1) = contornos{3,1}(:,1)*(-1) + offset; %Y del contorno 1
contornos{4,1}(:,1) = contornos{4,1}(:,1)*(-1) + offset; %Y del contorno 1
contornos{5,1}(:,1) = contornos{5,1}(:,1)*(-1) + offset; %Y del contorno 1
contornos{6,1}(:,1) = contornos{6,1}(:,1)*(-1) + offset; %Y del contorno 1

% Crear una matriz de celdas vacía con las mismas dimensiones
arreglo = cell(size(contornos)-1); %menos la margen de la imagen

% Copiar los valores sin el primer elemento
for i = 1:length(contornos)-1
    arreglo{i} = contornos{i+1}/100;
end

% hold on
% for i = 1:length(arreglo)
%     boundary = arreglo{i};
%     plot(boundary(:,2), boundary(:,1), 'g','LineWidth',2);
% end
% hold off

% Vector sumando las coordenadas
%Contorno 1
for i = 1:length(arreglo{1})
    arregloM1(i,1) = arreglo{1}(i,1) +5;
    arregloM1(i,2) = arreglo{1}(i,2) -10;
end

%Contorno 2
for i = 1:length(arreglo{2})
    arregloM2(i,1) = arreglo{2}(i,1) +5;
    arregloM2(i,2) = arreglo{2}(i,2) -10;
end
%Contorno 3
for i = 1:length(arreglo{3})
    arregloM3(i,1) = arreglo{3}(i,1) +5;
    arregloM3(i,2) = arreglo{3}(i,2) -10;
end
%Contorno 4
for i = 1:length(arreglo{4})
    arregloM4(i,1) = arreglo{4}(i,1) +5;
    arregloM4(i,2) = arreglo{4}(i,2) -10;
end
%Contorno 5
for i = 1:length(arreglo{5})
    arregloM5(i,1) = arreglo{5}(i,1) +5;
    arregloM5(i,2) = arreglo{5}(i,2) -10;
end

figure
axis([-10 0 5 15])
hold on;
for i = 1:length(arregloM1)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM1(i,2),arregloM1(i,1));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    plot(MTH.t(1),MTH.t(2),'.r');
%     plot(arregloM1(:,2), arregloM1(:,1), 'b','LineWidth',2);
end

for i = 1:length(arregloM2)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM2(i,2),arregloM2(i,1));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    plot(MTH.t(1),MTH.t(2),'.r');
%     plot(arregloM2(:,2), arregloM2(:,1), 'b','LineWidth',2);
end

for i = 1:length(arregloM3)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM3(i,2),arregloM3(i,1));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    plot(MTH.t(1),MTH.t(2),'.r');
%     plot(arregloM3(:,2), arregloM3(:,1), 'b','LineWidth',2);
end

for i = 1:length(arregloM4)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM4(i,2),arregloM4(i,1));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    plot(MTH.t(1),MTH.t(2),'.r');
%     plot(arregloM4(:,2), arregloM4(:,1), 'b','LineWidth',2);
end

for i = 1:length(arregloM5)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM5(i,2),arregloM5(i,1));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    plot(MTH.t(1),MTH.t(2),'.r');
%     plot(arregloM5(:,2), arregloM5(:,1), 'b','LineWidth',2);
end

hold off;

%% hyundai Otra prueba

clc;
clear all;
close all;

l1 = 10;
l2 = 10;
% Cargar la imagen
imagen = imread('hyundai.jpg');

imagen_gris = rgb2gray(imagen);
imagen_binaria = imbinarize(imagen_gris);

% Obtener los contornos de los objetos en la imagen binaria
[contornos, L, n] = bwboundaries(imagen_binaria);

% Arreglar todos los Y
offset = 850; 
for i = 1:length(contornos)
    contornos{i,1}(:,1) = contornos{i,1}(:,1)*(-1) + offset;
end

% Crear una matriz de celdas vacía con las mismas dimensiones
arreglo = cell(size(contornos)-1); %menos el contorno

% Copiar los valores sin el primer elemento y dividirlo entre 100
for i = 1:length(contornos)-1
    arreglo{i,1} = contornos{i+1}/100;
end

% Sumando las coordenadas
for i = 1:length(arreglo)
    for j = 1:length(arreglo{i,1})
        arreglo{i,1}(j,1) = arreglo{i,1}(j,1) + 5; %Y
        arreglo{i,1}(j,2) = arreglo{i,1}(j,2) - 10; %X
    end
end

%Gragicar (Plotear)
hold on;
for i = 1:length(arreglo)
    for j = 1:length(arreglo{i})
%         [theta1, theta2] = CI_Funcion_2R(l1,l2,arreglo{i,1}(i,2),arreglo{i,1}(i,1));
%         MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%         PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
%         plot(MTH.t(1),MTH.t(2),'.r');

        plot(arreglo{i,1}(:,2), arreglo{i,1}(:,1), 'b','LineWidth',2);
    end
end
hold off

%% Imagen Universidad Ecci
clc;
clear all;
close all;

l1 = 10;
l2 = 10;

% Cargar la imagen
imagen = imread('ecci.png');

imagen_gris = rgb2gray(imagen);
imagen_binaria = imbinarize(imagen_gris);

% Obtener los contornos de los objetos en la imagen binaria
[contornos, L, n] = bwboundaries(imagen_binaria);

% Arreglar todos los Y
offset = 500; %370
for i = 1:length(contornos)
    contornos{i,1}(:,1) = contornos{i,1}(:,1)*(-1) + offset;
end

%Dividir todo entre 100
for i = 1:length(contornos)
    contornos{i} = contornos{i}/100;
end

% %Plotearlo sin el rango especi
% hold on
% for i = 1:length(contornos)
%     boundary = contornos{i};
%     plot(boundary(:,2), boundary(:,1), 'b','LineWidth',2);
% end
% hold off

% Sumando las coordenadas
for i = 1:length(contornos)
    for j = 1:length(contornos{i,1})
        contornos{i,1}(j,1) = contornos{i,1}(j,1) + 10.5; %Y
        contornos{i,1}(j,2) = contornos{i,1}(j,2) - 10; %X
    end
end

%Gragicar (Plotear)
figure
axis([-10 10 10.5 16.5])
hold on;

for i = 1:length(contornos)
    %for j = 1:length(contornos{i})
%         [theta1, theta2] = CI_Funcion_2R(l1,l2,arregloM1(i,2),arregloM1(i,1));
%         MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%         plot(MTH.t(1),MTH.t(2),'.r');
        plot(contornos{i,1}(:,2), contornos{i,1}(:,1), 'b','LineWidth',2);
    %end
end

hold off

