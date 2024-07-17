import re

# 수정된 정규 표현식
pattern = re.compile(r'\b(?!Debug\b|writeLog\b|Thread\b|\w*Connect\w*)\w+\s*\([^)]*(\d+|".*?")[^)]*\)')

# 테스트 문자열들
test_strings = [
    'Debug(123)',          # 매치되지 않아야 함
    'writeLog("test")',    # 매치되지 않아야 함
    'Thread(456)',         # 매치되지 않아야 함
    'Connect("example")',  # 매치되지 않아야 함
    'func(789)',           # 매치되어야 함
    'call("test")',        # 매치되어야 함
    'myConnectFunction(100)',  # 매치되지 않아야 함
    'processConnection("example")',  # 매치되지 않아야 함
    'if(value > 50)'       # 매치되어함
]

# 정규 표현식 테스트
for test_string in test_strings:
    match = pattern.search(test_string)
    if match:
        print(f'Matched: {test_string}')
    else:
        print(f'Not matched: {test_string}')


# 수정된 정규 표현식
pattern = re.compile(r'^\s*\w+\s*=\s*([^";]*"[^"]*"[^";]*|\d+[^";]*)\s*([\+\-\*/]\s*([^";]*"[^"]*"[^";]*|\d+[^";]*))*\s*;\s*(//.*)?$')

# 테스트 문자열들
test_strings = [
    'variable = 123;',              # 일치
    ' variable = 456 ; // comment', # 일치
    'variable = "abc";',            # 일치 (우항이 문자열도 일치)
    'variable = 789; // comment',   # 일치
    'variable = 0123;    ',         # 일치
    'a1 = b1;    ',                 # 불일치
    'a1 = b1 + "TEST";    ',        # 일치
    'a1 = "TEST" + b1 ;    ',       # 일치
    'a1 = b1 + 50 ;    ',           # 일치
    'a1 = 50 - b1 ;    ',           # 일치
]

# 정규 표현식 테스트
for test_string in test_strings:
    match = pattern.match(test_string)
    if match:
        print(f'Matched: {test_string}')
    else:
        print(f'Not matched: {test_string}')
