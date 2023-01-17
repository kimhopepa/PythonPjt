

#1. 문자열 분리
str_text = "3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032"
str_list = str_text.split('|')
for str in str_list :
    print(str)
# exit()

# print(str_list)

#2. 문자열 교체

str_text = "query1 query1 query1"
result = str_text.replace("query1", "1", 1)
print(result)


str_text = "12345"
print(str_text[1:len(str_text)])

str_text = "()+/*=, "
if '_' in str_text :
    print("포함")
else :
    print("미포함")

#3. 문자열 Loop
query = "INSERT /*hanwha.convergence-PMModeLogic(IDX_PM_INSERT) 2022.12.21*/ INTO TN_CM_PM_APPR  (EQP_NO, START_DATE, END_DATE, ACTN_REASON_CONT, APPR_STATUS_CODE, REQ_DATE, REQ_USER_ID, APPR_DATE, APPR_USER_ID  , PM_START_YN, PM_END_YN, PM_EXT_NOTIFY_YN, EXT_DATE, PM_EXT_YN, MOD_DATE, MOD_USER_ID, REG_DATE, REG_USER_ID)  VALUES(:eqp_no, TO_TIMESTAMP(:start_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), TO_TIMESTAMP(:end_date, 'YYYY.MM.DD HH24:MI:SS.FF3') + 8 /24, :actn_reason_cont, :appr_status_code, TO_TIMESTAMP(:req_date, 'YYYY.MM.DD HH24:MI:SS.FF3')"
# query = "SELECT * FROM WHERE eqp_no = :eqp_no and param = :param"
bind_flag = True
bind_var = ""

bind_list = []
start_index = -1
bind_end_statement = "()+/*=, "
for i in range(len(query)) :
    s = query[i]

    #1. bind 변수에서 제외 되는 조건 -> 'xxxx'로 포함된 문자열은 제외 : ex) 'YYYY.MM.DD HH24:MI:SS.FF3'
    if s == "'" and bind_flag == True :
        bind_flag = False
    elif s == "'" and bind_flag == False :
        bind_flag = True

    #2. bind 변수 위치 찾기 - bind_var = ":" 저장
    if bind_flag == True and s == ':':
        start_index = i
        bind_var = query[start_index: i + 1]

    #3. bind 변수 문자열 추가
    if bind_var.find(':') >= 0 :

        #바인딩 변수인지 체크
        if s in bind_end_statement :
            bind_list.append(bind_var)
            bind_var = ""
        elif i == (len(query)-1):
            bind_list.append(bind_var + s)
        else :
            bind_var = query[start_index: i + 1]
            print("test - bind_var", bind_var)

print("result", bind_list)