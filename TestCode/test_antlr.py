from antlr4 import *
from CLexer import CLexer
from CParser import CParser

class MyCListener(ParseTreeListener):
    def enterFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        print("Entering function:", ctx.getChild(1).getText())  # 첫 번째 자식은 함수 이름

def main():
    # 파싱할 C 파일 경로
    c_file_path = "test.c"

    # C 파일을 읽어들입니다.
    with open(c_file_path, "r") as file:
        c_code = file.read()

    # ANTLR를 사용하여 C 코드를 파싱합니다.
    input_stream = InputStream(c_code)
    lexer = CLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CParser(token_stream)
    tree = parser.compilationUnit()

    # 파서 리스너를 생성하고, 트리를 걸어가며 리스너를 통해 이벤트를 처리합니다.
    listener = MyCListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

if __name__ == '__main__':
    main()