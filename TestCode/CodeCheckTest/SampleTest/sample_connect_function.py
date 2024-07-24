import re

# 예시 텍스트
text = """
dpConnect("test",
1);
dpSomeOtherConnect();
dpConnection();
dpAnotherConnectMethod();
dpConnectMethod(param1, param2);
dpQueryConnectSingle("cmd_update_AI", false, cfg_use_multi_instance, query, cfg_query_blocking_time);
dpConnect  (   "CB_reload"   ,  reload_dp  )  ;
"""

# 정규 표현식 패턴
pattern = r'dp\w*Connect\w*\s*\(\s*[\s\S]*?\s*\)\s*;'

# 패턴 찾기
matches = re.findall(pattern, text, re.DOTALL)  # 패턴과 일치하는 모든 문자열을 찾기

# 줄바꿈 문자 제거 후 결과 출력
cleaned_matches = [re.sub(r'\s+', ' ', match) for match in matches]

for match in cleaned_matches:
    print(match)


# 예시 텍스트
text = """
delayFunction(param1);
anotherFunction();
delay (param2) ;
delayExtra(param3, param4)  ;
"""

# 정규 표현식 패턴
pattern = r'delay\s*\(.*?\)\s*;'

# 패턴 찾기
matches = re.findall(pattern, text)

# 결과 출력
for match in matches:
    print("[delay]", match)


print("Start")

if "cod)_" ==  "code_check_callback" :
    print("Test True")
else :
    print("Test False")

list_1 = ['CB_ChangeActiveCondition', 'CB_force_cx', 'CB_semi_feedback', 'CB_mode', 'CB_blackout_condition']
for item in list_1:
    print(item)

list_2 = [[1,2],[3,4]]

for i, item in enumerate(list_2):
    print(i, item)

pattern = r'delay\s*\(.*?\)\s*;'