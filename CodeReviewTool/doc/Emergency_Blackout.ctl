//v1.0 (2024.02.22)
//ù ���� ����
//v1.01 (2024.03.07)
//- Secondary �������� Dist ���� Ȯ�� �κ� ����
//- Ma, MB ��� �� Status Ȯ�� Logic ���� (On ���½� �ٷ� ���� Step ����)

#uses "CtrlADO"			
#uses "library_standard.ctl"	//DB Connection�� �ʿ���� ���

//---------------------------------------------
// configuration path & filename  
//---------------------------------------------
string script_path;      //getPath(SCRIPTS_REL_PATH);
string config_filename = "config/config.Emergency_Blackout";

const string g_script_release_version = "v1.01";
const string g_script_release_date = "2024.03.07";
const string g_script_name = "Emergency_Blackout";
string manager_dpname ="";  //ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)

int cfg_query_blocking_time = 500;
global int g_mode, g_q_status_count, g_semi_auto_logic_skip, g_operation_thread_id = -1;
global bool g_operation = false;

//init_append_list���� ���, alarm list append �ʱ⿡ �ѹ��� �ϱ� ����
global dyn_string g_k_alarm_list, g_mamb_alarm_list;

//CB_blackout_condition���� ���, ���� ���� �� Q Status true ��� ��� üũ ����
global dyn_bool g_blackout_condition_list, g_blackout_q_status_list;

//MODE ���� ���
const int IDX_MODE_AUTO = 0; //Auto Mode
const int IDX_MODE_SEMI_AUTO = 1; //Semi Auto Mode
const int IDX_MODE_LOCK = 2; //Lock Mode

//���ǹ� ��� ������ ����ϱ� ����
const int INIT_ZERO = 0;
const int INIT_ONE = 1;

//UT �ִϸ��̼� ǥ������ ���
const int IDX_STEP_NUM_0 = 0; //��� ���
const int IDX_STEP_NUM_1 = 1; //Q�� ���� ���� Ȯ��
const int IDX_STEP_NUM_2 = 2; //������ ���� ���� Ȯ��
const int IDX_STEP_NUM_3 = 3; //Ma, Mb ����
const int IDX_STEP_NUM_11 = 11; //�κ� ����

//CB_semi_feedback, blackout_thread���� ���
const int IDX_SEMI_STATUS_NORMAL = 0; //Semi Popup Open ���� �ƴ�
const int IDX_SEMI_STATUS_POPUP = 1; //Semi Popup Open
const int IDX_SEMI_STATUS_POPUP_OK = 2; //Already Semi Popup Open

//CB_semi_feedback, blackout_thread���� ���
const int IDX_BLACKOUT_NONE = 0; //���� ���� �ƴ�
const int IDX_BLACKOUT_LOGIC = 1; //��ü ���� or �κ� ����
const int IDX_BLACKOUT_GEN_NOT_RUN = 2; //������ ������ �ȵ� ��� : �˾�

//---------------------------------------------
// config option 	
//---------------------------------------------
string cfg_all_blackout_status;
string cfg_part_blackout_status;
string cfg_part_blackout_gen_check;
string cfg_all_blackout_gen_check;
string cfg_semi_popup_check;
string cfg_semi_popup_feedback;
string cfg_before_retry_genst;
string cfg_current_retry_genst;
string cfg_not_dpexists;
string cfg_step;
string cfg_hvcbgq_delaytime_pt;
string cfg_hvcb_gen_delaytime_pt;

string cfg_blackout_mode;
string cfg_hvcbgq_delaytime;
string cfg_hvcb_gen_delaytime;
string cfg_hvcbgk_delaytime;
string cfg_cx_delaytime;
string cfg_comm_delaytime;
string cfg_mamb_delaytime;
string cfg_hvcbgk_emg;
string cfg_current_retry_genst;

string cfg_comerr_a;
string cfg_comerr_b;
string cfg_comerr_c;
string cfg_comerr_d;
string cfg_comerr_e;
string cfg_comerr_f;
string cfg_comerr_g;
string cfg_comerr_ma;
string cfg_comerr_mb;

string ScriptActive_Condition;
string blackout_dp;

string cfg_dp_type;
string cfg_pjt_id;
string cfg_dist_pjt_num;
string cfg_status_parameter;
string cfg_alarm_parameter;
string cfg_select_cx_parameter;
string cfg_operator_cx_parameter;

dyn_string cfg_q_status_dp;
dyn_string cfg_alm_27_a_dp;
dyn_string cfg_alm_27_b_dp;
dyn_string cfg_k_cx_dp;
dyn_string cfg_k_st_dp;
dyn_string cfg_gen_dp;
dyn_string cfg_mamb_cx_dp;
dyn_string cfg_mamb_st_dp;

int cfg_part_gen_count;

//*******************************************************************************
// name         : main
// argument     : 
// return value : void
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Script Main Function
//*******************************************************************************
void main(){
	try
	{
		init_lib_Commmon();	//Debug-Flag Initialize
		
		writeLog(g_script_name, "0. Script Start! Release Version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
		writeLog(g_script_name, "		          lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);
		
		manager_dpname = init_program_info(g_script_name, g_script_release_version, g_script_release_date);	//Create Script Monitoring DP
		
		//---------------------------------------------
		//1. Load config file
		//---------------------------------------------
		if (load_config() == false)
		{
			update_user_alarm(manager_dpname, "1. Initialize(Load the Config) : NG");
			exit();
		}
		else
		{
			writeLog(g_script_name, "1. Initialize(Load the Config) : OK", LV_INFO);
		}
		
		//---------------------------------------------
		//2. Apply script active conditions
		//---------------------------------------------
 		writeLog(g_script_name,"2. Apply Script Active Condition", LV_INFO);    
		
		if(dpExists(manager_dpname + ".Action.ActiveCondition"))
			dpConnect("CB_ChangeActiveCondition", manager_dpname + ".Action.ActiveCondition");
		else
			init_script_active();
				
		delay(1);
		
		init_user_alarm(manager_dpname);	//Reset user User-defined alarm to OFF
  
		//---------------------------------------------
		//3. �ʱ�ȭ Logic
        //---------------------------------------------
        if(isScriptActive == true)
        {
    		if(init_dp() == 0)
    		{
    			writeLog(g_script_name, "3. Initialize(init_dp) : OK", LV_INFO);
    		}
    		else
    		{
    			writeLog(g_script_name, "3. Initialize(init_dp) : NG", LV_ERR);
    			exit();
    		}
        }
        
		//---------------------------------------------
		//4. ���� ���� ����
		//---------------------------------------------
		if(init_blackout_condition() == 0)
		{
			writeLog(g_script_name, "4. Monitoring(init_blackout_condition) : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "4. Monitoring(init_blackout_condition) : NG", LV_ERR);
			exit();
		}
		
		//---------------------------------------------
		//5. ���� ��� Mode
		//---------------------------------------------
		if(dpConnect("CB_force_cx", false , blackout_dp + cfg_hvcbgk_emg) == 0)
		{
			writeLog(g_script_name, "5. CB_force_cx : OK", LV_INFO);
		}
		else 
		{
			writeLog(g_script_name, "5. CB_force_cx : NG", LV_ERR);
			exit();
		}
		
		//---------------------------------------------
		//6. UI - SemiAuto ����
		//---------------------------------------------
		if(dpConnect("CB_semi_feedback", false , blackout_dp + cfg_semi_popup_feedback) == 0)
		{
			writeLog(g_script_name, "6. CB_semi_feedback : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "6. CB_semi_feedback : NG", LV_ERR);
			exit();
		}
		
		//---------------------------------------------
		//7. ��� ����
        //---------------------------------------------
		if(dpConnect("CB_mode", blackout_dp + cfg_blackout_mode) == 0)
		{
			writeLog(g_script_name, "7. CB_mode : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "7. CB_mode : NG", LV_ERR);
			exit();
		}
		
        //---------------------------------------------
		//7. ��� ����
        //---------------------------------------------
        int thread_id = startThread("lock_mode_check_thread");
        
        if(thread_id >= 0)
		{
			writeLog(g_script_name, "lock_mode_check_thread() : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "lock_mode_check_thread() : NG", LV_ERR);
            exit();
		}        

        writeLog(g_script_name,"===== Script initalize Complete =====", LV_INFO);
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of main(). Error = " + getLastException());
	}
	
}

//*******************************************************************************
// name         : lock_mode_check_thread
// argument     : 
// return value : 
// date         : 2024-02-20
// developed by : hanwha-convergence
// brief        : Lock Mode �϶�, dpexists check ��� Ȯ���ϱ� ���� Thread
//*******************************************************************************
void lock_mode_check_thread()
{
    while(true)
	{
		try
		{
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
//*******************************************************************************
// name         : blackout_thread
// argument     : userData(User-defined data), Reload DP
// return value : ���� ���� �ƴ� ���� (0), ���� ���� Logic ���� (1), Popup ���� (2)
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : ���� Logic ��ü Thread
//*******************************************************************************
void blackout_thread()
{
    dyn_int step_list;
	dyn_string k_cx_on_list, k_false_list;
	
	writeLog(g_script_name, "blackout_thread() - Start", LV_INFO);
	
	while(true)
	{
		try
		{
			update_heartbeat(manager_dpname); //Script Monitoring and Control
            
            //Logic ���ۿ� ����ϴ� Tag�� ���� dpExists Ȯ��
			if(dpexists_check() == 0)
            {
            	writeLog(g_script_name, "blackout_thread() - dpexists_check() = OK", LV_DBG1);
            }
            else
            {
            	writeLog(g_script_name, "blackout_thread() - dpexists_check() = NG", LV_ERR);
            }
			            
			//1. Mode Ȯ��
			if(g_mode == IDX_MODE_AUTO)
			{
				writeLog(g_script_name, "blackout_thread() - Mode Check. Mode = Auto Mode", LV_DBG1);
			}
            else if(g_mode == IDX_MODE_SEMI_AUTO)
			{
				writeLog(g_script_name, "blackout_thread() - Mode Check. Mode = Semi Auto Mode", LV_DBG1);
			}
			else
			{
                g_operation_thread_id = -1;
				writeLog(g_script_name, "blackout_thread() - Mode Check. Mode = Lock Mode", LV_INFO);
                
				delay(1);
				break;
			}
			
  			//2. ���� ���� Logic üũ
  			if(g_semi_auto_logic_skip == IDX_SEMI_STATUS_NORMAL)
  			{
  				//���� ���� Ȯ��(�κ� or ��ü) + ������ ���� Ȯ��(��ü or �κп� ����)
  				//IDX_BLACKOUT_NONE -> ���� ���� �ƴ�
  				//IDX_BLACKOUT_LOGIC -> ��ü ���� or �κ� ����
  				//IDX_BLACKOUT_GEN_NOT_RUN -> ������ ������ �ȵ� ��� : �˾�	
 				int status_condition = black_status_condition(k_cx_on_list);
				
  				if(status_condition == IDX_BLACKOUT_NONE)
  				{
  					writeLog(g_script_name, "blackout_thread() - Condition Check. Status Condition = IDX_BLACKOUT_NONE", LV_DBG2);
                    
  					delay(1);
  					continue;
  				}
  				else if(status_condition == IDX_BLACKOUT_GEN_NOT_RUN)
  				{
  					if(dynlen(k_cx_on_list) == 0)
  					{
  						//��ü ����, ������ ���� ���� 5�� �̸� Popup Open
  						if(isScriptActive == true)
  						{
  					  	    if(dpSetWait(blackout_dp + cfg_all_blackout_gen_check, true,
  						                 blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK,
  							             blackout_dp + cfg_before_retry_genst, INIT_ZERO) == 0)
                            {
                    		    writeLog(g_script_name, "blackout_thread() - All Blackout Gen Status Popup Open, Logic Stop dpSetWait: OK", LV_INFO);
                    		}
                            else
                    		{
                    			writeLog(g_script_name, "blackout_thread() - All Blackout Gen Status Popup Open, Logic Stop dpSetWait: NG", LV_ERR);
                    		}
  						}
                        
  						delay(0,100); //Delay�� ������ Lock Mode�� �ʰ� ��ȯ ��.
  					}
  					else
  					{
  						//�κ� ����, ������ ���� ���� 4�� �̸� Popup Open
  						if(isScriptActive == true)
  						{
  					  	    if(dpSetWait(blackout_dp + cfg_part_blackout_gen_check, true,
  					  	                 blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK,
  						  	             blackout_dp + cfg_before_retry_genst, INIT_ZERO) == 0)
                            {
                    		    writeLog(g_script_name, "blackout_thread() - Part Blackout Gen Status Popup Open, Logic Stop dpSetWait: OK", LV_INFO);
                    		}
                            else
                    		{
                    			writeLog(g_script_name, "blackout_thread() - Part Blackout Gen Status Popup Open, Logic Stop dpSetWait: NG", LV_ERR);
                    		}
  						}
                        
  						delay(0,100); //Delay�� ������ Lock Mode�� �ʰ� ��ȯ ��.
  					}
  					writeLog(g_script_name, "blackout_thread() - Condition Check. Status Condition = IDX_BLACKOUT_GEN_NOT_RUN", LV_INFO);
  					continue;
  				}
  				else if(status_condition == IDX_BLACKOUT_LOGIC)
  				{
  					writeLog(g_script_name, "blackout_thread() - Condition Check. Status Condition = IDX_BLACKOUT_LOGIC", LV_INFO);
  				}
                else
                {
  					writeLog(g_script_name, "blackout_thread() - Condition Check. Not Status Condition", LV_INFO);
                }
  			}

  			//3. SEMI_AUTO ����
  			if(g_mode == IDX_MODE_AUTO || g_semi_auto_logic_skip == IDX_SEMI_STATUS_POPUP_OK)
  			{
  				g_semi_auto_logic_skip = IDX_SEMI_STATUS_NORMAL;
  				writeLog(g_script_name, "blackout_thread() - IDX_SEMI_STATUS_NORMAL", LV_INFO);
  			}
  			else if(g_mode == IDX_MODE_SEMI_AUTO)
  			{
  				if(g_semi_auto_logic_skip == IDX_SEMI_STATUS_NORMAL)
  				{
  					g_semi_auto_logic_skip = IDX_SEMI_STATUS_POPUP;
					if(isScriptActive == true)
					{
						if(dpSetWait(blackout_dp + cfg_semi_popup_check, true) == 0) //Semi Popup Open
                        {
                    		writeLog(g_script_name, "blackout_thread() - Semi Popup Open dpSetWait: OK", LV_INFO);
                    	}
                        else
                    	{
                    		writeLog(g_script_name, "blackout_thread() - Semi Popup Open dpSetWait: NG", LV_ERR);
                    	}
					}
  					continue;
  				}
  				else
  				{
  					//IDX_SEMI_STATUS_POPUP �����϶�
  					writeLog(g_script_name, "blackout_thread() - Already Semi Popup Open", LV_INFO);
                    
  					delay(1);
  					continue;
  				}

  				delay(1);
  				continue;
  			}
  			else
  			{
  				writeLog(g_script_name, "blackout_thread() - Not Semi Mode", LV_INFO);
                
  				delay(1);
  				continue;
  			}
   
  			//4. Logic Start
  			//��ü ����
  			if(dynlen(k_cx_on_list) == 0)
  			{
  			 	if(get_k_off(k_false_list, step_list) == 0)     //1. K�� Off ��� ��ȸ
                {          
				    writeLog(g_script_name, "blackout_thread() - All Blackout get_k_off() = OK", LV_INFO);
                }
                else
                {
    				writeLog(g_script_name, "blackout_thread() - All Blackout get_k_off() = NG", LV_ERR);
                }
                
                if(cx_change(k_false_list, true, step_list) == 0) //2. K�� Off ��� ���(true = all_blackout)
                {          
				    writeLog(g_script_name, "blackout_thread() - All Blackout cx_change() = OK", LV_INFO);
					  
					if(cx_check(k_false_list, true, step_list) == 0)  //3. K�� Off ��� ��� Ȯ��
					{          
						writeLog(g_script_name, "blackout_thread() - All Blackout cx_check() = OK", LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "blackout_thread() - All Blackout cx_check() = NG", LV_ERR);
					}
                }
                else
                {
    				writeLog(g_script_name, "blackout_thread() - All Blackout cx_change() = NG", LV_ERR);
                }
              
  			}
  			//�κ� ����
  			else
  			{
				if(get_q_on(k_cx_on_list, step_list) == 0)       //1. Q�� On ��� Index ��ȸ
                {          
				    writeLog(g_script_name, "blackout_thread() - Part Blackout get_q_on() = OK", LV_INFO);
                }
                else
                {
    				writeLog(g_script_name, "blackout_thread() - Part Blackout get_q_on() = NG", LV_ERR);
                }
                
  				if(cx_change(k_cx_on_list, false) == 0)          //2. K�� Off ��� ���(false = part_blackout)
                {          
				    writeLog(g_script_name, "blackout_thread() - Part Blackout cx_change() = OK", LV_INFO);
					                
					if(cx_check(k_cx_on_list, false, step_list) == 0)//3. K�� Off ��� ��� Ȯ��
					{          
						writeLog(g_script_name, "blackout_thread() - Part Blackout cx_check() = OK", LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "blackout_thread() - Part Blackout cx_check() = NG", LV_ERR);
					}
                }
                else
                {
    				writeLog(g_script_name, "blackout_thread() - Part Blackout cx_change() = NG", LV_ERR);
                }

			}
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of blackout_thread(). Error = " + getLastException());
		}
		delay_cycle(1);
	}
}


//*******************************************************************************
// name         : black_status_condition
// argument     : userData(User-defined data), Reload DP
// return value : ���� ���� �ƴ� ���� (0), ���� ���� Logic ���� (1), Popup ���� (2)
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Relaod DP monitoring
//*******************************************************************************
int black_status_condition(dyn_string& k_cx_on_list)
{
	int result = 0, q_delaytime, gen_delay_time, current_count = -1, check_count;
    
	try
	{
		int gen_count = dynlen(cfg_gen_dp);  // ������ ����
        
		if(dpGet(blackout_dp + cfg_hvcbgq_delaytime, q_delaytime,
                     blackout_dp + cfg_hvcb_gen_delaytime, gen_delay_time,
                     blackout_dp + cfg_current_retry_genst, check_count) == 0)
        {
    		writeLog(g_script_name, "black_status_condition() - Q, Gen Delaytime, Check Count dpGet: OK", LV_DBG2);
    	}
        else
    	{
    		writeLog(g_script_name, "black_status_condition() - Q, Gen Delaytime, Check Count dpGet: NG", LV_ERR);
            
            return -1;
    	}
		
		//1. ���� ���� Ȯ��
		//�κ��� ��쿡�� k_cx_on_list �����
		int black_count = blackout_check(q_delaytime, k_cx_on_list);
			
	    if(black_count == 0)
		{
		    //���� ���� �ƴ�
			writeLog(g_script_name, "black_status_condition() - black_count(zero) = " + black_count, LV_DBG2);		
				
			if(isScriptActive == true)
			{
				if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_0,
				             blackout_dp + cfg_before_retry_genst, INIT_ZERO) == 0)
                {
    		        writeLog(g_script_name, "[STEP0] black_status_condition() - Step has changed. -> Step0 : OK", LV_DBG2);
        		} 
                else
        		{
        			writeLog(g_script_name, "[STEP0] black_status_condition() - Step has changed. -> Step0 : NG", LV_ERR);
                    
                    return -1;
        		}
			}
            
			return IDX_BLACKOUT_NONE;
		}
			
        g_q_status_count = dynCount(g_blackout_q_status_list, true);
        
		for(int i = 0; i <= check_count ; i++)
		{
            // ������ ���� Ȯ�� ��õ� Ƚ��
			current_count = current_count + 1;
            
			if(isScriptActive == true)
			{
    			if(dpSetWait(blackout_dp + cfg_before_retry_genst, current_count) == 0)
                {
    		        writeLog(g_script_name, "black_status_condition() - Current Count dpSetWait: OK", LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "black_status_condition() - Current Count dpSetWait: NG", LV_ERR);
                    
                    return -1;
        		}
			}
            
			//2. ������ �������� Ȯ��
			int gen_status_count = check_gen_status(gen_delay_time, k_cx_on_list);
            
			//3. �������� & ������ ��������
			//3-1. ��ü �������� && ������ �������°� Max ���
            if(g_q_status_count == dynlen(g_blackout_condition_list) && gen_status_count == gen_count)
			{
				writeLog(g_script_name, "black_status_condition() - All Blackout Condition: OK", LV_INFO);
                
				return IDX_BLACKOUT_LOGIC;
				break;
			}
			//3-2. �κ� ��� && ������ �������°� Max -1 ���
			else if(dynlen(g_blackout_condition_list) > g_q_status_count > 0 && gen_status_count >= cfg_part_gen_count)
			{
				writeLog(g_script_name, "black_status_condition() - Part Blackout Condition: OK", LV_INFO);
                
				return IDX_BLACKOUT_LOGIC;
				break;
			}
			else
			{
				if(current_count == check_count)
				{
					//������ POPUP OPEN
					writeLog(g_script_name, "black_status_condition() - Current Count = Check Count", LV_INFO);
                    
					return IDX_BLACKOUT_GEN_NOT_RUN;
				}
				else if(current_count < check_count)
				{
					writeLog(g_script_name, "black_status_condition() - Current_count < Check Count", LV_DBG2);
				}
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of black_status_condition(). Error = " + getLastException());
        
		result = -1;
	}
	
	return result;
}

//*******************************************************************************
// name         : blackout_check
// argument     :
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : �κ� ���� �϶�, Q�� true�� ��� k_cx_on_list�� ����
//*******************************************************************************
int blackout_check(int delay_time, dyn_string& k_cx_on_list)
{
	int blackout_count, q_delaytime_cnt, step_val, blackout_status_count;
	bool step_flag = false;
    
	try
	{
		dynClear(k_cx_on_list);
		
		for(int i = 1; i <= delay_time ; i++)
		{
			blackout_count = 0;
            blackout_status_count = 0;
			
			
            if(dpGet(blackout_dp + cfg_step, step_val) == 0)
            {
    		    writeLog(g_script_name, "blackout_check() - Current Step Status dpGet: OK", LV_DBG2);
    		}
            else
    		{
    			writeLog(g_script_name, "blackout_check() - Current Step Status dpGet: NG", LV_ERR);
                
                return -1;
    		}
            
            if(step_val == INIT_ZERO)
            {
                for(int k = 1; k <= dynlen(g_blackout_condition_list); k++)
              	{
              		if(g_blackout_condition_list[k] == true)
                       blackout_status_count = blackout_status_count + 1;
      			}  
                
                //���� ���� �ƴ� ��
      			if(blackout_status_count == 0)
      			{
      				writeLog(g_script_name, "blackout_check() - Blackout Status Count(zero) = " + blackout_count, LV_DBG2);
                    
      				return blackout_count;
      			}
            }
            
			for(int j = 1; j <= dynlen(g_blackout_q_status_list); j++)
			{
    			if(g_blackout_q_status_list[j] == true)
    			    blackout_count = blackout_count + 1;
			}
			
			//���� ���� ���� Ȯ��
			if(blackout_count == 0)
			{
				writeLog(g_script_name, "blackout_check() Blackout Count(zero) = " + blackout_count, LV_DBG2);
                
				return blackout_count;
			}
			else if(step_flag == false)
			{
				if(isScriptActive == true)
				{
					if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_1) == 0)
					{
						writeLog(g_script_name, "blackout_check() - Step has changed. -> Step1 : OK ", LV_INFO);
						step_flag = true;
					}
					else
					{
						writeLog(g_script_name, "blackout_check() - Step has changed. -> Step1 : NG ", LV_ERR);
                        
                        return -1;
					}
				}
			}
			
			//��ü ���� ���� Ȯ��
			if(blackout_count == dynlen(g_blackout_condition_list))
			{
				writeLog(g_script_name, "blackout_check() - Blackout Count(MAX) = " + blackout_count, LV_DBG2);
                
				return blackout_count;
			}
			else
			{
				writeLog(g_script_name, "blackout_check() - Blackout Count = " + blackout_count, LV_DBG2);
			}
			
			q_delaytime_cnt = delay_time - i;
			
			//STEP1 : Q�� ���� ���� Ȯ�� Count ������Ʈ
			if(isScriptActive == true)
			{
				if(dpSetWait(blackout_dp + cfg_hvcbgq_delaytime_pt, q_delaytime_cnt) == 0)
                {
            	    writeLog(g_script_name, "[STEP1] blackout_check() - Q Delaytime Cnt dpSetWait: OK, q_delaytime_cnt = " + q_delaytime_cnt, LV_INFO);
                }
                else
                {
                	writeLog(g_script_name, "[STEP1] blackout_check() - Q Delaytime Cnt dpSetWait: NG, q_delaytime_cnt = " + q_delaytime_cnt, LV_ERR);
                    
                    return -1;
                }
			}
            
			delay(1);
		}
		
		//Part Q�� ��� �̸� ����
		for(int i = 1 ; i <= dynlen(g_blackout_q_status_list); i++)
		{
			if(g_blackout_q_status_list[i] == true)
			{
				dynAppend(k_cx_on_list, cfg_k_cx_dp[i]);
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of blackout_check(). Error = " + getLastException());
	}
	
	return blackout_count;
}

//*******************************************************************************
// name         : check_gen_status
// argument     :
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Delaytime ���� �������� ������ ���� Check
//*******************************************************************************
int check_gen_status(int delay_time, dyn_string& k_cx_on_list)
{
	int gen_status_count, g_delaytime_cnt, g_delaytime;
	dyn_int dyn_gen_value;
    dyn_string gen_status_dp;
 
	try
	{
        if(isScriptActive == true)
        {
            if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_2) == 0)
            {
                writeLog(g_script_name, "check_gen_status() - Step has changed. -> Step2 : OK", LV_INFO);
            }
            else
            {
            	writeLog(g_script_name, "check_gen_status() - Step has changed. -> Step2 : NG", LV_DBG2);
            }
        }      		
            
    	//1.������ ���� ���� dpGet()
    	for(int k = 1;k <= dynlen(cfg_gen_dp); k++)
    	{
    	    dynAppend(gen_status_dp, cfg_gen_dp[k] + cfg_status_parameter); 
    	}
            
		for(int i = 1; i <= delay_time; i++)
		{
			if(dpGet(gen_status_dp, dyn_gen_value) == 0)// ������ ���� get
			{
				writeLog(g_script_name, "check_gen_status() - Gen Status dpGet: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "check_gen_status() - Gen Status dpGet: NG", LV_ERR);
			}
            
			gen_status_count = dynSum(dyn_gen_value);
			
			writeLog(g_script_name, "check_gen_status() - Gen Status Cnt:" + gen_status_count, LV_INFO);
				
			//��ü ����
			if(gen_status_count == dynlen(gen_status_dp))
			{
				writeLog(g_script_name, "check_gen_status() - Gen Status Cnt(MAX) = " + gen_status_count, LV_INFO);
				
				return gen_status_count;
			}
			//�κ� ����
			else if(dynlen(k_cx_on_list) != 0 && gen_status_count >= cfg_part_gen_count)
			{
				writeLog(g_script_name, "check_gen_status() - Part Gen Status Cnt = " + gen_status_count, LV_INFO);
					
				return gen_status_count;
			} 
			else
			{
				writeLog(g_script_name, "check_gen_status() - Etc Gen Status Cnt = " + gen_status_count, LV_INFO);
			}            
				
			g_delaytime_cnt = delay_time - i;
			
			//STEP2 : ������ ���� ���� COUNT ������Ʈ
			if(isScriptActive == true)
			{
				if(dpSetWait(blackout_dp + cfg_hvcb_gen_delaytime_pt, g_delaytime_cnt) == 0)
				{
					writeLog(g_script_name, "[STEP2] check_gen_status() - Gen Delaytime Cnt dpSetWait: OK. g_delaytime_cnt = " + g_delaytime_cnt, LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "[STEP2] check_gen_status() - Gen Delaytime Cnt dpSetWait: NG. g_delaytime_cnt = " + g_delaytime_cnt, LV_ERR);
				}
			}
					
			delay(1);
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of check_gen_status(). Error = " + getLastException());
	}
	
	return gen_status_count;
	
}

//*******************************************************************************
// name         : init_blackout_condition
// argument     : 
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : ���� ���� ����
//*******************************************************************************
int init_blackout_condition()
{
	int result = 0 ;
    
	try
	{
        //K��, MaMb Alarm List ���� �Լ� ȣ��
		if(init_append_list(g_k_alarm_list, g_mamb_alarm_list) == 0)
        {
			writeLog(g_script_name, "init_append_list() - Alarm List Append : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "init_append_list() - Alarm List Append : NG", LV_ERR);
            
            return -1;
		}
		
		for(int i = 1; i <= dynlen(cfg_q_status_dp); i++)
		{
			if(dpConnectUserData("CB_blackout_condition", i, cfg_pjt_id + cfg_q_status_dp[i] + cfg_status_parameter, 
                                                  		     cfg_pjt_id + cfg_alm_27_a_dp[i] + cfg_alarm_parameter,
                                                  		     cfg_pjt_id + cfg_alm_27_b_dp[i] + cfg_alarm_parameter) == 0)
			{
            	writeLog(g_script_name, "init_blackout_condition() - Blackout Condition List Index: OK", LV_DBG2);
			}
			else
			{
            	writeLog(g_script_name, "init_blackout_condition() - Blackout Condition List Index: NG", LV_DBG2);
                
				result = -1;
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of init_blackout_condition(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}

//*******************************************************************************
// name         : init_append_list
// argument     : 
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : K��, MaMb Alarm List ����
//*******************************************************************************
int init_append_list(dyn_string& k_alarm_list, dyn_string& mamb_alarm_list)
{ 
	int result = 0 ;
    
	try
	{
		//K�� Alarm List ����
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_a);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_b);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_c);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_d);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_e);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_f);
        dynAppend(k_alarm_list, blackout_dp + cfg_comerr_g);
		
        //MaMb Alarm List ����
		dynAppend(mamb_alarm_list, blackout_dp + cfg_comerr_ma);
        dynAppend(mamb_alarm_list, blackout_dp + cfg_comerr_mb);
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of init_append_list(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}

//*******************************************************************************
// name         : get_k_off
// argument     : 
// return value : int
// date         : 2024-01-04
// developed by : hanwha-convergence
// brief        : ��ü ���� �϶�, ������ false�� ��� k_false_list�� ����
//*******************************************************************************
int get_k_off(dyn_string& k_false_list, dyn_int& step_list)
{
    int result = 0 ;
    dyn_string k_status_dp, tmp_dp;
    dyn_bool k_status_value;
    
	try
	{
		dynClear(k_false_list);
		dynClear(step_list);
  
        for(int i = 1; i <= dynlen(cfg_k_st_dp); i++)
        {
            dynAppend(k_status_dp, cfg_k_st_dp[i] + cfg_status_parameter); 
        }
  
        if(dpGet(k_status_dp, k_status_value) == 0)
        {
            writeLog(g_script_name, "get_k_off() - K Status dpGet: OK", LV_INFO);
    	}
        else
    	{
    	    writeLog(g_script_name, "get_k_off() - K Status dpGet: NG", LV_ERR);
                
			result = -1;
    	}
  
        tmp_dp = cfg_k_cx_dp;
  
        for(int j = 1; j <= dynlen(k_status_value); j++) //K�� ���� false ��� Ȯ��
	    {
	        if(k_status_value[j] == false)
		    {
    		    dynAppend(k_false_list, tmp_dp[j]);
		    	dynAppend(step_list, j);
		    }
	    }
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_k_off(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}

//*******************************************************************************
// name         : get_q_on
// argument     : 
// return value : int
// date         : 2024-01-04
// developed by : hanwha-convergence
// brief        : �κ� ���� �϶�, Q�� true�� ��� Index�� step_list�� ����
//*******************************************************************************
int get_q_on(dyn_string& q_true_list, dyn_int& step_list)
{
    int result = 0, q_on_step;
    dyn_string tmp_dp;
    
	try
	{
    	dynClear(step_list);
   
        //q_true_list = Q�� true ����� K�� CX Tag ������ �迭, K�� CX ��ü Tag �迭(cfg_k_cx_dp) �ҷ��ͼ� Index �������� ����
        tmp_dp = cfg_k_cx_dp;
  
        for(int i = 1; i <= dynlen(q_true_list); i++)
        {
            q_on_step = dynContains(tmp_dp,q_true_list[i]);
            dynAppend(step_list, q_on_step);
        }
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_q_on(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}

//*******************************************************************************
// name         : CB_blackout_condition
// argument     : 
// return value : 
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Q��, 27�ҽ�a, 27�ҽ�b�� ���� ���� ���� �׽� üũ (AND ����, Q�� ���� ���� ����)
//*******************************************************************************


void CB_blackout_condition(anytype index, string status_dp, bool status_value,
							              string alarm27_a_dp, bool alarm27_a_value,
						                  string alarm27_b_dp, bool alarm27_b_value)
{
	try
	{
		if(status_value == true && alarm27_a_value == true && alarm27_b_value == true)
		{
			g_blackout_condition_list[index] = true;
			writeLog(g_script_name, "CB_blackout_condition() - Blackout Condition List : true", LV_INFO);
		}
		else
		{
			g_blackout_condition_list[index] = false;
			writeLog(g_script_name, "CB_blackout_condition() - Blackout Condition List : false", LV_INFO);
		}
		g_blackout_q_status_list[index] = status_value;	//Q�� ���� ������ ����
		writeLog(g_script_name, "CB_blackout_condition() - Blackout Q Status List Save", LV_DBG2);
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of CB_blackout_condition(). Error = " + getLastException());
	}
}

//*******************************************************************************
// name         : init_dp
// argument     : 
// return value : int
// date         : 2024-01-04
// developed by : hanwha-convergence
// brief        : Control Dp ���� �� �ʱ�ȭ
//*******************************************************************************
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
		
		if(dpSetWait(blackout_dp + cfg_all_blackout_status, false, //��ü���� ���� false
			         blackout_dp + cfg_part_blackout_status, false, //�κ����� ���� false
			         blackout_dp + cfg_hvcbgk_emg, false, //������� false
			         blackout_dp + cfg_before_retry_genst, INIT_ZERO, //���� ��Ȯ�� Ƚ�� �ʱ�ȭ
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

//*******************************************************************************
// name         : dpexists_check
// argument     : 
// return value : int
// date         : 2024-03-07
// developed by : hanwha-convergence
// brief        : Logic ���ۿ� ����ϴ� Tag�� ���� dpExists Ȯ��
//*******************************************************************************
int dpexists_check(bool lock_mode = false)
{
    dyn_string dp_total, temp_dp1;
    dyn_int getsysNum; 
    int result = 0;
    bool isPriActive,isSecActive;
    
	try
	{
        // v1.01 - eventmanager status dpget
        if(dpGet("_ReduManager.EvStatus",isPriActive,
                 "_ReduManager_2.EvStatus",isSecActive) == 0)
        {
            writeLog(g_script_name, "dpexists_check().eventmanager status - EvStatus dpGet: OK", LV_INFO);
        }
    	else
		{
    		writeLog(g_script_name, "dpexists_check().eventmanager status - EvStatus dpGet: NG", LV_ERR);
					
			return -1;
		}   
        
        // v1.01 - active server dist status check
        if(isScriptActive == true)
		{
            if(isPriActive) // pri
            {
                if(dpGet("_DistManager.State.SystemNums",getsysNum) == 0)
                {
            		writeLog(g_script_name, "dpexists_check().pri dist_check - SystemNums Linked To DistManager dpGet: OK", LV_INFO);
    			}
        		else
    			{
        			writeLog(g_script_name, "dpexists_check().pri dist_check - SystemNums Linked To DistManager dpGet: NG", LV_ERR);
						
    				return -1;
    			}
            }
            else // sec
            {
                if(dpGet("_DistManager_2.State.SystemNums",getsysNum) == 0)
                {
            		writeLog(g_script_name, "dpexists_check().sec dist_check - SystemNums Linked To DistManager dpGet: OK", LV_INFO);
    			}
        		else
    			{
        			writeLog(g_script_name, "dpexists_check().sec dist_check - SystemNums Linked To DistManager dpGet: NG", LV_ERR);
						
    				return -1;
    			}                
            }
        }
       // ---------------------------------------------       

        if(isScriptActive == true)
		{        
            if(!dynContains(getsysNum,cfg_dist_pjt_num))
            {
                 writeLog(g_script_name, "dpexists_check().dist_check - Dist Server Connection Lost", LV_INFO);
             
                 result = -1;
            }
            else
            {
                 writeLog(g_script_name, "dpexists_check().dist_check - Dist Server Connection Ok", LV_DBG2);
            }
        }
       
        for(int i = 1; i <= dynlen(cfg_q_status_dp); i++)
        {
            dynAppend(temp_dp1,cfg_pjt_id + cfg_q_status_dp[i]);
            dynAppend(temp_dp1,cfg_pjt_id + cfg_alm_27_a_dp[i]);
            dynAppend(temp_dp1,cfg_pjt_id + cfg_alm_27_b_dp[i]);
        }

        dyn_string temp_dp = cfg_k_cx_dp;
        dynAppend(dp_total,temp_dp);
		
        temp_dp = cfg_k_st_dp;
        dynAppend(dp_total,temp_dp);
		
        temp_dp = cfg_gen_dp;
        dynAppend(dp_total,temp_dp);
		
        temp_dp = cfg_mamb_cx_dp;
        dynAppend(dp_total,temp_dp);
		
        temp_dp = cfg_mamb_st_dp;
        dynAppend(dp_total,temp_dp);
		
        temp_dp = temp_dp1;
        dynAppend(dp_total,temp_dp);

		for(int i = 1 ; i <= dynlen(dp_total) ; i++)
		{
			if(dpExists(dp_total[i]) == false)
			{
		        writeLog(g_script_name, "dpexists_check() - Not dpExists = " + dp_total[i], LV_INFO);
				result = -1;
			}
			else
			{
		        writeLog(g_script_name, "dpexists_check() - dpExists = " + dp_total[i], LV_DBG2);
			}
		}
		
		if(result == -1)
		{
			//Lock ��� ���� ���� : set_lock_mode = 1�� ��쿡�� ����
			if(lock_mode == false)
			{
				if(isScriptActive == true)
				{
					if(dpSetWait(blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK, //Lock Mode ��ȯ
								 blackout_dp + cfg_not_dpexists, true) == 0) //Logic�� ���Ǵ� Tag�� �ϳ��� ������ ������ Popup ���
					{
						writeLog(g_script_name, "dpexists_check() - Lock Mode, Not Dpexists Popup Bit dpSetWait: OK", LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "dpexists_check() - Lock Mode, Not Dpexists Popup Bit dpSetWait: NG", LV_ERR);
						
						return -1;
					}
				}
			}
			else
			{
				//Lock ����� ��� �˾� ���� Ȯ�� �Ͽ� ���
				int dpexists_status;
				if(dpGet(blackout_dp + cfg_not_dpexists, dpexists_status) == 0)
				{
					writeLog(g_script_name, "dpexists_check() - Not Dpexists Popup Bit dpGet: OK", LV_INFO);
					
					if(dpexists_status == false)
					{
						if(dpSetWait( blackout_dp + cfg_not_dpexists, true) == 0) //Logic�� ���Ǵ� Tag�� �ϳ��� ������ ������ Popup ���
						{
							writeLog(g_script_name, "dpexists_check() - Not Dpexists Popup Bit dpSetWait: OK", LV_INFO);
						}
						else
						{
							writeLog(g_script_name, "dpexists_check() - Not Dpexists Popup Bit dpSetWait: NG", LV_ERR);
							
							return -1;
						}
					}
				}
				else
				{
					writeLog(g_script_name, "dpexists_check() - Not Dpexists Popup Bit dpGet: NG", LV_ERR);
					return -1;
				}
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of dpexists_check(). Error = " + getLastException());
        
		result = -1;
	}
    
	return result;
}
//*******************************************************************************
// name         : cx_change
// argument     :
// return value : int
// date         : 2024-03-07
// developed by : hanwha-convergence
// brief        : MaMb ���Ժ��� K�� ��� On/Off ���� �Լ�
//*******************************************************************************
int cx_change(dyn_string k_false_list, bool all_blackout, dyn_int step_list = makeDynInt())
{
	int result = 0, mamb_delay_time, off_delay_time, k_delay_time;
    dyn_bool dyn_mamb_status_value;
    string mamb_status_dp;
	dyn_string dp_list, mamb_dp_list;
 
	try
	{
	    if(dpGet(blackout_dp + cfg_mamb_delaytime, mamb_delay_time,
                 blackout_dp + cfg_cx_delaytime, off_delay_time,
                 blackout_dp + cfg_hvcbgk_delaytime, k_delay_time) == 0)
        {
	        writeLog(g_script_name, "cx_change() - Delaytime dpGet: OK", LV_INFO);
	    }
        else
		{
			writeLog(g_script_name, "cx_change() - Delaytime dpGet: NG", LV_ERR);
            
            return -1;
		}
            
        //�̹� Logic ������
		if(g_operation == true)
		{
			writeLog(g_script_name,"cx_change() - Logic Operation." , LV_INFO);
            
			return -1;
		}
		else		
		{
			g_operation = true;
			writeLog(g_script_name,"cx_change() - Circuit breaker input logic has been Started." , LV_INFO);
		}

		
		//Logic Start Bit true 	���� Ȯ�� �ʿ�
		// ��ü ���� Logic
		if(all_blackout == true)
		{
			if(dpSetWait(blackout_dp + cfg_all_blackout_status, true) == 0)
			{
				writeLog(g_script_name, "cx_change() - All Blackout Logic Status Bit true dpSetWait: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "cx_change() - All Blackout Logic Status Bit true dpSetWait: NG", LV_ERR);
                
                return -1;
			}  
		}
		// �κ� ���� Logic
		else
		{
			if(dpSetWait(blackout_dp + cfg_part_blackout_status, true) == 0)
			{
				writeLog(g_script_name, "cx_change() - Part Blackout Logic Status Bit true dpSetWait: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "cx_change() - Part Blackout Logic Status Bit true dpSetWait: NG", LV_ERR);
                
                return -1;
			}
		}
	
		//STEP3 : MA, MB ���		
		for(int i = 1 ; i <= dynlen(cfg_mamb_cx_dp); i++)
		{
			dynAppend(mamb_dp_list,cfg_mamb_cx_dp[i]);
		}

		if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_3) == 0)
		{
			writeLog(g_script_name, "[STEP3] cx_change() - Step has changed. -> Step3 : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "[STEP3] cx_change() - Step has changed. -> Step3 : NG", LV_ERR);
            
            return -1;
		}
		writeLog(g_script_name,"[STEP3] cx_change() - Ma, Mb CX On" , LV_INFO);
		
		int thread_id = startThread("cx_thread", mamb_dp_list, off_delay_time);
        
        if(thread_id >= 0)
		{
			writeLog(g_script_name, "[STEP3] cx_change() - Ma, Mb Insert CX On/Off : OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "[STEP3] cx_change() - Ma, Mb Insert CX On/Off : NG", LV_ERR);
			
            return -1;
		}
	        
        // v1.01 - mamb dp ����
        dyn_string ma_mb_status_list;
    	for(int k = 1 ; k <= dynlen(cfg_mamb_st_dp); k++)
    	{
    		mamb_status_dp = cfg_mamb_st_dp[k] + cfg_status_parameter;
			dynAppend(ma_mb_status_list, mamb_status_dp);
		}

        // v1.01 - mamb delayTime flag bit �߰�
		bool ma_mb_status_check = false;        
        
        // v1.01 - mamb delayTime �߰�
    	for(int i = 1 ; i <= mamb_delay_time; i++)
        {
    		//Ma,Mb ���� ���� Ȯ��
			if(dpGet(ma_mb_status_list, dyn_mamb_status_value) == 0)
			{
				writeLog(g_script_name, "[STEP3] cx_change() - Ma, Mb Status dpGet: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "[STEP3] cx_change() - Ma, Mb Status dpGet: NG", LV_ERR);

				return -1;
			}
        
    		//Ma,Mb ���°� 1�� �̻� true�̸� �̾ Logic ����
    		if(dynCount(dyn_mamb_status_value, true) >= INIT_ONE) // v1.01 - ���� true �� ��� ���� step ����
    		{
    			writeLog(g_script_name,"[STEP3] cx_change() - Ma Or Mb More Than One Alive : ", LV_INFO);
                ma_mb_status_check = true;
                break;
    		}
            
			delay(1);
			writeLog(g_script_name,"[STEP3] cx_change() - MaMb Check Delay Time Wait : " + i , LV_INFO); // v1.01 - delayTime ��� �ð� �߰�
        } 

        // v1.01 - Ma,Mb status Ȯ�� �� �˶� �߻�
        for(int j = 1 ; j <= dynlen(cfg_mamb_st_dp); j++)
        {
			if(!dyn_mamb_status_value[j])
			{
				if(dpSetWait(g_mamb_alarm_list[j], true) == 0)
				{
					writeLog(g_script_name, "[STEP3] cx_change() - MaMb Comm Error Alarm On OK : " + g_mamb_alarm_list[j], LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "[STEP3] cx_change() - MaMb Comm Error Alarm On NG : " + g_mamb_alarm_list[j], LV_ERR);
                    
                    return -1;
				}
			}
			else
			{
				writeLog(g_script_name,"[STEP3] cx_change() - Ma & Mb Status Check OK : " + mamb_status_dp, LV_INFO);
			}
		}
 
        // v1.01 - Ma,Mb status ��� Off ���·� ���� Lock ��� ��ȯ
        if(ma_mb_status_check == false)
        {
    		if(dpSetWait(blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK,
    					 blackout_dp + cfg_all_blackout_status, false,
    					 blackout_dp + cfg_part_blackout_status, false) == 0)
    		{
    			writeLog(g_script_name, "[STEP3] cx_change() - Ma & Mb Off, Lock Mode Change dpSetWait: OK", LV_INFO);
    			g_operation = false;
                
                return 1 ;
    		}
    		else
    		{
    			writeLog(g_script_name, "[STEP3] cx_change() - Ma & Mb Off, Lock Mode Change dpSetWait: NG", LV_ERR);
               
                return -1;
    		}
			
    	    delay(1); //Delay�� ������ StopThread�� �ʰ� ����  
        }      
        
		//STEP4~10 : ��ü ���� K�� ��� 
		if(all_blackout == true)
		{
			//���ܱ� ���� �������� ���
			for(int i = 1 ; i <= dynlen(k_false_list); i++)
			{
				int step = step_list[i];
				int log_step = step + IDX_STEP_NUM_3;
			
				dynClear(dp_list);
				dynAppend(dp_list, k_false_list[i]);

				int thread_id = startThread("cx_thread", dp_list, off_delay_time);
			
				if(thread_id >= 0)
				{
					if(dpSetWait(blackout_dp + cfg_step, step + IDX_STEP_NUM_3) == 0)
					{
						writeLog(g_script_name, "[STEP" + log_step + "] " + "cx_change() - Step has changed. -> Step" + log_step  + " : OK", LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "[STEP" + log_step + "] " + "cx_change() - Step has changed. -> Step" + log_step  + " : NG", LV_ERR);
                        
                        return -1;
					}
					writeLog(g_script_name, "[STEP" + log_step + "] " + "cx_change() - All Blackout K Insert CX On/Off : OK", LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "[STEP" + log_step + "] " + "cx_change() - All Blackout K Insert CX On/Off : NG", LV_ERR);
				
					result = -1;
				}
				
				//K�� ���� ���� �ð�
				delay(k_delay_time);
				writeLog(g_script_name,"[STEP" + log_step + "] " + "cx_change() - K On Delay Time Wait : " + k_delay_time , LV_INFO);
			}
		
		}
        //STEP11 : �κ� ���� K�� ���
		else
		{
			dynClear(dp_list);
			dp_list = k_false_list;

			int thread_id = startThread("cx_thread", dp_list, off_delay_time);

			if(thread_id >= 0)
			{
				if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_11) == 0)
				{
					writeLog(g_script_name, "[STEP11] cx_change() - Step has changed. -> Step11 : OK", LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "[STEP11] cx_change() - Step has changed. -> Step11 : NG", LV_ERR);
                    
                    return -1;
				}
				writeLog(g_script_name, "[STEP11] cx_change() - Part Blackout K Insert CX On/Off : OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "[STEP11] cx_change() - Part Blackout K Insert CX On/Off : NG", LV_ERR);
				
				result = -1;
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of cx_change(). Error = " + getLastException());
        
		result = -1;
	}
	finally
	{
		g_operation = false;
		writeLog(g_script_name,"cx_change() - Circuit breaker input logic has ended." , LV_INFO);
	}
    
	return result;
}

//*******************************************************************************
// name         : cx_thread
// argument     : 
// return value : int
// date         : 2024-01-04
// developed by : hanwha-convergence
// brief        : K�� ��� On/Off Thread
//*******************************************************************************
void cx_thread(dyn_string dp_list, int off_delay_tm)
{
	try
	{
    	//CX On ���
    	for(int i = 1; i <= dynlen(dp_list); i++)
    	{
            if(isScriptActive == true)
            {
                if(dpSetWait(dp_list[i] + cfg_select_cx_parameter, true) == 0)
                {
    		        writeLog(g_script_name, "cx_thread() - Select CX On: OK. Dp = " + dp_list[i], LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "cx_thread() - Select CX On: NG. Dp = " + dp_list[i], LV_ERR);
        		}
            }
                
            delay(0,100);
                
            if(isScriptActive == true)
            {
            	if(dpSetWait(dp_list[i] + cfg_operator_cx_parameter, true) == 0)
                {
    		        writeLog(g_script_name, "cx_thread() - Operator CX On: OK. Dp = " + dp_list[i], LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "cx_thread() - Operator CX On: NG. Dp = " + dp_list[i], LV_ERR);
        		}
            }
		}
		    
        //���� CX Off Delaytime
		delay(off_delay_tm);
        writeLog(g_script_name,"cx_thread() - CX Off Delay Time Wait : " + off_delay_tm , LV_INFO);
		
		for(int i = 1; i <= dynlen(dp_list); i++)
		{
            if(isScriptActive == true)
            {
            	if(dpSetWait(dp_list[i] + cfg_select_cx_parameter, false) == 0)
                {
    		        writeLog(g_script_name, "cx_thread() - Select CX Off: OK. Dp = " + dp_list[i], LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "cx_thread() - Select CX Off: NG. Dp = " + dp_list[i], LV_ERR);
        		}
            }
                
        	delay(0,100);
                
            if(isScriptActive == true)
            {
            	if(dpSetWait(dp_list[i] + cfg_operator_cx_parameter, false) == 0)
                {
    		        writeLog(g_script_name, "cx_thread() - Operator CX Off: OK. Dp = " + dp_list[i], LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "cx_thread() - Operator CX Off: NG. Dp = " + dp_list[i], LV_ERR);
        		}
            }
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of cx_thread(). Error = " + getLastException());
	}
}   

//*******************************************************************************
// name         : CB_semi_feedback
// argument     :
// return value : bool
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Semi Popup Open ��, ��� ���ۿ� ���� Logic ���� �Ǵ� ����
//*******************************************************************************
void CB_semi_feedback(string feedback_dp, bool feedback_value)
{
    try
	{
    	writeLog(g_script_name, "CB_semi_feedback() - Semi Popup Open Status = " + feedback_value, LV_INFO);
		
    	if(feedback_value == true)
    	{
    		g_semi_auto_logic_skip = IDX_SEMI_STATUS_POPUP_OK;
    	}
    	else
    	{
	    	g_semi_auto_logic_skip = IDX_SEMI_STATUS_NORMAL;
			
		    if(isScriptActive == true)
		    {
    	    	if(dpSetWait(blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK,//LOCK ��� ����
		    	             blackout_dp + cfg_before_retry_genst, INIT_ZERO,
		    	             blackout_dp + cfg_semi_popup_check, false) == 0) //SEMI POPUP false
                {
    	    	    writeLog(g_script_name, "CB_semi_feedback() - Lock Mode, Current Count, Semi Popup Bit Reset dpSetWait: OK", LV_INFO);
    	    	}
                else
    	    	{
    	    		writeLog(g_script_name, "CB_semi_feedback() - Lock Mode, Current Count, Semi Popup Bit Reset dpSetWait: NG", LV_ERR);  	    	
                }
	    	}
	    }
    }
    catch
	{
		update_user_alarm(manager_dpname, "Exception of CB_semi_feedback(). Error = " + getLastException());
	}
}	

//*******************************************************************************
// name         : load_config
// argument     : 
// return value : bool
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Script config information Load
//*******************************************************************************
bool load_config()
{
    bool result = true;
	string config_path;
	
	try
	{
		//load script Path
        set_config_path(getPath(SCRIPTS_REL_PATH) + config_filename);
  
		//[general] section 
		read_config("general", "Active_Condition", ScriptActive_Condition, CFG_MODE, true);
        
        //[main] section
		read_config("main", "blackout_dp", blackout_dp, CFG_MODE, true);
		read_config("main", "dp_type", cfg_dp_type, CFG_MODE, true);
		read_config("main", "Pjt_ID", cfg_pjt_id, CFG_MODE, true);
        read_config("main", "Dist_pjt_num", cfg_dist_pjt_num, CFG_MODE, true);

		read_config("main", "Q_STATUS_DP", cfg_q_status_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "ALARM_27_A", cfg_alm_27_a_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "ALARM_27_B", cfg_alm_27_b_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "K_CX_DP", cfg_k_cx_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "K_ST_DP", cfg_k_st_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "GEN_DP", cfg_gen_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "MaMb_CX_DP", cfg_mamb_cx_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "MaMb_ST_DP", cfg_mamb_st_dp, CFG_LIST_SEPARATOR_MODE, true);
		read_config("main", "STATUS_PARAMETER", cfg_status_parameter, CFG_MODE, true);
		read_config("main", "ALARM_PARAMETER", cfg_alarm_parameter, CFG_MODE, true);
		read_config("main", "SELECT_CX_PARAMETER", cfg_select_cx_parameter, CFG_MODE, true);
		read_config("main", "OPERATOR_CX_PARAMETER", cfg_operator_cx_parameter, CFG_MODE, true);
		read_config("main", "ALL_BLACKOUT_STATUS", cfg_all_blackout_status, CFG_MODE, true);
		read_config("main", "PART_BLACKOUT_STATUS", cfg_part_blackout_status, CFG_MODE, true);
		read_config("main", "PART_BLACKOUT_GEN_CHECK", cfg_part_blackout_gen_check, CFG_MODE, true);
		read_config("main", "ALL_BLACKOUT_GEN_CHECK", cfg_all_blackout_gen_check, CFG_MODE, true);
		read_config("main", "SEMI_POPUP_CHECK", cfg_semi_popup_check, CFG_MODE, true);
		read_config("main", "SEMI_POPUP_FEEDBACK", cfg_semi_popup_feedback, CFG_MODE, true);
		read_config("main", "BEFORE_RETRY_GENST", cfg_before_retry_genst, CFG_MODE, true);
		read_config("main", "CURRENT_RETRY_GENST", cfg_current_retry_genst, CFG_MODE, true);
		read_config("main", "NOT_DPEXISTS", cfg_not_dpexists, CFG_MODE, true);
		read_config("main", "STEP", cfg_step, CFG_MODE, true);
		read_config("main", "HVCBGQ_DELAYTIME_PT", cfg_hvcbgq_delaytime_pt, CFG_MODE, true);
		read_config("main", "HVCB_GEN_DELAYTIME_PT", cfg_hvcb_gen_delaytime_pt, CFG_MODE, true);
		read_config("main", "BLACKOUT_MODE", cfg_blackout_mode, CFG_MODE, true);
		read_config("main", "HVCBGQ_DELAYTIME", cfg_hvcbgq_delaytime, CFG_MODE, true);
		read_config("main", "HVCB_GEN_DELAYTIME", cfg_hvcb_gen_delaytime, CFG_MODE, true);
		read_config("main", "HVCBGK_DELAYTIME", cfg_hvcbgk_delaytime, CFG_MODE, true);
		read_config("main", "CX_DELAYTIME", cfg_cx_delaytime, CFG_MODE, true);
		read_config("main", "COMM_DELAYTIME", cfg_comm_delaytime, CFG_MODE, true);
		read_config("main", "MAMB_DELAYTIME", cfg_mamb_delaytime, CFG_MODE, true);
		read_config("main", "HVCBGK_EMG", cfg_hvcbgk_emg, CFG_MODE, true);
		read_config("main", "COMERR_A", cfg_comerr_a, CFG_MODE, true);
		read_config("main", "COMERR_B", cfg_comerr_b, CFG_MODE, true);
		read_config("main", "COMERR_C", cfg_comerr_c, CFG_MODE, true);
		read_config("main", "COMERR_D", cfg_comerr_d, CFG_MODE, true);
		read_config("main", "COMERR_E", cfg_comerr_e, CFG_MODE, true);
		read_config("main", "COMERR_F", cfg_comerr_f, CFG_MODE, true);
		read_config("main", "COMERR_G", cfg_comerr_g, CFG_MODE, true);
		read_config("main", "COMERR_MA", cfg_comerr_ma, CFG_MODE, true);
		read_config("main", "COMERR_MB", cfg_comerr_mb, CFG_MODE, true);
		read_config("main", "PART_GEN_COUNT", cfg_part_gen_count, CFG_MODE, true);
    }
	catch
	{
		update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
        
		result = false;
	}
	finally
	{
		return result;
	}
}

//*******************************************************************************
// name         : CB_mode
// argument     :
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : �׽� MODE ���� ����
//*******************************************************************************
void CB_mode(string dp, int mode_val)
{
    string log_mode;
            
	try
	{
        //Mode Log
        if(mode_val == IDX_MODE_AUTO)
        {
            log_mode = "Auto Mode";
        }
        else if(mode_val == IDX_MODE_SEMI_AUTO)
        {
            log_mode = "Semi Auto Mode";
        }
        else
        {
            log_mode = "Lock Mode";
        }
		writeLog(g_script_name, "CB_mode() - Chagned Mode : " + log_mode, LV_INFO);
        
        //Lock Mode �����϶���
		if(mode_val == IDX_MODE_LOCK)
		{
			//Thread ����
			if(g_operation_thread_id >= 0)
			{
				if(stopThread(g_operation_thread_id) == 0)
				{
                    g_operation = false;
					writeLog(g_script_name, "stopThread(blackout_thread) : OK. g_operation_thread_id = " + g_operation_thread_id, LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "stopThread(blackout_thread) : NG. g_operation_thread_id = " + g_operation_thread_id, LV_DBG2);
				}
				
				g_operation_thread_id = -1;
			}
		}
		else //Auto or Semi Auto
		{
			//Thread ȣ��
			if(g_operation_thread_id <= 0)
			{
				//---------------------------------------------
				//Main Logic Thread ȣ��
				//---------------------------------------------
				g_operation_thread_id = startThread("blackout_thread");

				if(g_operation_thread_id >= 0)
				{
					writeLog(g_script_name, "startThread(blackout_thread) : OK. g_operation_thread_id = " + g_operation_thread_id, LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "startThread(blackout_thread) : NG. g_operation_thread_id = " + g_operation_thread_id, LV_DBG2);
				}
			}
			else
			{
				writeLog(g_script_name, "CB_mode(). mode changed. g_operation_thread_id = " + g_operation_thread_id, LV_INFO);
			}
		}
        
        //����ó�� Step �߰�
        if((g_mode == IDX_MODE_AUTO && mode_val == IDX_MODE_SEMI_AUTO))
        {
		    g_mode = mode_val;
			writeLog(g_script_name, "CB_mode() - Auto -> Semi", LV_INFO);
		}
        else if((g_mode == IDX_MODE_SEMI_AUTO && mode_val == IDX_MODE_AUTO))
        {
		    g_mode = mode_val;
			writeLog(g_script_name, "CB_mode() - Semi -> Auto", LV_INFO);
		}
        else
        {
		    g_mode = mode_val;
		    if(isScriptActive == true)
		    {
			    if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_0) == 0)
                {
        		    writeLog(g_script_name, "[STEP0] CB_mode() - Step has changed. -> Step0 : OK", LV_INFO);
        		}
                else
        		{
        			writeLog(g_script_name, "[STEP0] CB_mode() - Step has changed. -> Step0 : NG", LV_ERR);
        		}   
            }
        }
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of CB_mode(). Error = " + getLastException());
	}
}

//*******************************************************************************
// name         : CB_force_cx
// argument     :
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : Lock Mode �� ���� ��� ����
//*******************************************************************************
void CB_force_cx(string dp_name, bool force_cx)
{
    dyn_string k_false_list;
    dyn_int step_list;
    
    try
	{
    	writeLog(g_script_name, "CB_force_cx() - Force CX Operation Start", LV_INFO);
        //Lock Mode �����϶���
        if(g_mode == IDX_MODE_LOCK)
    	{
    		if(force_cx)
    		{
				//1. K�� Off ��� ��ȸ
    			if(get_k_off(k_false_list, step_list) == 0)
                {          
    				writeLog(g_script_name, "CB_force_cx() - get_k_off() = OK", LV_INFO);
                }
                else
                {
    				writeLog(g_script_name, "CB_force_cx() - get_k_off() = NG", LV_ERR);
                }
            
    			//2. K�� Off ��� ��� 
				if(cx_change(k_false_list, true, step_list) == 0)
                {          
    				writeLog(g_script_name, "CB_force_cx() - cx_change() = OK", LV_INFO);
					
					//3. K�� Off ��� ��� Ȯ��
					if(cx_check(k_false_list, true, step_list) == 0)
					{
						writeLog(g_script_name, "CB_force_cx() - cx_check() = OK", LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "CB_force_cx() - cx_check() = NG", LV_ERR);
					}
                }
                else
                {
    				writeLog(g_script_name, "CB_force_cx() - cx_change() = NG", LV_ERR);
                }

 
				//4. ���� ��� �� �ʱ�ȭ (UI �ִϸ��̼�)
                if(isScriptActive == true)
                {
                    if(dpSetWait(blackout_dp + cfg_step, IDX_STEP_NUM_0,
                                 blackout_dp + cfg_hvcbgk_emg, false) == 0)
                    {          
            	        writeLog(g_script_name, "[STEP0] CB_force_cx() - Step0, Force CX Bit false dpSetWait: OK", LV_INFO);
                    }
                    else
                    {
            		    writeLog(g_script_name, "[STEP0] CB_force_cx() - Step0, Force CX Bit false dpSetWait: NG", LV_ERR);
                    }
                }
		    }
    		else
    		{
    			writeLog(g_script_name,"CB_force_cx() - Force CX Off", LV_INFO);
    		}
    	}
    }
    catch
	{
		update_user_alarm(manager_dpname, "Exception of CB_force_cx(). Error = " + getLastException());
	}
}

//*******************************************************************************
// name         : cx_check
// argument     :
// return value : int
// date         : 2024-02-13
// developed by : hanwha-convergence
// brief        : ���Ե� K�� ���ܱ� Status Ȯ��
//*******************************************************************************
int cx_check(dyn_string k_st_list, bool all_blackout, dyn_int step_list)
{
    int result = 0, dp_st_delaytm;
	bool k_status_value;
	string k_status_dp;

		if(dpGet(blackout_dp + cfg_comm_delaytime,dp_st_delaytm) == 0)
		{
			writeLog(g_script_name, "cx_check() - Comm Delaytime dpGet: OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "cx_check() - Comm Delaytime dpGet: NG", LV_ERR);
            
            return -1;
		}
		
		//K�� ���ܱ� ���� ���� Ȯ�� �ð�
		delay(dp_st_delaytm);
		writeLog(g_script_name,"cx_check() - K Check Delay Time Wait : " + dp_st_delaytm , LV_INFO);
		
		//K�� ���ܱ� ���� ���� Ȯ�� ��, �׿� ���� �˶� �߻�
		for(int i = 1; i <= dynlen(step_list); i++)
		{
			//���Ե� K�� ���ܱ� ���¸� Ȯ�� �ϱ� ���� step_list �� ���
			int index_st = step_list[i];
			k_status_dp = cfg_k_st_dp[index_st];
		
			if(dpGet(k_status_dp + cfg_status_parameter, k_status_value) == 0)
			{
				writeLog(g_script_name, "cx_check() - K Status Value dpGet: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "cx_check() - K Status Value dpGet: NG", LV_ERR);
                
                return -1;
			}

			if(!k_status_value)
			{
				if(isScriptActive == true)	
				{
					if(dpSetWait(g_k_alarm_list[index_st], true) == 0)
					{
						writeLog(g_script_name, "cx_check() - K Comm Error Alarm On OK : " + g_k_alarm_list[index_st], LV_INFO);
					}
					else
					{
						writeLog(g_script_name, "cx_check() - K Comm Error Alarm On NG : " + g_k_alarm_list[index_st], LV_ERR);
                        
                        return -1;
					}
				}
			}
			else
			{
				writeLog(g_script_name,"cx_check() - K Status Check OK : " + k_status_dp, LV_INFO);
			}
		}
	
		delay(0,100);
		dpGet("Aa", aa);
		
		//��ü ���� ����
		if(all_blackout == true)
		{
			if(isScriptActive == true)	
			{
    			if(dpSetWait(blackout_dp + cfg_all_blackout_status, false) == 0)
    			{
    				writeLog(g_script_name, "cx_check() - All Blackout Logic Status Bit false dpSetWait: OK", LV_INFO);
    			}
    			else
    			{
    				writeLog(g_script_name, "cx_check() - All Blackout Logic Status Bit false dpSetWait: NG", LV_ERR);
                    
                    return -1;
    			}  
			}
		}
		//�κ� ���� ����
		else
		{
			if(isScriptActive == true)	
			{
				if(dpSetWait(blackout_dp + cfg_part_blackout_status, false) == 0)
				{
					writeLog(g_script_name, "cx_check() - Part Blackout Logic Status Bit false dpSetWait: OK", LV_INFO);
				}
				else
				{
					writeLog(g_script_name, "cx_check() - Part Blackout Logic Status Bit false dpSetWait: NG", LV_ERR);
                    
                    return -1;
				} 
			}
		}
		
		if(isScriptActive == true)	
		{
			dpSetWait(blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK, //LOCK MODE ��ȯ
						 blackout_dp + cfg_before_retry_genst, INIT_ZERO,
						 blackout_dp + cfg_semi_popup_feedback, false)
			if(dpSetWait(blackout_dp + cfg_blackout_mode, IDX_MODE_LOCK, //LOCK MODE ��ȯ
						 blackout_dp + cfg_before_retry_genst, INIT_ZERO,
						 blackout_dp + cfg_semi_popup_feedback, false) == 0)
			{
				writeLog(g_script_name, "cx_check() - Lock Mode, Current Count, Popup Feedback Bit Reset dpSetWait: OK", LV_INFO);
			}
			else
			{
				writeLog(g_script_name, "cx_check() - Lock Mode, Current Count, Popup Feedback Bit Reset dpSetWait: NG", LV_ERR);
                
                return -1;
			}
		}

    
	return result;
}


void func_6(int a, int b)
{
	while(true)
	{
		
		try
		{
			
			if(test == true)
			{
			}
		}
		catch
		{
			
		}
		finnally
		{
			
		}
		
	}

}