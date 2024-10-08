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
end