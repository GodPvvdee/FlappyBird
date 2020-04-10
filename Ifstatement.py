import random
count = 0

for i in range(10):
     guess = int(input(" 1-3 hvrtelh toogoo taana uu"))
     ran = random.randint(1,3)
     print(ran)
     if guess == ran:
         count =+1
         
     else:
         
         count = 0
     if count >1:
         print(count,"ta yllaa")
             
     
