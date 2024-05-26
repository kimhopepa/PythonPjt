import os
import tree_sitter

# 파서 로드
tree_sitter.Language.build_library(
  # 언어 소스 파일이 있는 디렉토리의 경로
  'tree-sitter-languages.so',

  # 파싱할 언어를 지정하는 언어 그램 파일의 경로
  ['tree-sitter/tree-sitter-c']
)
# C_LANGUAGE = tree_sitter.Language('tree-sitter-languages.so', 'c')
#
# # 파서 설정
# parser = tree_sitter.Parser()
# parser.set_language(C_LANGUAGE)
#
# # 파싱할 C 코드 읽기
# with open('test.c', 'r') as file:
#     code = file.read()
#
# # 코드 파싱
# tree = parser.parse(bytes(code, "utf8"))
#
# # 파싱된 AST 출력
# print(tree.root_node)