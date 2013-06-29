import sys
import random
f = open('./isbn-list', 'w')
runs=input("How many numbers? ")
i=0
k=0
num=0
isbn=['0']*13
for k in range(runs):
    for i in range(13):
        f.write(str(random.randint(0,9)));
    f.write("\n")
f.close()
