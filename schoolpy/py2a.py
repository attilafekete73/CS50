numa=int(input("Please enter a number! "))
numb=int(input("Please enter another number! "))
if numa > numb:
    print(f'{numa} is greather than {numb}')
elif numa<numb:
    print(f'{numa} is less than {numb}')
else:
    print('The two numbers are equal')