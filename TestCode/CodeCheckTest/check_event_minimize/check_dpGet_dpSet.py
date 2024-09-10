text = '''		if (dpExists(cfg_alarm_ack_client))
		{
			dpGet(cfg_alarm_ack_client, ack_client);
			dpGet(cfg_alarm_ack_username, ack_username);
			dpGet(cfg_alarm_ack_type, ackType);

			if (ack_client == "") ack_client = " ";
			if (ack_username == "") ack_username = " ";

			ackType = ackType - 1;
			dpSet(cfg_alarm_ack_type, ackType);

			if (ackType <= 0)
			{
				dpSet(cfg_alarm_ack_client, "");
				dpSet(cfg_alarm_ack_username, "");
				dpSet(cfg_alarm_ack_type, 0);
			}
		}
'''


def find_consecutive_lines(text, search_string):
    lines = text.splitlines()  # 입력된 텍스트를 줄 단위로 나누기
    consecutive_lines = []  # 연속된 문자열 위치를 저장할 리스트
    prev_line_number = None

    for line_number, line_text in enumerate(lines, start=1):
        # if prev_line_number is not None and search_string in line and search_string in lines[prev_line_number-1]:
        if prev_line_number is not None :
            if check_functions( line_text, lines[prev_line_number-1], ["dpGet", "dpSet"]) == True :
                consecutive_lines = consecutive_lines + [[line_number, line_text]]

        prev_line_number = line_number
    return consecutive_lines

# 이전, 현재 라인 코드 비교하여 체크할 문자열이 포함되어 있으면 배열 저장
def check_functions(current_text:str, prev_text:str, check_list:list) -> bool:
    result_list = []
    #1. 체크할 문자열 리스트 동작
    for check_text in check_list :
        #2. 이전 라인, 현재 라인 포함하는지 조건 확인
        if check_text in prev_text and check_text in current_text :
           return True

if __name__ == '__main__':

    # 예제 사용법

    search_string = 'target_string'
    result_list = find_consecutive_lines(text, 'dpGet')
    result_list = find_consecutive_lines(text, 'dpSet')
    check_functions("","", ["test1", "test2"] );
    print(result_list)