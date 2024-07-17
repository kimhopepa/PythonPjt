
str1 = '"A.value.PVLAST"'
str2 = '123'
print(str1)
print(str2)

def is_number(s:str) -> bool :
    if s.isdigit() :
        return True
    else :
        return False

def is_string(s:str) -> bool :
    if '"' in s :
        return True
    else :
        return False

def check_str(input_string:str) -> bool :
    if is_number(input_string) or is_string(input_string) :
        return True
    else :
        return False


print(str1 , check_str(str1))
print(str2 , check_str(str2))