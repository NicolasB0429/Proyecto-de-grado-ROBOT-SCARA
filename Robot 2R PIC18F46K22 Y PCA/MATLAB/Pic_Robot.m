function varargout = Pic_Robot(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Pic_Robot_OpeningFcn, ...
                   'gui_OutputFcn',  @Pic_Robot_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

function Pic_Robot_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
guidata(hObject, handles);

% Leer la imagen
imagen = imread('universidad.jpg');

% Mostrar la imagen en el objeto "Axes"
imshow(imagen, 'Parent', handles.axes2);

global l1 l2 punto2 Pxpunto2 Pypunto2;  %Variables globales

%Variables del punto 2
punto2 = 0;
Pxpunto2 = 0;
Pypunto2 = 0;
PuertoSerial(0,0);

%Eslabones
l1 = 10;
l2 = 10;


function varargout = Pic_Robot_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;

% COORDENADAS
function pushbutton1_Callback(hObject, eventdata, handles)

global l1 l2 punto2 Pxpunto2 Pypunto2;
load("contorno.mat"); % carga variables del contorno

axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

%Solo una vez posición inicial
if punto2 == 0
    Pxpunto2 = 20;
    Pypunto2 = 0;
    punto2= punto2+1; 
end

[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Pxpunto2,Pypunto2);

Px2 = str2num(get(handles.edit1,'string'));
Py2 = str2num(get(handles.edit2,'string'));

flag1 = 0; %Comparación sección derecha
flag2 = 0; %Comparación sección izquierda

%Comparar si esta dentro del entorno de trabajo
for i=1:length(x1y1) %Derecha abajo
    if x1y1(i,1) >= Px2 
        if x1y1(i,2) <= Py2 
            flag1 = flag1 + 1; 
            break
        end
    end
end

for i=1:length(x2y2) %Derecha arriba
    if x2y2(i,1) <= Px2 
        if x2y2(i,2) >= Py2 
            flag1 = flag1 + 1;           
            break
        end
    end
end

for i=1:length(x3y3) %Izquierda arriba
    if x3y3(i,1) <= Px2 
        if x3y3(i,2) >= Py2 
            flag2 = flag2 + 1; 
            break
        end
    end
end

for i=1:length(x4y4) %Izquierda abajo
    if x4y4(i,1) >= Px2 
        if x4y4(i,2) <= Py2 
            flag2 = flag2 + 1;
            break
        end
    end
end

if flag1 == 2 || flag2 == 2 
    [theta1_P2, theta2_P2] = CI_Funcion_2R(l1,l2,Px2,Py2);

	theta1P1_P2 = linspace(theta1_P1,theta1_P2,1);
	theta2P1_P2 = linspace(theta2_P1,theta2_P2,1);

	for i=1:length(theta2P1_P2) 
		MTH = CD_Funcion_2R(l1,l2,theta1P1_P2(i),theta2P1_P2(i));
		PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
        hold on;
		plot(MTH.t(1),MTH.t(2),'*r');
    
	end
	Pxpunto2 = Px2;
	Pypunto2 = Py2;
    hold off;
else
   % Carga la imagen
    imagen = imread('Error.png'); % Reemplaza 'ruta_a_tu_imagen.jpg' con la ruta correcta de tu imagen
    
    % Muestra la imagen en axes1
    imshow(imagen, 'Parent', handles.axes1);
end

set(hObject,'BackgroundColor',[1 0 0]);

set(hObject,'BackgroundColor',[1 0 0]);

function edit1_Callback(hObject, eventdata, handles)

function edit1_CreateFcn(hObject, eventdata, handles)

if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit2_Callback(hObject, eventdata, handles)

function edit2_CreateFcn(hObject, eventdata, handles)

if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% AREA DE TRABAJO
function pushbutton2_Callback(hObject, eventdata, handles)
global a l1 l2 s1 s2; 

axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

theta1P1_P2 = 0;
theta2P1_P2 = linspace(0,(5/6)*pi,8);
for i=1:8
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2,theta2P1_P2(i));
    PuertoSerial((theta1P1_P2/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*r');
end

theta1P2_P3 = 0;
theta2P2_P3 = linspace((5/6)*pi,0,8);
for i=1:8
    MTH = CD_Funcion_2R(l1,l2,theta1P2_P3,theta2P2_P3(i));
    PuertoSerial((theta1P2_P3/pi)*180, (theta2P2_P3(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end

theta1P3_P4 = linspace(0,pi,8);
theta2P3_P4 = 0;
for i=1:8
    MTH = CD_Funcion_2R(l1,l2,theta1P3_P4(i),theta2P3_P4);
    PuertoSerial((theta1P3_P4(i)/pi)*180, (theta2P3_P4/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end

theta1P4_P5 = pi;
theta2P4_P5 = linspace(0,(5/6)*pi,8);
for i=1:8
    MTH = CD_Funcion_2R(l1,l2,theta1P4_P5,theta2P4_P5(i));
    PuertoSerial((theta1P4_P5/pi)*180, (theta2P4_P5(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'*');
end
set(hObject,'BackgroundColor',[1 0 0]);


% NOMBRE
function pushbutton3_Callback(hObject, eventdata, handles)
global a l1 l2 Px Py s1 s2;

axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

PuertoSerial(0,0);

palabra = get(handles.edit3,'string');

%PUNTOS INICIALES
%Punto Inicial 1
Px1 = 20;
Py1 = 0;
[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Px1,Py1);

%Punto Inicial 2
Px = -13;
Py = 11; 
[theta1_P2, theta2_P2] = CI_Funcion_2R(l1,l2,Px,Py);

theta1P1_P2 = linspace(theta1_P1,theta1_P2,10);
theta2P1_P2 = linspace(theta2_P1,theta2_P2,10);

for i=1:length(theta2P1_P2)
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2(i),theta2P1_P2(i));
    PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
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

set(hObject,'BackgroundColor',[1 0 0]);

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
    [Pxf,Pyf] = linea_vertical(3,Px1, Py1);
    Px1 = Pxf;
    Py1 = Pyf;
    [Pxf,Pyf] = linea_horizantal(3,Px1, Py1);
    Px1 = Pxf;
    Py1 = Pyf;
    [Pxf,Pyf] = linea_horizantal(-3,Px1, Py1);
    Px1 = Pxf;
    Py1 = Pyf;
    [Pxf,Pyf] = linea_vertical(-2,Px1, Py1);
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
    [Pxf,Pyf] = linea_horizantal(4,Px1, Py1);
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
    [Pxf,Pyf] = linea_diagonal(2,-2,Px1, Py1);
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


function edit3_Callback(hObject, eventdata, handles)
function edit3_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


%FUNCIONES DE LINEAS LETRAS
function [Pxf,Pyf] = linea_vertical(longitud,Px1, Py1)
global l1 l2;

%cont=0;
Pxf = Px1; 
Pyf = Py1 + longitud; 
    
Px7_Pxf = Pxf;
Py7_Pyf = linspace(Py1,Pyf,4);

for i=1:length(Py7_Pyf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf,Py7_Pyf(i));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'.r');
end

function [Pxf,Pyf] = linea_horizantal(longitud,Px1, Py1)
global l1 l2;

Pxf = Px1 + longitud; 
Pyf = Py1; 
    
Px7_Pxf = linspace(Px1,Pxf,4);
Py7_Pyf = Pyf;

for i=1:length(Px7_Pxf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf(i),Py7_Pyf);
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'.r');
end

function [Pxf,Pyf] = linea_diagonal(longitudx, longitudy,Px1, Py1)
global  l1 l2;

Pxf = Px1 + longitudx; 
Pyf = Py1 + longitudy; 
    
Px7_Pxf = linspace(Px1,Pxf,4);
Py7_Pyf = linspace(Py1,Pyf,4);

for i=1:length(Px7_Pxf)
    [theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf(i),Py7_Pyf(i));
    MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
    PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2),'.r');
end

% IMAGEN ECCI
function pushbutton4_Callback(hObject, eventdata, handles)

axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

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

% Sumando las coordenadas
for i = 1:length(contornos)
    for j = 1:length(contornos{i,1})
        contornos{i,1}(j,1) = contornos{i,1}(j,1) + 10.5; %Y
        contornos{i,1}(j,2) = contornos{i,1}(j,2) - 10; %X
    end
end

%Gragicar (Plotear)
hold on;

for i = 1:length(contornos)
    for j = 1:length(contornos{i})
%         [theta1, theta2] = CI_Funcion_2R(l1,l2,contornos{i,1}(i,2),contornos{i,1}(i,1));
%         MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
%         PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
%         plot(MTH.t(1),MTH.t(2),'.r');

        plot(contornos{i,1}(:,2), contornos{i,1}(:,1), 'b','LineWidth',2);
    end
end

hold off
set(hObject,'BackgroundColor',[1 0 0]);

% IMAGEN HYUNDAI
function pushbutton5_Callback(hObject, eventdata, handles) 

axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

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
set(hObject,'BackgroundColor',[1 0 0]);


% IMAGEN ...
function pushbutton6_Callback(hObject, eventdata, handles)
axes(handles.axes1);
cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);




set(hObject,'BackgroundColor',[1 0 0]);
