from random import randint

arr = []
for i in range(1000000):
    arr.append(randint(1, 1000000000))
f = open("bigdata_input.txt", 'w')
for i in range(len(arr)):
    if i == len(arr)-1:
        f.write(str(arr[i]))
    else:
        f.write(str(arr[i]) + " ")

f.close()
