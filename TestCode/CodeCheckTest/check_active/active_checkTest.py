import re

text = """
void lock_mode_check_thread()
{
    while(true)
	{
		try
		{
		    if( isScriptActive222 == true)
			    writeLog(g_script_name, "lock_mode_check_thread()", LV_DBG2);
			
            if(g_mode == IDX_MODE_LOCK)
            {
                if(dpexists_check(true) == 0)
				{
					writeLog(g_script_name, "lock_mode_check_thread() - Dp Check OK", LV_DBG2);
				}
				else
				{
					writeLog(g_script_name, "lock_mode_check_thread() - Dp Check NG", LV_ERR);
				}
            }
        }
		catch
		{
			update_user_alarm(manager_dpname, "Exception of lock_mode_check_thread(). Error = " + getLastException());
		}
		
		delay_cycle(1);
	}
}
"""

def isCheckActive(text:str) -> bool :
    pattern = r'if\s*\(\s*isScriptActive\b'
    match = re.search(pattern, text)
    if not match :
        print("Actvie 설정이 되지 않습니다.")


if __name__ == '__main__':
    isCheckActive(text)