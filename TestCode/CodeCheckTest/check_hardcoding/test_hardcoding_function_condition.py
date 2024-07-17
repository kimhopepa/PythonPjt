import re

# 테스트 문자열들
test_strings = [
    'Debug(123)',
    'writeLog("test")',
    'Thread(456)',
    'dpQueryConnectSingle("example")',
    'func(789)',
    'call(tag_name )',
    'dpConnect(100)',
    'processConnection("example")',
    'if(value > 50)'      
    'if(value < 50) || if(value ==100)'
]


def check_hardcoding_bracket(line_code:str) :
    #1. 괄호안의 비연산자 리스트로 저장
    pattern =