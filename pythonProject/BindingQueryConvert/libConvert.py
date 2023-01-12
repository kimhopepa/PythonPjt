class ConvertManager:

    def __init__(self):
        print("ConvertManager.__init__()")

    def makeLiteralQuery(self, bind_query, bind_variable):
        try:
            print("ConvertManager.makeLiteralQuery() - query : " + bind_query)
            print("ConvertManager.makeLiteralQuery() - bind_variable : " + bind_variable)

            # 1. bind 변수 리스트로 변환
            bind_var_list = self.get_bind_list(bind_variable)
            print("result", type(bind_var_list), bind_var_list)

            # 2. bind query

        except Exception as e:
            print("ConvertManager.makeLiteralQuery()", e)

    def get_bind_list(self, bind_variable, split_char='|'):
        bind_var_list = []
        try:
            #1. 문자열 리스트 변환
            # 3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 -> ['3651139', '2023.01.12 14:50:56.032', '2023.01.12 14:50:56.032']
            list_temp = bind_variable.split(split_char)
            print("ConvertManager.get_bind_list() - bind_variable : " + bind_variable)

            #2. 리스트내 문자열 공백 제거
            for i in list_temp:
                i = i.strip()
                bind_var_list.append(i)

            print("ConvertManager.get_bind_list() - bind_var_list", bind_var_list)

        except Exception as e:
            print("ConvertManager.makeLiteralQuery()", e)

        return bind_var_list

    def get_bindquery_list(self, bind_query):
        #바인딩 쿼리에서 바인딩 변수를 리스트로 저장
        result_list = []
        try:
            print("ConvertManager.get_bind_var_list() - query : " + bind_query)

            for str in bind_query :

            # 1. bind 변수 리스트로 변환


            # 2. bind query

        except Exception as e:
            print("ConvertManager.get_bind_var_list()", e)

        return result_list