from random import randint

numa=randint(1,100)
numb=randint(1,100)

if numa > numb:
    print(f'{numa} is greather than {numb}')
elif numa<numb:
    print(f'{numa} is less than {numb}')
else:
    print('The two numbers are equal')