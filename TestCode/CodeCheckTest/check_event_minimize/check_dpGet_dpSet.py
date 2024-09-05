
text = '''
		if (dpExists(cfg_alarm_ack_client))
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

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()  # 줄 끝의 공백 제거
        if prev_line_number is not None and search_string in line and search_string in lines[prev_line_number - 1]:
            consecutive_lines.append((prev_line_number, line_number))
        if search_string in line:
            prev_line_number = line_number

    return consecutive_lines


# 예제 사용법

search_string = 'target_string'
result_list = find_consecutive_lines(text, 'dpGet')
print(result_list)