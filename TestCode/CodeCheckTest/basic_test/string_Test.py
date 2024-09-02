# str = "1111dp_name2222"
#
# str2 = 'DebugTN("test")'
#
# if 'dp_name33' in str :
#     print(True)
# else :
#     print(False)
#
#
# if 'DebugTN' in str2 :
#     print(True)
# else :
#     print(False)
#
# str = 'string manager_dpname ="";  //ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)'
# print(str.find('/'))

def string_check_function() :
    text1 = "load_config"
    function_list = ['config', 'writeLog']
    result = any(item in text1 for item in function_list)
    print("result", result)

if __name__ == '__main__':
    string_check_function()
