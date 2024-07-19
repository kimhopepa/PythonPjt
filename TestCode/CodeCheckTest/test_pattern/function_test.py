import re

pattern = r'^[^/]*\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((?:[^)(]*|\([^)]*\))*\)\s*\{'

test_code = """
int init_dp()
{
	dyn_string dp_cx;
    dyn_bool cx_sel_value, cx_oper_value;
	int result = 0;
    
	try
	{
        dyn_string tmp_dp = cfg_k_cx_dp;
        dynAppend(dp_cx,tmp_dp);
        
        tmp_dp = cfg_mamb_cx_dp;
        dynAppend(dp_cx,tmp_dp);
        
        for(int i = 1; i <= dynlen(dp_cx); i++)
        {
            if(dpGet(dp_cx[i] + cfg_select_cx_parameter,cx_sel_value[i],
                     dp_cx[i] + cfg_operator_cx_parameter,cx_oper_value[i]) == 0)
            {
        		writeLog(g_script_name, "init_dp() - K, MaMb CX dpGet : OK", LV_DBG2);
            }
            else
        	{
        		writeLog(g_script_name, "init_dp() - K, MaMb CX dpGet : NG", LV_ERR);
                    
        		result = -1;
        	}
            
            if(cx_sel_value[i] == true)
            {
                if(dpSetWait(dp_cx[i] + cfg_select_cx_parameter, false) == 0)
                {
    				writeLog(g_script_name, "Select CX Set Value Initial : OK. dp_name = " + dp_cx[i], LV_DBG2);
                }
                else
        		{
        			writeLog(g_script_name, "Select CX Set Value Initial : NG. dp_name = " + dp_cx[i], LV_ERR);
          
        			result = -1;
        		}
            }
            
            delay(0,100);
            
            if(cx_oper_value[i] == true)
            {
                if(dpSetWait(dp_cx[i] + cfg_operator_cx_parameter, false) == 0)
                {
    				writeLog(g_script_name, "Operator CX Set Value Initial : OK. dp_name = " + dp_cx[i], LV_DBG2);
                }
                else
        		{
        			writeLog(g_script_name, "Operator CX Set Value Initial : NG. dp_name = " + dp_cx[i], LV_ERR);
                       
        			result = -1;
        		}
            }
        }
        
		writeLog(g_script_name,"1. Set Value Initial", LV_INFO);
		
		if(dpSetWait(blackout_dp + cfg_all_blackout_status, false, //전체정전 상태 false
			         blackout_dp + cfg_part_blackout_status, false, //부분정전 상태 false
			         blackout_dp + cfg_hvcbgk_emg, false, //강제출력 false
			         blackout_dp + cfg_before_retry_genst, INIT_ZERO, //현재 재확인 횟수 초기화
			         blackout_dp + cfg_semi_popup_feedback, false, //SEMI POPUP FEEDBACK false
              	     blackout_dp + cfg_not_dpexists, false, //SEMI POPUP FEEDBACK false
			         blackout_dp + cfg_hvcbgq_delaytime_pt, INIT_ZERO,
			         blackout_dp + cfg_hvcb_gen_delaytime_pt, INIT_ZERO,
  			         blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK) == 0)
		{
			writeLog(g_script_name, "Set Value Initial : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "Set Value Initial : NG", LV_ERR);
                
        	result = -1;
		}
        
        if(dpexists_check() == 0)
        {          
        	writeLog(g_script_name, "init_dp() - dpexists_check() = OK", LV_INFO);
        }
        else
        {
        	writeLog(g_script_name, "init_dp() - dpexists_check() = NG", LV_ERR);
            
		    result = -1;
        }
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of init_dp(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}

void anotherFunction(int a)
{
    // Another function body
}

float computeSum(float x, float y = 0.0)
{
    return x + y;
}
"""

matches = re.findall(pattern, test_code)

for match in matches:
    print(f"Function Name: {match}")