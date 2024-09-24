import math
import string
import random

Character = string.ascii_letters
num = string.digits
Special = string.punctuation

pass_len = int(input("please enter the password length"))

Character_len = pass_len // 2
num_len = math.ceil(pass_len * 30/100)
Special_len = pass_len-(Character_len+num_len)

password = []

def password_generate (length,array,is_alpha=False):
    for i in range(length):
        index = random.randint(0,1)
        password_tem  = random.choice(array)
        if is_alpha:
            case = random.randint(0,1)
            if case == 1 :
                password_tem = password_tem.upper()
        password.append(password_tem)

password_generate(Character_len, Character, True)
# numeric password
password_generate(num_len, num)
# special Character password
password_generate(Special_len, Special)
# suffle the generated password list
random.shuffle(password)

password_1 = "".join(password)
print(password_1)



