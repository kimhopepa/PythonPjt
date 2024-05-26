import clang.cindex

# libclang.dll 파일이 포함된 디렉토리의 경로를 설정합니다.
clang.cindex.Config.set_library_path(r'C:\path\to\libclang.dll')

def traverse_ast(node, depth=0):
    print('  ' * depth + str(node.kind) + ' : ' + (node.spelling or ''))
    for child in node.get_children():
        traverse_ast(child, depth + 1)

def main():
    # Index 객체를 생성합니다.
    index = clang.cindex.Index.create()

    # 분석할 C 파일의 경로를 지정합니다.
    file_path = "example.c"

    # TranslationUnit 객체를 생성합니다.
    tu = index.parse(file_path)

    # 추상 구문 트리(AST)를 순회하며 출력합니다.
    traverse_ast(tu.cursor)

if __name__ == "__main__":
    main()