function varargout = PIC_ROBOT_2R(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @PIC_ROBOT_2R_OpeningFcn, ...
                   'gui_OutputFcn',  @PIC_ROBOT_2R_OutputFcn, ...
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

function PIC_ROBOT_2R_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
guidata(hObject, handles);

clear all; %Limpiar
global l1 l2 punto2 Pxpunto2 Pypunto2;  %Variables globales

%Variables del punto 2
punto2 = 0;
Pxpunto2 = 0;
Pypunto2 = 0;
PuertoSerial(0,0);

%Eslabones
l1 = 10;
l2 = 10;

function varargout = PIC_ROBOT_2R_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;


% PUNTO 2
function pushbutton1_Callback(hObject, eventdata, handles)
global l1 l2 punto2 Pxpunto2 Pypunto2;

cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);
if punto2 == 0
    Pxpunto2 = 20;
    Pypunto2 = 0;

    punto2= punto2+1; %Solo una vez
end

[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Pxpunto2,Pypunto2);

Px2 = str2num(get(handles.edit1,'string'));
Py2 = str2num(get(handles.edit2,'string'));
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


% PUNTO 3
function pushbutton2_Callback(hObject, eventdata, handles)
global a l1 l2 s1 s2; 

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

% PUNTO 4
function pushbutton3_Callback(hObject, eventdata, handles)
global a l1 l2 s1 s2 Px Py;

cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);
%PUNTOS INICIALES
%Punto Inicial 1
Px1 = 20;
Py1 = 0;
[theta1_P1, theta2_P1] = CI_Funcion_2R(l1,l2,Px1,Py1);

%Punto Inicial 2
Px = -13;
Py = 11; 
[theta1_P2, theta2_P2] = CI_Funcion_2R(l1,l2,Px,Py);

theta1P1_P2 = linspace(theta1_P1,theta1_P2,3);
theta2P1_P2 = linspace(theta2_P1,theta2_P2,3);

for i=1:length(theta2P1_P2)
    MTH = CD_Funcion_2R(l1,l2,theta1P1_P2(i),theta2P1_P2(i));
    PuertoSerial((theta1P1_P2(i)/pi)*180, (theta2P1_P2(i)/pi)*180);
    hold on;
    plot(MTH.t(1),MTH.t(2));
end

% Letra F
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
Px1 = Pxf;
Py1 = Pyf;

% Letra A
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
Px1 = Pxf;
Py1 = Pyf;

% Letra B
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
Px1 = Pxf;
Py1 = Pyf;

%Letra I
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
Px1 = Pxf;
Py1 = Pyf;

% Letra A
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
Px1 = Pxf;
Py1 = Pyf;

%Letra N
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

set(hObject,'BackgroundColor',[1 0 0]);

% PUNTO 5
function pushbutton4_Callback(hObject, eventdata, handles)
global a l1 l2 Px Py s1 s2;

cla %Sirve para limpiar el AXES
set(hObject,'BackgroundColor',[0 1 0]);

%writePosition(s1,0);
%writePosition(s2,0);
PuertoSerial(0,0);


palabra = get(handles.edit3,'string');
%get(handles.edit1,'string');

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


function edit3_Callback(hObject, eventdata, handles)
function edit3_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


%FUNCIONES DE LINEAS LETRAS
function [Pxf,Pyf] = linea_vertical(longitud,Px1, Py1)
global l1 l2  cont;

cont=0;
Pxf = Px1; 
Pyf = Py1 + longitud; 
    
Px7_Pxf = Pxf;
Py7_Pyf = Pyf;

[theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf,Py7_Pyf);
MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
hold on;
plot(MTH.t(1),MTH.t(2),'.r');
cont = cont+1;


function [Pxf,Pyf] = linea_horizantal(longitud,Px1, Py1)
global l1 l2 cont;
cont = 0;

Pxf = Px1 + longitud; 
Pyf = Py1; 
    
Px7_Pxf = Pxf;
Py7_Pyf = Pyf;

[theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf,Py7_Pyf);
MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
hold on;
plot(MTH.t(1),MTH.t(2),'.r');
cont = cont+1;



function [Pxf,Pyf] = linea_diagonal(longitudx, longitudy,Px1, Py1)
global  l1 l2 cont;

cont=0;
Pxf = Px1 + longitudx; 
Pyf = Py1 + longitudy; 
    
Px7_Pxf = Pxf;
Py7_Pyf = Pyf;

[theta1, theta2] = CI_Funcion_2R(l1,l2,Px7_Pxf,Py7_Pyf);
MTH = CD_Funcion_2R(l1,l2,theta1,theta2);
PuertoSerial((theta1/pi)*180, (theta2/pi)*180);
hold on;
plot(MTH.t(1),MTH.t(2),'.r');
cont = cont+1;


function PuertoSerial(angulo1, angulo2)
servo1 = angulo1
servo2 = angulo2

%Elimina la basura que queda en el puerto
oldobj = instrfind; %Encontrar un objeto Serial
if ~isempty(oldobj) %Si esta vacio el objeto
    fclose(oldobj); %Cierra el objeto
    delete(oldobj); %Elimina el objeto
end

% Crear el puerto serial (Se crea el objeto con las confguraciones del puerto serial) 
if ~exist('s','var')
    s = serial('COM2','BaudRate',9600,'DataBits',8,'Parity','None','StopBits',1);%Serial Funcion de MATLAB
end

%Apertura del puerto serial 
% strcmp comparar un string(status de s)
if strcmp(get(s,'status'),'closed')
    fopen(s);
end

%fprinf para enviar datos
%fscanf(s); %Escaneo la variable s (Se peude asignar a una variable)
 

fprintf(s,'%s','A');
%fprintf(s,'%2.f',servo1);Envia enteros
fprintf(s,'%.2f',servo1);
%fprintf(s,'%d',servo1);
fprintf(s,'%s \n','O');

fprintf(s,'%s','B');
fprintf(s,'%.2f',servo2);
%fprintf(s,'%d',servo2);
fprintf(s,'%s \n','O');

fprintf(s,'%s \n','K'); % Confirmación Total

fclose(s); 