def check_skip_item(input_code : str)  -> bool:
    result = False
    skip_list = ['Debug', 'dpConnect', 'writeLog', 'startThread', 'update_user_alarm', 'config', 'paCfg', 'for', 'sprintf', 'FROM', 'WHERE', 'delay', '0', '-1']

    result = any(item.lower() in input_code.lower() for item in skip_list)


    return result


def get_pos_LinText(input_code:str , index:int) -> str :
    # 주어진 인덱스를 기준으로 앞쪽 \n 찾기
    start_index = text.rfind('\n', 0, index)
    # 주어진 인덱스를 기준으로 뒤쪽 \n 찾기
    end_index = text.find('\n', index)
    if start_index == -1:
        start_index = 0  # 텍스트의 시작점
    else:
        start_index += 1  # '\n' 이후부터 시작하도록 조정

    if end_index == -1:
        end_index = len(text)  # 텍스트의 끝까지

    extract_text = text[start_index:end_index]
    return extract_text
text = ''''
ager.EvStatus",isPriActive,
"_ReduManager_2.EvStatus",isSecActive) == 0)
{
writeLog(g_script_name, "dpexists_check().eventmanager status - EvStatus dpGet: OK", LV_INFO);
}
else
{
writeLog(g_script_nam'
'''


if __name__ == '__main__':

    print(check_skip_item('DebugTN("test func1");'))
    print(check_skip_item('debugTN("test");'))
    print(get_pos_LinText(text, 10))

    print(get_pos_LinText(text, 30))
