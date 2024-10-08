function [theta1,theta2] = CI_Funcion_2R(l1,l2,Px,Py)
    %Theta2
    b = sqrt(Px^2+Py^2);
    cos_theta2 = (b^2-l2^2-l1^2)/(2*l2*l1);
    sen_theta2 = sqrt(1-(cos_theta2)^2);
    theta2 = atan2(sen_theta2,cos_theta2);
    fprintf('Theta2 = %.3f \n', rad2deg(theta2));
    %Theta1
    alpha = atan2(Py,Px);
    phi = atan2((l2*sen_theta2),(l1+l2*cos_theta2));
    theta1 = alpha - phi;
    if theta1<0
        theta1 = theta1*-1;
    end
    fprintf('Theta1 = %.3f \n',rad2deg(theta1));
end