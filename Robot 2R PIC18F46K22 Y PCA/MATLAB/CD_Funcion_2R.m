function [MTH] = CD_Funcion_2R(l1,l2,theta1,theta2)
    q1 = theta1;
    q2 = theta2;
    
    q = [q1,q2];
    
    R(1) = Link('revolute','d',0,'alpha',0,'a',l1,'offset',0);
    R(2) = Link('revolute','d',0,'alpha',0,'a',l2,'offset',0);
    Robot = SerialLink(R);
    Robot.name = 'HACKER';
    
    Robot.plot(q,'scale',1.0,'workspace',[-25 25 -15 25 -30 30]);
    %ylim([10 20]);
    zlim([-10 10]);
    %Robot.teach(q);
    MTH = Robot.fkine(q); 
end