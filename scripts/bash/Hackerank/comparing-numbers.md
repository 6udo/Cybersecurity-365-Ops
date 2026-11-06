#Objective given 2 integers X and Y identify whether X > Y, X < Y or X = Y 

read X
read Y
if ((X < Y)); then
    echo "X is less than Y"
elif ((X > Y)); then
    echo "X is greater than Y"
else
    echo "X is equal to Y"
fi
