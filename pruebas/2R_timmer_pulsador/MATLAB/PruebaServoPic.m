clc
clear all
close all 

%Elimina la basura que queda en el puerto
oldobj = instrfind; %Encontrar un objeto Serial
if ~isempty(oldobj) %Si esta vacio el objeto
    fclose(oldobj); %Cierra el objeto
    delete(oldobj); %Elimina el objeto
end

% Crear el puerto serial (Se crea el objeto con las confguraciones del puerto serial) 
if ~exist('s','var')
    s = serial('COM3','BaudRate',9600,'DataBits',8,'Parity','None','StopBits',1);%Serial Funcion de MATLAB
end

%Apertura del puerto serial 
% strcmp comparar un string(status de s)
if strcmp(get(s,'status'),'closed')
    fopen(s);
end

%fprinf para enviar datos
%fscanf(s); %Escaneo la variable s (Se peude asignar a una variable)
 
s1 = 0;
fprintf(s,'%s','A');
%fprintf(s,'%d',s1);
fprintf(s,'%.2f',s1);
fprintf(s,'%s \n','O');

s2 = 90;
fprintf(s,'%s','B');
%fprintf(s,'%d',s2);
fprintf(s,'%.2f',s2);
fprintf(s,'%s \n','O');

fprintf(s,'%s \n','K'); % Confirmación Total

fclose(s); % Cierra el puerto Serial
% Termina Pisciones Iniciales Servos
