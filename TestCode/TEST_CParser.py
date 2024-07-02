from pycparser import c_parser, c_ast
#
# parser = c_parser.CParser()
# ast = parser.parse("""
# int main() {
#    printf("Hello, World!");
#    return 0;
# }
# """)
#
# ast.show()


# 주석을 제거하는 함수

class UnusedGlobalVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.used_variables = set()

    def visit_Decl(self, node):
        if node.init is None:
            self.variables.add(node.name)
        self.generic_visit(node)

    def visit_ID(self, node):
        self.used_variables.add(node.name)

class UnusedVariableVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.used_variables = set()

    def visit_Decl(self, node):
        if node.init is None:
            self.variables.add(node.name)
        self.generic_visit(node)

    def visit_ID(self, node):
        self.used_variables.add(node.name)

def remove_comments(code):
    lines = code.split('\n')
    cleaned_lines = []
    in_comment = False
    for line in lines:
        line = line.strip()
        if not in_comment:
            if line.startswith('/*'):
                in_comment = True
            elif '//' in line:
                line = line[:line.index('//')]
            if line:
                cleaned_lines.append(line)
        else:
            if line.endswith('*/'):
                in_comment = False
    return '\n'.join(cleaned_lines)

# C 파일 읽기
with open('test.c', 'r') as f:
    c_code = f.read()

# 주석 제거
cleaned_code = remove_comments(c_code)
# C 코드를 파싱하여 AST(Abstract Syntax Tree) 생성
parser = c_parser.CParser()
st = parser.parse(cleaned_code)


# 전역 변수 찾기
global_visitor = UnusedGlobalVisitor()
global_visitor.visit(ast)
unused_global_variables = global_visitor.variables - global_visitor.used_variables

# 미사용 변수 찾기
variable_visitor = UnusedVariableVisitor()
variable_visitor.visit(ast)
unused_variables = variable_visitor.variables - variable_visitor.used_variables
# AST 출력
# ast.show()

# class FuncDefVisitor(c_ast.NodeVisitor):
#     def visit_FuncDef(self, node):
#         print('Function name:', node.decl.name)
#         self.generic_visit(node)
#
# # C 파일 읽기
# with open('test.c', 'r') as f:
#     c_code = f.read()
#
# print(c_code)
# # C 코드를 파싱하여 AST(Abstract Syntax Tree) 생성
# parser = c_parser.CParser()
# ast = parser.parse(c_code)
#
# # FuncDefVisitor를 사용하여 함수 정의를 방문합니다.
# visitor = FuncDefVisitor()
# visitor.visit(ast)