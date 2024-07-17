import re


def has_try_catch_blocks(text):
    # 정규 표현식 패턴 정의
    pattern = r'\s*try\s*\{.*?\}\s*catch\s*\{.*?\}'
    pattern = r'\s*try\s*\{.*?\}\s*(//.*\s*)?catch\s*\{.*?\}'
    # 정규 표현식 컴파일
    regex = re.compile(pattern, re.DOTALL)

    # 패턴이 텍스트에 있는지 확인
    match = regex.search(text)

    return match is not None

# 테스트 텍스트
text1 = """
int a,b,c;
try {
    // 임의 코드
} 
catch {
    // 임의 코드
}
"""

text2 = """
try {
    // 임의 코드
}//
catch {
    // 임의 코드
}
"""

text3 = """
try {
    // 임의 코드
    
    
    
    
    catch {
    // 임의 코드
}
"""

text4 = """
// some code
try {
    // 임의 코드
} catch {
    // 임의 코드
}
"""

print("Text1 has try-catch blocks:", has_try_catch_blocks(text1))  # True
print("Text2 has try-catch blocks:", has_try_catch_blocks(text2))  # True
print("Text3 has try-catch blocks:", has_try_catch_blocks(text3))  # False
print("Text4 has try-catch blocks:", has_try_catch_blocks(text4))  # True