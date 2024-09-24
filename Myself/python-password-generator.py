import random
import string

total = string.ascii_letters + string.digits + string.punctuation
# string是函数中内置的
length = 16

password = "".join(random.sample(total, length))
password_1 = "-".join(random.choices(total, k=10))
#This choices can be selected multiple times,but samlpe not
print(password)
print(password_1)


