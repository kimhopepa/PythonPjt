//v1.0(2024.06.21)
//1. first version

#uses "library_standard.ctl"

//---------------------------------------------
// configuration path & filename
//---------------------------------------------
string script_path;      //getPath(SCRIPTS_REL_PATH);
string config_filename;
const string g_script_release_version = "v1.0";
const string g_script_release_date = "2024.06.21";
const string g_script_name = "SmartIO_STS";
string manager_dpname = ""; //ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)


//---------------------------------------------
// config option
//---------------------------------------------
string ScriptActive_Condition  = "ACTIVE";  //|BOTH|HOST1|HOST2";
int loop_time;

// config parameter
string cfg_total_tag;
string cfg_status_para, cfg_27_para, cfg_rjx_para, cfg_stslamp_para, cfg_rjlamp_para, cfg_rjelamp_para, cfg_rslamp_para, cfg_testlamp_para, cfg_lrst_para, cfg_test_para;
string cfg_runtime_para, cfg_stoptime_para, cfg_runcount_para, cfg_reset_para;
dyn_string blink_list_ms_1000, blink_list_ms_100, lamptest_list;
const int SEC_60 = 60;
const int RESET_SEC_3 = 3;

const int STATUS_LAMP_OFF = 0;
const int STATUS_LAMP_BLINK = 1;
const int STATUS_LAMP_ON = 2;

const bool ON_27 = true;
const bool OFF_27 = false;

mapping g_map_cfg_info;	//key = "STS_4F1_A", value = dyn_string(STS_ECB4F11LSG_A, STS_VCB4F11GQ_A)
mapping g_map_heartbeat;
mapping g_map_rjx_values;

mapping g_map_stslamp;
mapping g_map_rjlamp;
mapping g_map_rjelamp;
mapping g_map_rslamp;
mapping g_map_masterlamp;
mapping g_map_bktime_flag;

bool reset_flag, lrst_flag, lamptest_flag;

string sysname = getSystemName();



//*******************************************************************************
// name         : main
// argument     :
// return value : void
// date         : 2020-08-12
// developed by : Ino-Group
// brief        : Script Main Function
//*******************************************************************************
void main()
{
	int result;

	try
	{
		init_lib_Commmon();	//Debug-Flag Initialize

		writeLog(g_script_name, "0. Script Start! Release Version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
		writeLog(g_script_name, "		lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);

		manager_dpname = init_program_info(g_script_name, g_script_release_version, g_script_release_date);		//Create Script Monitoring DP

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
		writeLog(g_script_name, "2. Apply Script Active Condition", LV_INFO);

		if (dpExists(manager_dpname + ".Action.ActiveCondition"))
		  dpConnect("CB_ChangeActiveCondition", manager_dpname + ".Action.ActiveCondition");
		else
		  init_script_active();

		delay(1);

		init_user_alarm(manager_dpname);	//Reset user User-defined alarm to OFF


		//---------------------------------------------
		//3. Thread Start
		//--------------------------------------------
		for(int i = 1 ; i <= mappinglen(g_map_cfg_info) ; i++)
		{
			string mapping_key = mappingGetKey(g_map_cfg_info, i); // STS_GROUP_TOTAL, STS_GROUP_1, STS_GROUP_2, ...

			// 3-1. Total 정/복전 Logic
			if(mapping_key == "STS_GROUP_TOTAL")
			{
				dyn_string mapping_list = mappingGetValue(g_map_cfg_info, i);

				// Master STS Logic
				result = startThread("master_sts_logic", mapping_list);

				if(result >= 0)
				{
					writeLog(g_script_name, "3-1. Thread Start. function = master_sts_logic, group : " + mapping_key, LV_INFO);
				}
				else
				{
					update_user_alarm(manager_dpname, "3-1. Thread Start NG. function = master_sts_logic, group : " + mapping_key);
					exit();
				}

				// Master RJ Logic
				result = startThread("master_rj_logic", mapping_list);

				if(result >= 0)
				{
					writeLog(g_script_name, "3-2. Thread Start. function = master_rj_logic, group : " + mapping_key, LV_INFO);
				}
				else
				{
					update_user_alarm(manager_dpname, "3-2. Thread Start NG. function = master_rj_logic, group : " + mapping_key);
					exit();
				}
				
				// Master RS Logic
				result = startThread("master_rs_logic", mapping_list);

				if(result >= 0)
				{
					writeLog(g_script_name, "3-3. Thread Start. function = master_rs_logic, group : " + mapping_key, LV_INFO);
				}
				else
				{
					update_user_alarm(manager_dpname, "3-3. Thread Start NG. function = master_rs_logic, group : " + mapping_key);
					exit();
				}
			}
			// 3-2. Main Logic
			else
			{
				dyn_string mapping_list = mappingGetValue(g_map_cfg_info, i);
				result = startThread("main_sts_logic", mapping_list);

				if(result >= 0)
				{
					writeLog(g_script_name, "3-4. Thread Start. function = main_sts_logic, group : " + mapping_key, LV_INFO);
				}
				else
				{
					update_user_alarm(manager_dpname, "3-4. Thread Start NG. function = main_sts_logic, group : " + mapping_key);
					exit();
				}
			}
		}

		// 4-1. Blink Logic - 1sec
		result = startThread("blink_list_ms_1000_logic");
		if(result >= 0)
		{
			writeLog(g_script_name, "4-1. Thread Start. function = blink_list_ms_1000_logic.", LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname, "4-1. Thread Start NG. function = blink_list_ms_1000_logic.");
			exit();
		}

		// 4-2. Blink Logic - 0.1sec
		result = startThread("blink_list_ms_100_logic");
		if(result >= 0)
		{
			writeLog(g_script_name, "4-2. Thread Start. function = blink_list_ms_100_logic.", LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname, "4-2. Thread Start NG. function = blink_list_ms_100_logic.");
			exit();
		}


		// g_map_heartbeat Data 추가 대기
		delay(3);
		// 4-3. Heartbeat Check Thread
		result = startThread("heartbeat_check", g_map_heartbeat);

		if(result >= 0)
		{
			writeLog(g_script_name, "4-3. Thread Start. function = heartbeat_check", LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname, "4-3. Thread Start NG. function = heartbeat_check");
			exit();
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of main(). Error = " + getLastException());
	}

}

//*******************************************************************************
// name         : load_config
// argument     :
// return value : bool
// date         : 2024-04-05
// developed by : KWH
// brief        : Script config information Load
//*******************************************************************************
bool load_config()
{
	bool is_result = true;
	string config_path;

	try
	{
		//1. load config File Name from Manager DP
		if(globalExists("global_config_name") == true)
			config_filename = global_config_name;

		//2. load script Path
		config_path = getPath(SCRIPTS_REL_PATH) + config_filename;

		writeLog(g_script_name, "load_config() - config file path = " + config_path, LV_DBG2);

		// [general] Active_Condition
		if(paCfgReadValue(config_path, "general", "Active_Condition", ScriptActive_Condition) != 0)
			writeLog(g_script_name, "[general] Active_Condition. Default value is " + ScriptActive_Condition, LV_INFO);

		// [general] LoopTime
		if(paCfgReadValue(config_path, "general", "LoopTime", loop_time) != 0)
		{
			writeLog(g_script_name, "Failed to load : [general] LoopTime.", LV_WARN);
			is_result = false;
		}

		// [main] status_para
		if(paCfgReadValue(config_path, "main", "STATUS_PARA", cfg_status_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_status_para.", LV_WARN);
			is_result = false;
		}

		// [main] 27_para
		if(paCfgReadValue(config_path, "main", "27_PARA", cfg_27_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_status_para.", LV_WARN);
			is_result = false;
		}

		// [main] rjx_para
		if(paCfgReadValue(config_path, "main", "RJX_PARA", cfg_rjx_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_rjx_para.", LV_WARN);
			is_result = false;
		}

		// [main] stslamp_para
		if(paCfgReadValue(config_path, "main", "STSLAMP_PARA", cfg_stslamp_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_stslamp_para.", LV_WARN);
			is_result = false;
		}

		// [main] rjlamp_para
		if(paCfgReadValue(config_path, "main", "RJLAMP_PARA", cfg_rjlamp_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_rjlamp_para.", LV_WARN);
			is_result = false;
		}

		// [main] rjelamp_para
		if(paCfgReadValue(config_path, "main", "RJELAMP_PARA", cfg_rjelamp_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_rjelamp_para.", LV_WARN);
			is_result = false;
		}

		// [main] rslamp_para
		if(paCfgReadValue(config_path, "main", "RSLAMP_PARA", cfg_rslamp_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_rslamp_para.", LV_WARN);
			is_result = false;
		}
		
		// [main] testlamp_para
		if(paCfgReadValue(config_path, "main", "TESTLAMP_PARA", cfg_testlamp_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_testlamp_para.", LV_WARN);
			is_result = false;
		}

		// [main] lrst_para
		if(paCfgReadValue(config_path, "main", "LRST_PARA", cfg_lrst_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_lrst_para.", LV_WARN);
			is_result = false;
		}

		// [main] test_para
		if(paCfgReadValue(config_path, "main", "TEST_PARA", cfg_test_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_test_para.", LV_WARN);
			is_result = false;
		}

		// [main] runtime_para
		if(paCfgReadValue(config_path, "main", "BKTIME_RUNTIME_PARA", cfg_runtime_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_runtime_para.", LV_WARN);
			is_result = false;
		}

		// [main] stoptime_para
		if(paCfgReadValue(config_path, "main", "BKTIME_STOPTIME_PARA", cfg_stoptime_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_stoptime_para.", LV_WARN);
			is_result = false;
		}

		// [main] runcount_para
		if(paCfgReadValue(config_path, "main", "BKTIME_RUNCOUNT_PARA", cfg_runcount_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_runcount_para.", LV_WARN);
			is_result = false;
		}

		// [main] reset_para
		if(paCfgReadValue(config_path, "main", "BKTIME_RESET_PARA", cfg_reset_para) != 0)
		{
			writeLog(g_script_name, "Failed to load : [main] cfg_reset_para.", LV_WARN);
			is_result = false;
		}

		string msg =
			"\n[general]  \n" +
			"Active_Condition = " + ScriptActive_Condition + "\n" +
			"LoopTime = " + loop_time + "\n" +
			"\n[main]  \n" +
			"cfg_status_para = " + cfg_status_para + "\n" +
			"cfg_27_para = " + cfg_27_para + "\n" +
			"cfg_rjx_para = " + cfg_rjx_para + "\n" +
			"cfg_stslamp_para = " + cfg_stslamp_para + "\n" +
			"cfg_rjlamp_para = " + cfg_rjlamp_para + "\n" +
			"cfg_rjelamp_para = " + cfg_rjelamp_para + "\n" +
			"cfg_rslamp_para = " + cfg_rslamp_para + "\n" +
			"cfg_testlamp_para = " + cfg_testlamp_para + "\n" +
			"cfg_lrst_para = " + cfg_lrst_para + "\n" +
			"cfg_test_para = " + cfg_test_para + "\n" +
			"cfg_runtime_para = " + cfg_runtime_para + "\n" +
			"cfg_stoptime_para = " + cfg_stoptime_para + "\n" +
			"cfg_runcount_para = " + cfg_runcount_para + "\n" +
			"cfg_reset_para = " + cfg_reset_para + "\n";

		// [STS_DP_XX] ~~
		string section = "STS_GROUP_";
		int section_index = 1;
		string config_section_name;
		string tmp_sts_tag, tmp_ecb_tag, tmp_gq_tag, tmp_bktime_27_tag;
		dyn_string tmp_sts_tag_list;

		config_section_name = section + "TOTAL";

		// [STS_GROUP_TOTAL]
		if (paCfgReadValue(config_path, config_section_name, "STS_TOTAL_TAG", cfg_total_tag) != 0)
		{
			writeLog(g_script_name, "Failed to load : [dp_name] STS_TAG", LV_ERR);
			is_result = false;
		}

		if(paCfgReadValueList(config_path, config_section_name, "STS_TAG", tmp_sts_tag_list)!=0)
			writeLog(g_script_name,"[ " + config_section_name + "] STS_TAG_LIST empty", LV_INFO);

		// map save - key : STS_GROUP_TOTAL
		// map save - value : STS_ALL_A
		g_map_cfg_info[config_section_name] = cfg_total_tag;

		msg += " STS_TOTAL_TAG = " + cfg_total_tag + "\n";

		// [STS_GROUP_index]
		while (true)
		{
			config_section_name = section + section_index;

			//[STS_GROUP_xx] STS_TAG
			if (paCfgReadValue(config_path, config_section_name, "STS_TAG", tmp_sts_tag) != 0)
			{
				if (section_index == 1)
				{
					writeLog(g_script_name, "Failed to load : [dp_name] STS_TAG", LV_ERR);
					is_result = false;
				}
				else
				{
					writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
					break;
				}
			}

			//[STS_GROUP_xx] ECB_TAG
			if (paCfgReadValue(config_path, config_section_name, "ECB_TAG", tmp_ecb_tag) != 0)
			{
				if (section_index == 1)
				{
					writeLog(g_script_name, "Failed to load : [dp_name] ECB_TAG", LV_ERR);
					is_result = false;
				}
				else
				{
					writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
					break;
				}
			}

			//[STS_GROUP_xx] GQ_TAG
			if (paCfgReadValue(config_path, config_section_name, "GQ_TAG", tmp_gq_tag) != 0)
			{
				if (section_index == 1)
				{
					writeLog(g_script_name, "Failed to load : [dp_name] GQ_TAG", LV_ERR);
					is_result = false;
				}
				else
				{
					writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
					break;
				}
			}
			
			//[STS_GROUP_xx] BKTIME_27_TAG
			if (paCfgReadValue(config_path, config_section_name, "BKTIME_27_TAG", tmp_bktime_27_tag) != 0)
			{
				if (section_index == 1)
				{
					writeLog(g_script_name, "Failed to load : [dp_name] BKTIME_27_TAG", LV_ERR);
					is_result = false;
				}
				else
				{
					writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
					break;
				}
			}

			msg += "\n [" + config_section_name + "]	\n" ;

			// map save - key : STS_GROUP_1
			// map save - value : STS_4F2_A, STS_ECB4F12LSG_A, STS_4F2_A
			g_map_cfg_info[config_section_name] = makeDynString(tmp_sts_tag, tmp_ecb_tag, tmp_gq_tag, tmp_bktime_27_tag);

			msg += " STS_TAG = " + tmp_sts_tag + "\n";
			msg += " ECB_TAG = " + tmp_ecb_tag + "\n";
			msg += " GQ_TAG = " + tmp_gq_tag + "\n";
			msg += " BKTIME_27_TAG = " + tmp_bktime_27_tag + "\n";

			section_index++;
			delay(0, 10);
		}

		writeLog(g_script_name, msg, LV_INFO);
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
		is_result = false;
	}

	finally
	{
		return is_result;
	}
}


//*******************************************************************************
// name         : master_sts_logic
// argument     :
// return value :
// date         : 2024-04-12
// developed by : KWH
// brief        : Master STS Logic
//*******************************************************************************
void master_sts_logic(dyn_string sts_taglist)
{
    string master_stslamp_dp, master_testlamp_dp, all_lrst_dp, all_test_dp, all_sts_dp;
    dyn_string stslamp_dps;
    dyn_bool lamptest_values, lamptest_list_bk;
    int sts_step = 0;
    int bktime_sec = 0;
    int sts_blink_check = 0;
    bool lamptest_flag_old = 0;
	bool bktime_flag = false;

    dyn_string stslamp_values;
	dyn_string bktime_values;

    // 감시 DP 명칭 정리
    for(int i = 1 ; i <= dynlen(sts_taglist) ; i++)
    {
		// P4_M154:STS_ALL_A_STSLAMP.OPLAST
		// P4_M154:STS_ALL_A_LRST_STATUS.alert.FLTKEEP
		// P4_M154:STS_ALL_A_TEST_STATUS.alert.FLTKEEP
		// P4_M154:STS_ALL_A
		master_stslamp_dp = sysname + sts_taglist[i] + cfg_stslamp_para;
		master_testlamp_dp = sysname + sts_taglist[i] + cfg_testlamp_para;
		all_lrst_dp = sysname + sts_taglist[i] + cfg_lrst_para;
		all_test_dp = sysname + sts_taglist[i] + cfg_test_para;
		all_sts_dp = sysname + sts_taglist[i];

		// LampTest를 위한 Lamp대상 추가
		dynAppend(lamptest_list, master_stslamp_dp);
		dynAppend(lamptest_list, master_testlamp_dp);
		
		g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_OFF;
    }

    // 감시 시작
    while(true)
    {
		try
		{
			writeLog(g_script_name, "Master STS Logic - Thread is operating normally." , LV_DBG2);
			dynClear(stslamp_values);
			dynClear(bktime_values);
			
			for(int i = 1; i <= mappinglen(g_map_stslamp); i++)
			{
				dynAppend(stslamp_values, mappingGetValue(g_map_stslamp, i));
			}
			
			for(int i = 1; i <= mappinglen(g_map_bktime_flag); i++)
			{
				dynAppend(bktime_values, mappingGetValue(g_map_bktime_flag, i));
			}
			
			// BKTIME Logic
			if(dynCount(bktime_values, ON_27) > 0)
			{
				// 첫 동작
				if(bktime_flag == false)
				{
					bktime_flag = true;
					bktime_sec = 0;
					
					if(isScriptActive == true)
					{
						time t = getCurrentTime();
						if(dpSetWait(all_sts_dp + cfg_runtime_para, t) != 0)
							writeLog(g_script_name, "master_sts_logic() - Master RunTime dpSet NG. dp_name = " + all_sts_dp + cfg_runtime_para + ", value = " + t, LV_ERR);
					}
				}
				else
				{
					bktime_sec++;
					if(isScriptActive == true)
					{
						if(dpSetWait(all_sts_dp + cfg_runcount_para, bktime_sec) != 0)
							writeLog(g_script_name, "master_sts_logic() - RunCount dpSet NG. dp_name = " + all_sts_dp + cfg_runcount_para + ", value = " + tmp_sec_check, LV_ERR);
					}
				}
			}
			else
			{
				if(bktime_flag == true)
				{
					bktime_flag = false;
					if(isScriptActive == true)
					{
						time t = getCurrentTime();
						if(dpSetWait(all_sts_dp + cfg_stoptime_para, t) != 0)
							writeLog(g_script_name, "master_sts_logic() - StopTime dpSet NG. dp_name = " + all_sts_dp + cfg_stoptime_para + ", value = " + t, LV_ERR);
					}
				}
			}

			// Master STS Lamp BLINK
			if(dynCount(stslamp_values, STATUS_LAMP_BLINK) > 0)
			{
				if(sts_step != 1)
				{
					sts_step = 1;
					writeLog(g_script_name, "master_sts_logic() - Master STS Lamp Blink.", LV_INFO);
					sts_blink_check = 0;
				}

				// Master STS Lamp -> BLINK
				if(g_map_masterlamp[master_stslamp_dp] != STATUS_LAMP_BLINK)
				{
					if(q_append(blink_list_ms_1000, master_stslamp_dp) == 0)
						g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_BLINK;
					else
						writeLog(g_script_name, "master_sts_logic() - Queue Append NG. dp_name = " + master_stslamp_dp, LV_ERR);
				}
				
				// 60초 경과
				sts_blink_check++;
				if(sts_blink_check == SEC_60)
				{
					// Master STS Lamp -> BLINK 1초 -> 0.1초
					if(q_remove(blink_list_ms_1000, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Remove NG. dp_name = " + master_stslamp_dp, LV_ERR);
					
					if(q_append(blink_list_ms_100, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Append NG. dp_name = " + master_stslamp_dp, LV_ERR);
				}
			}

			// Master STS Lamp ON
			else if(dynCount(stslamp_values, STATUS_LAMP_BLINK) == 0 && dynCount(stslamp_values, STATUS_LAMP_ON) > 0)
			{
				if(sts_step != 2)
				{
					sts_step = 2;
					writeLog(g_script_name, "master_sts_logic() - Master STS Lamp On.", LV_INFO);
				}

				// Master STS Lamp -> ON
				if(g_map_masterlamp[master_stslamp_dp] != STATUS_LAMP_ON)
				{
					if(q_remove(blink_list_ms_1000, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Remove NG. dp_name = " + master_stslamp_dp, LV_ERR);

					if(q_remove(blink_list_ms_100, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Remove NG. dp_name = " + master_stslamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(master_stslamp_dp, true) == 0)
							g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_ON;
						else
							writeLog(g_script_name, "master_sts_logic() - Master STS Lamp On NG. dp_name = " + master_stslamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_ON;
					}
				}
			}

			// STS Lamp OFF
			else if(dynCount(stslamp_values, STATUS_LAMP_OFF) == dynlen(stslamp_values))
			{
				if(sts_step != 0)
				{
					sts_step = 0;
					writeLog(g_script_name, "master_sts_logic() - Master STS Lamp Off", LV_INFO);
				}

				// Master STS Lamp OFF
				if(g_map_masterlamp[master_stslamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_1000, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Remove NG. dp_name = " + master_stslamp_dp, LV_ERR);

					if(q_remove(blink_list_ms_100, master_stslamp_dp) != 0)
						writeLog(g_script_name, "master_sts_logic() - Queue Remove NG. dp_name = " + master_stslamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(master_stslamp_dp, false) == 0)
							g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "master_sts_logic() - Master STS Lamp Off NG. dp_name = " + master_stslamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_masterlamp[master_stslamp_dp] = STATUS_LAMP_OFF;
					}
				}
			}

			// UI 및 STS Board Reset 감지하여 Reset 동작 + Lamp Test
			if(dpGet(all_sts_dp + cfg_reset_para, reset_flag,
					 all_lrst_dp, lrst_flag,
					 all_test_dp, lamptest_flag) != 0)
			{
				writeLog(g_script_name,"master_sts_logic() - STS Reset Flag dpGet NG. dp_name = " + all_sts_dp + cfg_reset_para + ", value = " + reset_flag, LV_ERR);
				delay_cycle(1);
				continue;
			}

			// reset
			if(reset_flag == true && isScriptActive == true)
			{
				writeLog(g_script_name, "master_sts_logic() - Reset Flag On - Master BKTIME Reset.", LV_INFO);

				if(dpSetWait(all_sts_dp + cfg_runtime_para, "1970.01.01 09:00:00.000",
						     all_sts_dp + cfg_stoptime_para, "1970.01.01 09:00:00.000",
							 all_sts_dp + cfg_runcount_para, "0") != 0)
				{
					writeLog(g_script_name,"master_sts_logic() - Master STS BKTIME Reset dpSet NG. dp_name = " + all_sts_dp + ", value = " + 0, LV_ERR);
				}
			}

			// lamp test
			if(lamptest_flag != lamptest_flag_old && isScriptActive == true)
			{
				if(lamptest_flag == true)
				{
					writeLog(g_script_name, "master_sts_logic() - Lamp Test Flag On - Master Lamp On.", LV_INFO);
					dynClear(lamptest_values);

					for(int i = 1 ; i <= dynlen(lamptest_list) ; i++)
					{
						dynAppend(lamptest_values, lamptest_flag);
					}

					// 기존 값 Backup 이후 LAMP 전체 점등
					if(dpGet(lamptest_list, lamptest_list_bk) != 0)
						writeLog(g_script_name, "master_sts_logic() - STS Lamp State Backup dpGet NG.", LV_ERR);

					if(dpSetWait(lamptest_list, lamptest_values) != 0)
						writeLog(g_script_name, "master_sts_logic() - STS Lamp TEST Start dpSet NG.", LV_ERR);
					
				  }
				else
				{
					writeLog(g_script_name, "master_sts_logic() - Lamp Test Flag Off - Master Lamp Reset.", LV_INFO);

					// 기존 Backup 값을 다시 Update
					if(dpSetWait(lamptest_list, lamptest_list_bk) != 0)
						writeLog(g_script_name, "master_sts_logic() - STS Lamp TEST End dpSet NG.", LV_ERR);

				}

			  lamptest_flag_old = lamptest_flag;
			}

			g_map_heartbeat[master_stslamp_dp] = true;
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of master_sts_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
    }
}

//*******************************************************************************
// name         : master_rj_logic
// argument     :
// return value :
// date         : 2024-05-31
// developed by : KWH
// brief        : Master RJ Logic
//*******************************************************************************
void master_rj_logic(dyn_string sts_taglist)
{
	string master_rjlamp_dp;
	int sts_step = 0;

	dyn_string rjlamp_values;

	// 감시 DP 명칭 정리
	for(int i = 1 ; i <= dynlen(sts_taglist) ; i++)
	{
		// P4_M154:STS_ALL_A_RJLAMP.OPLAST
		master_rjlamp_dp = sysname + sts_taglist[i] + cfg_rjlamp_para;
	}

	// LampTest를 위한 Lamp대상 추가
	dynAppend(lamptest_list, master_rjlamp_dp);
	
	g_map_masterlamp[master_rjlamp_dp] = STATUS_LAMP_OFF;

    // 감시 시작
    while(true)
    {
		try
		{
			writeLog(g_script_name, "Master RJ Logic - Thread is operating normally." , LV_DBG2);

			dynClear(rjlamp_values);

			for(int i = 1; i <= mappinglen(g_map_rjlamp); i++)
			{
				dynAppend(rjlamp_values, mappingGetValue(g_map_rjlamp, i));
			}

			// Master RJ Lamp BLINK
			if(dynCount(rjlamp_values, STATUS_LAMP_BLINK) > 0)
			{
				if(sts_step != 1)
				{
					sts_step = 1;
					writeLog(g_script_name,"master_rj_logic() - Master RJ Lamp Blink", LV_INFO);
				}

				// Master RJ Lamp -> BLINK
				if(g_map_masterlamp[master_rjlamp_dp] != STATUS_LAMP_BLINK)
				{
					if(q_append(blink_list_ms_100, master_rjlamp_dp) == 0)
						g_map_masterlamp[master_rjlamp_dp] = STATUS_LAMP_BLINK;
					else
						writeLog(g_script_name, "master_rj_logic() - Queue Append NG. dp_name = " + master_rjlamp_dp, LV_ERR);
				}
			}

			// Master RJ Lamp OFF
			else if(dynCount(rjlamp_values, STATUS_LAMP_OFF) == dynlen(rjlamp_values))
			{
				if(sts_step != 2)
				{
					sts_step = 2;
					writeLog(g_script_name,"master_rj_logic() - Master RJ Lamp Off", LV_INFO);
				}

				// Master RJ Lamp -> OFF
				if(g_map_masterlamp[master_rjlamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_100, master_rjlamp_dp) != 0)
						writeLog(g_script_name, "master_rj_logic() - Queue Remove NG. dp_name = " + master_rjlamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(master_rjlamp_dp, false) == 0)
							g_map_masterlamp[master_rjlamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "master_rj_logic() - Master RJ Lamp Off NG. dp_name = " + master_rjlamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_masterlamp[master_rjlamp_dp] = STATUS_LAMP_OFF;
					}

				}
			}

			g_map_heartbeat[master_rjlamp_dp] = true;
		}

		catch
		{
			update_user_alarm(manager_dpname, "Exception of master_rj_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
    }
}

//*******************************************************************************
// name         : master_rs_logic
// argument     :
// return value :
// date         : 2024-05-31
// developed by : KWH
// brief        : Master RS Logic
//*******************************************************************************
void master_rs_logic(dyn_string sts_taglist)
{
	string master_rslamp_dp;
	int sts_step = 0;

	dyn_string rjlamp_values;
	dyn_string rjelamp_values;
	dyn_string rslamp_values;
	dyn_bool rjx_values;

	// 감시 DP 명칭 정리
	for(int i = 1 ; i <= dynlen(sts_taglist) ; i++)
	{
		// P4_M154:STS_ALL_A_RJLAMP.OPLAST
		// P4_M154:STS_ALL_A_RSLAMP.OPLAST
		master_rslamp_dp = sysname + sts_taglist[i] + cfg_rslamp_para;
	}

	// LampTest를 위한 Lamp대상 추가
	dynAppend(lamptest_list, master_rslamp_dp);
	
	g_map_masterlamp[master_rslamp_dp] = STATUS_LAMP_OFF;

    // 감시 시작
    while(true)
    {
		try
		{
			writeLog(g_script_name, "Master RS Logic - Thread is operating normally." , LV_DBG2);

			dynClear(rjlamp_values);
			dynClear(rjelamp_values);
			dynClear(rslamp_values);
			dynClear(rjx_values);

			for(int i = 1; i <= mappinglen(g_map_rjlamp); i++)
			{
				dynAppend(rjlamp_values, mappingGetValue(g_map_rjlamp, i));
				dynAppend(rjelamp_values, mappingGetValue(g_map_rjelamp, i));
				dynAppend(rslamp_values, mappingGetValue(g_map_rslamp, i));
				dynAppend(rjx_values, mappingGetValue(g_map_rjx_values, i));
			}

			// Master RS Lamp BLINK
			if(dynCount(rjlamp_values, STATUS_LAMP_OFF) == dynlen(rjlamp_values) && dynCount(rjelamp_values, STATUS_LAMP_OFF) == dynlen(rjelamp_values) && dynCount(rslamp_values, STATUS_LAMP_BLINK) > 0)
			{
				if(sts_step != 1)
				{
					sts_step = 1;
					writeLog(g_script_name,"master_rs_logic() - Master RS Lamp Blink", LV_INFO);
				}

				// Master RS Lamp -> Blink Queue 추가
				if(q_append(blink_list_ms_100, master_rslamp_dp) == 0)
					g_map_masterlamp[master_rslamp_dp] = STATUS_LAMP_BLINK;
				else
					writeLog(g_script_name, "master_rs_logic() - Queue Append NG. dp_name = " + master_rslamp_dp, LV_ERR);
			}

			// RS LAMP OFF
			else if((dynCount(rjlamp_values, STATUS_LAMP_BLINK) > 0 || dynCount(rjelamp_values, STATUS_LAMP_BLINK) > 0) ||
					(dynCount(rjlamp_values, STATUS_LAMP_OFF) == dynlen(rjlamp_values) && dynCount(rjelamp_values, STATUS_LAMP_OFF) == dynlen(rjelamp_values) && dynCount(rjx_values, false) == dynlen(rjx_values)))
			{
				if(sts_step != 0)
				{
					sts_step = 0;
					writeLog(g_script_name,"master_rs_logic() - Master RS Lamp Off", LV_INFO);
				}
				
				// Master RS Lamp -> OFF
				if(g_map_masterlamp[master_rslamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_100, master_rslamp_dp) != 0)
						writeLog(g_script_name, "master_rs_logic() - Queue Remove NG. dp_name = " + master_rslamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(master_rslamp_dp, false) == 0)
							g_map_masterlamp[master_rslamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "master_rs_logic() - Master RS Lamp Off NG. dp_name = " + master_rslamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_masterlamp[master_rslamp_dp] = STATUS_LAMP_OFF;
					}
				}
			}

			g_map_heartbeat[master_rslamp_dp] = true;
		}

		catch
		{
			update_user_alarm(manager_dpname, "Exception of master_rj_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
    }
}

//*******************************************************************************
// name         : main_sts_logic
// argument     : sts_taglist (STS_TAG, ECB_TAG, GQ_TAG)
// return value :
// date         : 2024-04-12
// developed by : KWH
// brief        : STS Main Logic
//*******************************************************************************
void main_sts_logic(dyn_string sts_taglist)
{
	bool all_lrst_value;
    string stslamp_dp, rjlamp_dp, rjelamp_dp;
    string ecb_status_dp, ecb_27_dp, gq_status_dp, ecb_rjx_dp, ecb_bktime_dp, bktime_27_dp;
    bool ecb_status_value, ecb_27_value, gq_status_value, ecb_rjx_value, bktime_27_value;
    int sts_step = 0;
    int bktime_sec = 0;
	int sts_blink_check = 0;
    int lrst_sec = 0;
    bool bk_flag;

    // 감시 DP 명칭 정리
    for(int i = 1 ; i <= dynlen(sts_taglist) ; i++)
    {
		if(patternMatch("STS_ECB_*", sts_taglist[i]))
		{
			bktime_27_dp = sysname + sts_taglist[i] + cfg_27_para;
		}
		else if(patternMatch("STS_ECB*", sts_taglist[i]))
		{
			ecb_status_dp = sysname + sts_taglist[i] + cfg_status_para;
			ecb_27_dp = sysname + sts_taglist[i] + cfg_27_para;
			ecb_rjx_dp = sysname + sts_taglist[i] + cfg_rjx_para;
			ecb_bktime_dp = sysname + sts_taglist[i];
		}
		else if(patternMatch("STS_VCB*", sts_taglist[i]))
		{
			gq_status_dp = sysname + sts_taglist[i] + cfg_status_para;
		}
		else
		{
			stslamp_dp = sysname + sts_taglist[i] + cfg_stslamp_para;
			rjlamp_dp = sysname + sts_taglist[i] + cfg_rjlamp_para;
			rjelamp_dp = sysname + sts_taglist[i] + cfg_rjelamp_para;
		}
    }

    // LampTest를 위한 Lamp대상 추가
    dynAppend(lamptest_list, stslamp_dp);
    dynAppend(lamptest_list, rjlamp_dp);
    dynAppend(lamptest_list, rjelamp_dp);

    g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
    g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
    g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
    g_map_rslamp[rjelamp_dp] = STATUS_LAMP_OFF; 		// rs는 실제로 존재하지 않는 대상이므로 rj dp명칭으로 대체
	
	g_map_bktime_flag[bktime_27_dp] = OFF_27;

    while(true)
    {
		try
		{
			writeLog(g_script_name, "main_sts_logic() - Thread is operating normally. Logic DP : " + ecb_status_dp, LV_DBG2);

			// dp 조회
			// 1초 주기로 값을 확인하여 Step 별 동작
			if(dpGet(ecb_status_dp, ecb_status_value,
					 gq_status_dp, gq_status_value,
					 ecb_27_dp, ecb_27_value,
					 ecb_rjx_dp, ecb_rjx_value,
					 bktime_27_dp, bktime_27_value) != 0)
			{
				writeLog(g_script_name, "main_sts_logic() - Step0. 1sec Cycle - DP Get NG.", LV_ERR);
				delay_cycle(1);
				continue;
			}

			// rjx 저장
			g_map_rjx_values[ecb_rjx_dp] = ecb_rjx_value;

			// Step과 무관하게 27 감시하여 정전 BKTIME 동작  60초 유지시 0.5초 Q 추가
			if(bktime_27_value == true)
			{
				// 첫 정전 인지
				if(g_map_bktime_flag[bktime_27_dp] == OFF_27)
				{
					g_map_bktime_flag[bktime_27_dp] = ON_27;

					if(isScriptActive == true)
					{
						// 정전 시, BKTIME 입력
						time t = getCurrentTime();
						if(dpSetWait(ecb_bktime_dp + cfg_runtime_para, t) != 0)
							writeLog(g_script_name, "main_sts_logic() - RunTime dpSet NG. dp_name = " + ecb_bktime_dp + cfg_runtime_para + ", value = " + t, LV_ERR);
					}
				}
				else
				{
					bktime_sec++;
					if(isScriptActive == true)
					{
						if(dpSetWait(ecb_bktime_dp + cfg_runcount_para, bktime_sec) != 0)
							writeLog(g_script_name, "main_sts_logic() - RunCount dpSet NG. dp_name = " + ecb_bktime_dp + cfg_runcount_para + ", value = " + tmp_sec_check, LV_ERR);
					}
				}
			}
			else
			{
				// 정전 해제 시, 복전 BKTIME 동작
				if(g_map_bktime_flag[bktime_27_dp] == ON_27)
				{
					g_map_bktime_flag[bktime_27_dp] = OFF_27;
					bktime_sec = 0;

					if(isScriptActive == true)
					{
						time t = getCurrentTime();
						if(dpSetWait(ecb_bktime_dp + cfg_stoptime_para, t) != 0)
							writeLog(g_script_name, "main_sts_logic() - StopTime dpSet NG. dp_name = " + ecb_bktime_dp + cfg_stoptime_para + ", value = " + t, LV_ERR);
					}
				}
			}

			// 정상 대기 상태
			if(ecb_rjx_value == false && ecb_status_value == true && ecb_27_value == false && gq_status_value == false)
			{
				if(sts_step != 0)
				{
					sts_step = 0;
					writeLog(g_script_name,"main_sts_logic() - STS Normal State. DP = " + ecb_status_dp, LV_INFO);
				}
			  
				// STS Lamp -> OFF
				if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
						writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
					if(q_remove(blink_list_ms_100, stslamp_dp) != 0)
						writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(stslamp_dp, false) == 0)
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "main_sts_logic() - STS Lamp Off NG. dp_name = " + stslamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
					}
				}
				
				// RJE Lamp -> OFF
				if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
						writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(rjelamp_dp, false) == 0)
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
					}
				}
				
				// RJ Lamp -> OFF
				if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_OFF)
				{
					if(q_remove(blink_list_ms_100, rjlamp_dp) != 0)
						writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
					
					if(isScriptActive == true)
					{
						if(dpSetWait(rjlamp_dp, false) == 0)
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
						else
							writeLog(g_script_name, "main_sts_logic() - RJ Lamp Off NG. dp_name = " + rjlamp_dp + ", value = " + false, LV_ERR);
					}
					else
					{
						// Secondary Server 값 저장
						g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
					}
				}
				
				// RS Lmap -> OFF
				g_map_rslamp[rjlamp_dp] = STATUS_LAMP_OFF;
			}
			else
			{
				// STS Lamp BLINK
				if(ecb_27_value == true && gq_status_value == false)
				{
					if(sts_step != 1)
					{
						sts_step = 1;
						writeLog(g_script_name, "main_sts_logic() - STS Lamp Blink. DP = " + ecb_status_dp, LV_INFO);
						sts_blink_check = 0;
					}
				  
					// STS Lamp -> BLINK
					if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_BLINK)
					{
						if(q_append(blink_list_ms_1000, stslamp_dp) == 0)
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_BLINK;
						else
							writeLog(g_script_name, "main_sts_logic() - Queue Append NG. dp_name = " + stslamp_dp, LV_ERR);
					}
					
					// RJE Lamp -> OFF
					if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjelamp_dp, false) == 0)
								g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RJ Lamp -> OFF
					if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjlamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjlamp_dp, false) == 0)
								g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJ Lamp Off NG. dp_name = " + rjlamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RS Lmap -> OFF
					g_map_rslamp[rjlamp_dp] = STATUS_LAMP_OFF;
					
					sts_blink_check++;
					// 60초에 STS Lamp Queue 변경
					if(sts_blink_check == SEC_60)
					{
						if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						if(q_append(blink_list_ms_100, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Append NG. dp_name = " + stslamp_dp, LV_ERR);
					}
				}

				// STS Lamp 점등
				else if(ecb_27_value == true && gq_status_value == true)
				{
					if(sts_step != 2)
					{
						sts_step = 2;
						writeLog(g_script_name, "main_sts_logic() - STS Lamp On. DP = " + ecb_status_dp, LV_INFO);
					}
				  
					// STS Lamp -> ON
					if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_ON)
					{
						if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						if(q_remove(blink_list_ms_100, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(stslamp_dp, true) == 0)
								g_map_stslamp[stslamp_dp] = STATUS_LAMP_ON;
							else
								writeLog(g_script_name, "main_sts_logic() - STS Lamp On NG. dp_name = " + stslamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_ON;
						}
					}
					
					// RJE Lamp -> OFF
					if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjelamp_dp, false) == 0)
								g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
						}	
						else
						{
							// Secondary Server 값 저장
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RJ Lamp -> OFF
					if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjlamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjlamp_dp, false) == 0)
								g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJ Lamp Off NG. dp_name = " + rjlamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RS Lmap -> OFF
					g_map_rslamp[rjlamp_dp] = STATUS_LAMP_OFF;
				}

				//  RJE Lamp BLINK
				else if(ecb_rjx_value == false && ecb_27_value == false && gq_status_value == true)
				{
					if(sts_step != 3)
					{
						sts_step = 3;
						writeLog(g_script_name, "main_sts_logic() - RJE Lamp Blink. DP = " + ecb_status_dp, LV_INFO);
					}

					// STS Lamp -> OFF
					if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						if(q_remove(blink_list_ms_100, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(stslamp_dp, false) == 0)
								g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - STS Lamp Off NG. dp_name = " + stslamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
						}
					}

					// RJE Lamp -> BLINK
					if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_BLINK)
					{
						if(q_append(blink_list_ms_100, rjelamp_dp) == 0)
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_BLINK;
						else
							writeLog(g_script_name, "main_sts_logic() - Queue Append NG. dp_name = " + rjelamp_dp, LV_ERR);
					}
					
					// RJ Lamp -> OFF
					if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjlamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjlamp_dp, false) == 0)
								g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJ Lamp Off NG. dp_name = " + rjlamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RS Lmap -> OFF
					g_map_rslamp[rjlamp_dp] = STATUS_LAMP_OFF;
				}

				// RJ Lamp BLINK
				else if(ecb_rjx_value == true && ecb_27_value == false && gq_status_value == true)
				{
					if(sts_step != 4)
					{
						sts_step = 4;
						writeLog(g_script_name, "main_sts_logic() - RJ Lamp Blink. DP = " + ecb_status_dp, LV_INFO);
					}
				  
					// STS Lamp -> OFF
					if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						if(q_remove(blink_list_ms_100, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(stslamp_dp, false) == 0)
								g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - STS Lamp Off NG. dp_name = " + stslamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RJE Lamp -> OFF
					if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjelamp_dp, false) == 0)
								g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					
					// RJ Lamp -> BLINK
					if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_BLINK)
					{
						if(q_append(blink_list_ms_100, rjlamp_dp) == 0)
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_BLINK;
						else
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
					}
					
					// RS Lmap -> OFF
					g_map_rslamp[rjlamp_dp] = STATUS_LAMP_OFF;
				}

				// RS Lamp BLINK (실제 동작은 안하나, 변수로 저장하여 Master에서 사용)
				else if(ecb_rjx_value == true && ecb_status_value == true && ecb_27_value == false)
				{
					if(sts_step != 6)
					{
						sts_step = 6;
						writeLog(g_script_name, "main_sts_logic() - RS Lamp Blink. DP = " + ecb_status_dp, LV_INFO);
					}

					// STS Lamp -> OFF
					if(g_map_stslamp[stslamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_1000, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						if(q_remove(blink_list_ms_100, stslamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + stslamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(stslamp_dp, false) == 0)
								g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - STS Lamp Off NG. dp_name = " + stslamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_stslamp[stslamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RJE Lamp -> OFF
					if(g_map_rjelamp[rjelamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjelamp_dp, false) == 0)
								g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						}
					}
					
					// RJ Lamp -> OFF
					if(g_map_rjlamp[rjlamp_dp] != STATUS_LAMP_OFF)
					{
						if(q_remove(blink_list_ms_100, rjlamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjlamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjlamp_dp, false) == 0)
								g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJ Lamp Off NG. dp_name = " + rjlamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjlamp[rjlamp_dp] = STATUS_LAMP_OFF;
						}
					}

					// RS Lmap -> BLINK
					g_map_rslamp[rjlamp_dp] = STATUS_LAMP_BLINK;
				}

				// ALL LRST 3초 유지 -> RJE 해제
				// 동작 안해도 되는 Logic
				if(lrst_flag == true && ecb_status_value == true && gq_status_value == false && ecb_27_value == false)
				{
					if(lrst_sec == RESET_SEC_3)
					{
						// RJE Lamp -> Blink Queue 제거 -> 해제
						if(q_remove(blink_list_ms_100, rjelamp_dp) != 0)
							writeLog(g_script_name, "main_sts_logic() - Queue Remove NG. dp_name = " + rjelamp_dp, LV_ERR);
						
						if(isScriptActive == true)
						{
							if(dpSetWait(rjelamp_dp, false) == 0)
								g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
							else
								writeLog(g_script_name, "main_sts_logic() - RJE Lamp Off NG. dp_name = " + rjelamp_dp + ", value = " + false, LV_ERR);
						}
						else
						{
							// Secondary Server 값 저장
							g_map_rjelamp[rjelamp_dp] = STATUS_LAMP_OFF;
						}
					}

					lrst_sec++;
				}
				// 연속 3초 유지 X -> 초기화
				else
				{
					lrst_sec = 0;
				}
			}
			
			// RESET
		    if(reset_flag == true && isScriptActive == true)
			{
				if(dpSetWait(ecb_bktime_dp + cfg_runtime_para, "1970.01.01 09:00:00.000",
							 ecb_bktime_dp + cfg_stoptime_para, "1970.01.01 09:00:00.000",
							 ecb_bktime_dp + cfg_runcount_para, "0") != 0)
				{
					writeLog(g_script_name, "main_sts_logic() - STS BKTIME Reset NG. dp_name = " + ecb_bktime_dp + ", value = " + 0, LV_ERR);
				}
			}
			// Thread Check를 위한 Heartbeat
			g_map_heartbeat[ecb_bktime_dp] = true;
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of main_sts_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
    }
}



//*******************************************************************************
// name         : heartbeat_check
// argument     :
// return value :
// date         : 2024-04-12
// developed by : KWH
// brief        : heartbeat_check
//*******************************************************************************
void heartbeat_check()
{
	while(true)
	{
		try
		{
			writeLog(g_script_name, "HeartBeat Check - Thread is operating normally." , LV_DBG2);
			int hb_count=0;

			for(int i = 1 ; i <= mappinglen(g_map_heartbeat) ; i++)
			{
				bool mapping_value = mappingGetValue(g_map_heartbeat, i);

				if(mapping_value == true)
					hb_count++;
			}

			if(hb_count == mappinglen(g_map_heartbeat))
			{
				//delay = 5이므로, HB도 5씩증가
				update_heartbeat(manager_dpname);

				for(int i = 1 ; i <= mappinglen(g_map_heartbeat) ; i++)
				{
					string key = mappingGetKey(g_map_heartbeat, i);
					g_map_heartbeat[key] = false;
				}
			}
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of heartbeat_check() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(5);
		}
	}
}


//*******************************************************************************
// name         : blink_list_ms_1000_logic
// argument     :
// return value :
// date         : 2024-04-15
// developed by : KWH
// brief        : lamp output cycle - 1sec
//*******************************************************************************
void blink_list_ms_1000_logic()
{
    dyn_string blink_list_ms_1000_dps;
    dyn_bool blink_list_ms_1000_values;
    bool value;

    while(true)
    {
		try
		{
			writeLog(g_script_name, "Blink Logic 1sec - Thread is operating normally." , LV_DBG2);

			// dp가 있을때만 동작
			if(dynlen(blink_list_ms_1000) > 0 && lamptest_flag == false)
			{
				blink_list_ms_1000_dps = blink_list_ms_1000;

				// value 초기화 이후, dp수량에 맞게 value값 입력
				dynClear(blink_list_ms_1000_values);
				value = !value;

				for(int i = 1 ; i <= dynlen(blink_list_ms_1000_dps) ; i++)
				{
					dynAppend(blink_list_ms_1000_values, value);
				}

				// dpSet
				if(setDpValue_block(blink_list_ms_1000_dps, blink_list_ms_1000_values) == false)
				{
					writeLog(g_script_name,"blink_list_ms_1000_logic() - dpSet - NG. set_points = "
							+ dynlen(blink_list_ms_1000_dps) + ", set_values = " + dynlen(blink_list_ms_1000_values), LV_ERR);
				}
			}
		  }

		catch
		{
			update_user_alarm(manager_dpname, "Exception of blink_list_ms_1000_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
    }
}

//*******************************************************************************
// name         : blink_list_ms_100_logic
// argument     :
// return value :
// date         : 2024-04-15
// developed by : KWH
// brief        : lamp output cycle - 0.1sec
//*******************************************************************************
void blink_list_ms_100_logic()
{
    dyn_string blink_list_ms_100_dps;
    dyn_bool blink_list_ms_100_values;
    bool value;

    while(true)
    {
		try
		{
			writeLog(g_script_name, "Blink Logic 0.1sec - Thread is operating normally." , LV_DBG2);

			// dp가 있을때만 동작
			if(dynlen(blink_list_ms_100) > 0 && lamptest_flag == false)
			{
				blink_list_ms_100_dps = blink_list_ms_100;

				// value 초기화 이후, dp수량에 맞게 value값 입력
				dynClear(blink_list_ms_100_values);
				value = !value;

				for(int i = 1 ; i <= dynlen(blink_list_ms_100_dps) ; i++)
				{
					dynAppend(blink_list_ms_100_values, value);
				}

				// dpset
				if(setDpValue_block(blink_list_ms_100_dps, blink_list_ms_100_values) == false)
				{
					writeLog(g_script_name,"blink_list_ms_100_logic() - dpSet - NG. set_points = "
							+ dynlen(blink_list_ms_100_dps) + ", set_values = " + dynlen(blink_list_ms_100_values), LV_ERR);
				}
			}
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of blink_list_ms_100_logic() - for. Error = " + getLastException());
		}
		finally
		{
			delay(0, 100);
		}
    }
}


//*******************************************************************************
// name         : q_remove
// argument     : blink_list_ms_1000, blink_list_ms_100
// return value :
// date         : 2024-05-31
// developed by : KWH
// brief        : Blink Queue Remove
//*******************************************************************************
int q_remove(dyn_string& remove_q, string lamp_dpe_name)
{
	int result = 0;

	try
	{
		synchronized(blink_list_ms_1000)
		{
			int i = dynContains(remove_q, lamp_dpe_name);

			if(i != 0)
			{
				writeLog(g_script_name, "q_remove() - Blink Queue Remove OK. dp_name = " + lamp_dpe_name, LV_INFO);
				dynRemove(remove_q, i);
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of q_remove(). Error = " + getLastException());
		result = -1;
	}
	finally
	{
		return result;
	}
}

//*******************************************************************************
// name         : q_append
// argument     : blink_list_ms_1000, blink_list_ms_100
// return value :
// date         : 2024-05-31
// developed by : KWH
// brief        : Blink Queue Append
//*******************************************************************************
int q_append(dyn_string& append_q, string lamp_dpe_name)
{
	int result = 0;
	  
	try
	{
		synchronized(blink_list_ms_1000)
		{
			if(dynContains(append_q, lamp_dpe_name) == 0)
			{
				writeLog(g_script_name, "q_append() - Blink Queue Append OK. dp_name = " + lamp_dpe_name, LV_INFO);
				dynAppend(append_q, lamp_dpe_name);
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of q_remove(). Error = " + getLastException());
		result = -1;
	}

	finally
	{
		return result;
	}
}
