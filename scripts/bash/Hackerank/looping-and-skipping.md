#objective using bash to list odd numbers from 1-99
#Method 1 (Brace expansion)

for i in {1..99..2}
do
    echo $i
done

#Method 2 (C style)

for ((i=1; i<=99; i+=2))
do 
   echo $i
done

#Method3 (Modulo Operator)

for i in {1..99}
do 
    if [ $((i % 2)) -ne 0 ]; then
       echo $i
fi
done