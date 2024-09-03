import re


text = """

void lock_mode_check_thread()
{
    while(true)
	{
		try
		{
		    if( isScriptActive == true)
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
''
def finde_variable(code:str, variable:str) -> bool :
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

if __name__ == '__main__':
    print(finde_variable(text, "g_mode"))

