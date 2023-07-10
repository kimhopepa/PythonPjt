class ConvertManager:

    def __init__(self):
        print("ConvertManager.__init__()")

    def makeLiteralQuery(self, bind_query, bind_variable):
        try:
            print("ConvertManager.makeLiteralQuery() - query : " + bind_query)
            print("ConvertManager.makeLiteralQuery() - bind_variable : " + bind_variable)

            # 1. bind 변수 리스트로 변환
            bind_para_list = self.get_bind_parameter_list(bind_variable)
            print("[result - bind_para_list]", type(bind_para_list), len(bind_para_list), bind_para_list)

            # 2. bind query에서 변수만 리스트로 저장
            bind_var_list = self.get_bind_var_list(bind_query)
            print("[result - bind_var_list]", type(bind_query), len(bind_query), bind_query)

            # 3. literal Query 생성
            literal_query = self.get_literal_query(bind_query, bind_var_list, bind_para_list)

            return literal_query;

        except Exception as e:
            print("ConvertManager.makeLiteralQuery() - Exception", e)

    # 바인딩 파라미터를 입력받아 리스트로 저장
    # "3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 | SS_LOGIC | APPR_A" --> 3651139, 2023.01.12 14:50:56.03, .... : 리스트로 저장
    def get_bind_parameter_list(self, bind_variable, split_char='|'):
        bind_var_list = []
        try:
            # 1. 문자열 리스트 변환
            # 3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 -> ['3651139', '2023.01.12 14:50:56.032', '2023.01.12 14:50:56.032']
            list_temp = bind_variable.split(split_char)
            print("ConvertManager.get_bind_parameter_list() - bind_variable : " + bind_variable)

            # 2. 리스트내 문자열 공백 제거
            for i in list_temp:
                i = i.strip()
                bind_var_list.append(i)

            print("ConvertManager.get_bind_parameter_list() - bind_var_list", bind_var_list)

        except Exception as e:
            print("ConvertManager.get_bind_parameter_list() - Exception", e)

        return bind_var_list

    # 바인딩 쿼리를 입력받아서 바인딩 변수를 리스트에 저장
    # SELECT * FROM WHERE eqp_no = :eqp_no and param = :param -> ":eqp_no", ":param"
    def get_bind_var_list(self, bind_query):
        # 바인딩 쿼리에서 바인딩 변수를 리스트로 저장
        result_list = []
        try:
            print("ConvertManager.get_bind_var_list() - query : " + bind_query)
            start_index = -1
            bind_end_statement = "()+/*=, \n"
            bind_flag = True
            bind_var = ""
            for i in range(len(bind_query)):
                s = bind_query[i]

                # 1. bind 변수에서 제외 되는 조건 -> 'xxxx'로 포함된 문자열은 제외 : ex) 'YYYY.MM.DD HH24:MI:SS.FF3'
                if s == "'" and bind_flag == True:
                    bind_flag = False
                elif s == "'" and bind_flag == False:
                    bind_flag = True

                # 2. bind 변수 위치 찾기 - bind_var = ":" 저장
                if bind_flag == True and s == ':':
                    start_index = i
                    bind_var = bind_query[start_index: i + 1]

                # 3. bind 변수 문자열 추가
                if bind_var.find(':') >= 0:

                    # 바인딩 변수인지 체크
                    if s in bind_end_statement:
                        result_list.append(bind_var)
                        bind_var = ""
                    elif i == (len(bind_query) - 1):
                        result_list.append(bind_var + s)
                    else:
                        bind_var = bind_query[start_index: i + 1]
                        # print("test - bind_var", bind_var)

        except Exception as e:
            print("ConvertManager.get_bind_var_list() - Exception : ", e)

        return result_list

    def get_literal_query(self, bind_query, bind_var_list, bind_para_list):
        result_literal_query = bind_query
        try:
            if len(bind_var_list) == len(bind_para_list):
                print("ConvertManager.get_literal_query()", "number of lists match")
            else:
                print("ConvertManager.get_literal_query()", "number of lists match - Error \n")
                print("bind_var_list = " + bind_var_list)
                print("bind_para_list = " + bind_para_list)

            # print("ConvertManager.get_literal_query() - query : " + bind_var_list)
            for i in range(len(bind_var_list)):
                bind_var = bind_var_list[i]
                bind_parameter = "'" + bind_para_list[i] + "'"
                result_literal_query = result_literal_query.replace(bind_var, bind_parameter, 1)
                print("ConvertManager.get_literal_query()", result_literal_query)

        except Exception as e:
            print("ConvertManager.get_literal_query() - Exception", e)

        return result_literal_query
