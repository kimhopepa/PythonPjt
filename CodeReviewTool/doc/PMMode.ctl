//v0.1 (2020.06.09)-----------------------------------------
//1. PMMode ��� ���� ��ũ��Ʈ ���� �ۼ�
//-----------------------------------------------------------
//v0.2 (2020.07.09)-----------------------------------------
//1. PMMode ���� �� ���� ���� ���� �÷� �ʱ�ȭ
//-----------------------------------------------------------
//v1.01 (2020.11.02)-----------------------------------------
//1. ������ DB�� �����Ͱ� ��ġ���� ���� �� ������ �����ϰ� DB ������ Update
//2. DB reconnection �߰� 
//-----------------------------------------------------------
//v1.02 (2020.11.13)-----------------------------------------
//1. DPE ���� ���� Ȯ�� -> alert_hdl config ���� ���� üũ�� ����
//-----------------------------------------------------------
//v1.03 (2020.12.18)-----------------------------------------
//1. Query�� EQP_NO ��ȸ ���� ���� (SITE_CODE, SYS_CODE ����)
//2. config SITE_CODE, SYS_CODE ����
//-----------------------------------------------------------
//v1.04 (2021.05.12)-----------------------------------------
//1. EQP_NO ����Ʈ�� 1,000�� �̻��� ��� ����  : check_pmmode_end_notify(), check_pmmode_end_overtime_wait_state() �Լ� ����
//-----------------------------------------------------------
//v1.05(2021.06.30) ------------------------------------------
//1. Add config File name lookup from manager dp
//-----------------------------------------------------------
//v1.06(2021.11.01)------------------------------------------
//1. PMMODE ������ �˶� �߻� ���� ���� : TN_CM_PM_APPR ���̺��� ���� Ȯ�� �� min_prio ���� ���� Ȯ��
// Y -> ���� Logic ����, N -> min_prio ���� ���� ���� (N �ƴ� ��� ���� Logic��� ����)
//-----------------------------------------------------------
//v1.07(2023.01.26) ------------------------------------------
//1. PMMODE ���� �� delay config �߰� : cfg_delay_check_pmmode_start_end_sec
//-----------------------------------------------------------
//v1.08(2023.02.17) ------------------------------------------
//1. PMMODE �̷� ���� Query ���� : TH_CM_PM ���̺� ����� APPR_USER_ID �� �����Ͽ� ���� (TN_CM_PM_APPR���̺��� APPR_USER_ID ������ ����)
//2. PMMODE ���� ���� Tag�� �������� ���� �� ��� ���� ó�� �߰�
//-----------------------------------------------------------

#uses "CtrlADO"
#uses "library_DB.ctl"
#uses "library_standard.ctl"
#uses "hosts.ctl"

//-----------------------------------------------------------
// Variable Define
//-----------------------------------------------------------
// configuration path & filename
string config_filename;
const string g_script_release_version = "v1.08"; 
const string g_script_release_date = "2023.02.17";
const string g_script_name = "PMMode";
string manager_dpname = "";  			// ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)
string ScriptActive_Condition = "ACTIVE";	// |BOTH|HOST1|HOST2"; // lib_Common���� ���

//config 
// general
string cfg_extend_dp = "Trig_PM_APPR.Bool_02";	// ���� ���� �˸� Trigger
string cfg_pmmode_dp = ".internal.PMMODE";		// PMMode ���� DP
string cfg_approval_code = "APPR_A";			// PMMode ���� ���� �ڵ�
string cfg_reject_code = "APPR_B";				// PMMode ���� ���� �ڵ�
string cfg_wait_code = "APPR_C";				// PMMode ���� ���� �ڵ�
string cfg_user_id = "AUTO";					// PMMode ��ũ��Ʈ���� ���۽�Ų user id �ڵ�
int cfg_delay_check_pmmode_sec = 60;			// pmmode Ȯ�� �ֱ� (��)
int cfg_delay_check_pmmode_start_end_sec = 2;	// pmmode ���� & ���� Ȯ�� �ֱ� (��)
int cfg_pmmode_end_notify_time_min = 30;		// pmmode ���� ���� �˸� �ð� ����
int cfg_block_size = 200;						// �������� dp�� ���� �� delay �� dp ����
int cfg_alrm_ext_yn = 0;						// v1.06 �� �߰� : �˶� �߻� ���� �Ǵ� 1 -> min_prio ���� ���� , 0 -> ���� Logic

// parend_info
string cfg_pjt_id;		// ����Ʈ ����

// DB Connection
dbConnection CONN_DB;
string db_con_info;

// Constant
const int RTN_VALUE_ERROR = -1;			// API ���� ���� ���ϰ�
const int RTN_VALUE_OK = 0;				// API ���� ���� ���ϰ�
const string MOD_USER_ID = "SCRIPT";       // MOD_USER_ID �Է°� 

// flag
bool is_complete_check_pmmode_start_reservation = false;	// check_pmmode_start_reservation 1 cycle ���μ��� �Ϸ� ���� Ȯ�� flag
bool is_complete_check_pmmode_end_notify = false;		// check_pmmode_end_notify 1 cycle ���μ��� �Ϸ� ���� Ȯ�� flag
bool is_complete_check_pmmode_end_overtime = false;		// check_pmmode_end_overtime 1 cycle ���μ��� �Ϸ� ���� Ȯ�� flag
bool is_complete_check_pmmode_end_overtime_wait_state = false;		// check_pmmode_end_overtime_wait_state 1 cycle ���μ��� �Ϸ� ���� Ȯ�� flag

const string EQP_NO_CONDITION = "EQP_NO_CONDITION";
//*******************************************************************************
// name         : main()
// argument     :
// return value :
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : Script main function
//*******************************************************************************
void main()
{
	int thread_id;

	try
	{
		writeLog(g_script_name, "===== Script initialize start =====", LV_INFO);

		//-----------------------------------------------------------
		// 0. Common library initialize
		//-----------------------------------------------------------
		// Debug-Flag Initialize
		init_lib_Commmon();

		// Script infomation Log write
		writeLog(g_script_name, "0. Script info. Release version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
		writeLog(g_script_name, "                lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);
		writeLog(g_script_name, "                lib_db Version = " + g_lib_db_version + ", Date = " + g_lib_db_release_date, LV_INFO);

		//Create Script Monitoring DP
		manager_dpname = init_program_info(g_script_name, g_script_release_version, g_script_release_date);

		//-----------------------------------------------------------
		// 1. Load Configuration
		//-----------------------------------------------------------
		if (load_config() == true)
		{
			//DB Conifg Load			
			load_config_lib_db(config_filename);
			writeLog(g_script_name, "1. Load configuration - OK", LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname, "1. Initialize(Load the Config) : NG");
			writeLog(g_script_name, "1. Load configuration - NG", LV_ERR);
			exit();
		}

		//---------------------------------------------
		// 2. Apply script active conditions
		//---------------------------------------------
		writeLog(g_script_name, "2. Apply script active condition", LV_INFO);
		if (dpExists(manager_dpname + ".Action.ActiveCondition") == true)
		{
			dpConnect("CB_ChangeActiveCondition", manager_dpname + ".Action.ActiveCondition");
		}
		else
		{
			init_script_active();
		}

		init_user_alarm(manager_dpname);	//Reset user User-defined alarm to OFF

		delay(1);

		//---------------------------------------------
		// 3. PMMode DP Check
		//---------------------------------------------
		if (dpExists(cfg_extend_dp) == true)
		{
			writeLog(g_script_name, "3. Check pmmode extend dp - OK. DP name = " + cfg_extend_dp, LV_INFO);
		}
		else
		{
			writeLog(g_script_name, "3. Check pmmode extend dp - NG. DP name = " + cfg_extend_dp, LV_WARN);
			exit();
		}

		//-----------------------------------------------------------
		// 4. DB connection initialization
		//-----------------------------------------------------------
		if (init_DBConnPool() == true)
		{
			create_DBConnPool();

			writeLog(g_script_name, "4. DB connection initialization - OK", LV_INFO);

			// DB ������ Queue ����� ����� ��쿡�� �ּ� ��Ȱ��ȭ 
			// Queue ��� ���� ���� ���п� ���� ����ó���� �����
			// ����� ���� ���� �� ����� ���� �޴� ������� �ڵ��Ǿ� ����
			/*
			thread_id = startThread("queryQueue_manager", true);
			if (thread_id == RTN_VALUE_ERROR)
			{
			writeLog(g_script_name, "4-1. Thread start - NG. function = queryQueue_manager", LV_ERR);
			exit();
			}
			else
			{
			writeLog(g_script_name, "4-1. Thread start - OK. function = queryQueue_manager, Thread ID = " + thread_id, LV_INFO);
			}
			*/
		}
		else
		{
			writeLog(g_script_name, "4. DB connection initialization - NG", LV_ERR);
			exit();
		}

		//-----------------------------------------------------------
		// 5. Thread Start
		//-----------------------------------------------------------
		// pmmode�� ���� ���� ���� ������
		thread_id = startThread("check_pmmode_start_reservation");
		if (thread_id == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "5. Thread start - NG. Function = check_pmmode_start_reservation", LV_ERR);
			exit();
		}
		else
		{
			writeLog(g_script_name, "5. Thread start - OK. Function = check_pmmode_start_reservation, Thread ID = " + thread_id, LV_INFO);
		}

		// pmmode ���� 10���� �˸� ���� ������
		thread_id = startThread("check_pmmode_end_notify");
		if (thread_id == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "6. Thread start - NG. Function = check_pmmode_end_notify", LV_ERR);
			exit();
		}
		else
		{
			writeLog(g_script_name, "6. Thread start - OK. Function = check_pmmode_end_notify, Thread ID = " + thread_id, LV_INFO);
		}

		// pmmode ���� ���� ������
		thread_id = startThread("check_pmmode_end_overtime");
		if (thread_id == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "7. Thread start - NG. Function = check_pmmode_end_overtime", LV_ERR);
			exit();
		}
		else
		{
			writeLog(g_script_name, "7. Thread start - OK. Function = check_pmmode_end_overtime, Thread ID = " + thread_id, LV_INFO);
		}

		// pmmode�� ���� ���� ���� ������
		thread_id = startThread("check_pmmode_complete");
		if (thread_id == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "8. Thread start - NG. Function = check_pmmode_complete", LV_ERR);
			exit();
		}
		else
		{
			writeLog(g_script_name, "8. Thread start - OK. Function = check_pmmode_complete, Thread ID = " + thread_id, LV_INFO);
		}
    
		// pmmode�� ���� �� ������ ���� ���� ���� ������
		thread_id = startThread("check_pmmode_end_overtime_wait_state");
		if (thread_id == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "9. Thread start - NG. Function = check_pmmode_end_overtime_wait_state", LV_ERR);
			exit();
		}
		else
		{
			writeLog(g_script_name, "9. Thread start - OK. Function = check_pmmode_end_overtime_wait_state, Thread ID = " + thread_id, LV_INFO);
		}

		writeLog(g_script_name, "===== Script initialize complete =====", LV_INFO);
	}
	catch
	{
		update_user_alarm(g_script_name, "Exception of main() : " + getLastException());
	}
}


//*******************************************************************************
// name         : loadConfig()
// argument     :
// return value : bool
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : Script config initialize
//*******************************************************************************
bool load_config()
{
	bool is_result = true;
	string config_path;

	// Config Temp Variable
	int tmp_delay_check_pmmode_sec, tmp_pmmode_end_notify_time_min, tmp_block_size;
	string tmp_extend_dp, tmp_pmmode_dp, tmp_approval_code, tmp_reject_code, tmp_wait_code, tmp_user_id;
	string tmp_script_active_condition;

	try
	{
		//-----------------------------------------------------------
		// 1. load config File Name from Manager DP
		//-----------------------------------------------------------
		if(globalExists("global_config_name") == TRUE)
			config_filename = global_config_name;
			
		//-----------------------------------------------------------
		// 2. load script Path
		//-----------------------------------------------------------
		config_path = getPath(SCRIPTS_REL_PATH) + config_filename;
		writeLog(g_script_name, "loadConfig() - config file path = " + config_path, LV_DBG2);

		//-----------------------------------------------------------
		// 3. read by section
		//-----------------------------------------------------------
		// [general] section read
		// ��ũ��Ʈ ���� ���
		if (paCfgReadValue(config_path, "general", "ACTIVE_CONDITION", tmp_script_active_condition) != 0)
		{
			writeLog(g_script_name, "Failed to load : [general] ACTIVE_CONDITION. Set to default value to " + ScriptActive_Condition, LV_WARN);
		}
		else
		{
			ScriptActive_Condition = tmp_script_active_condition;
		}

		// pmmode db�� �ֱ������� Ȯ���ϱ� ���� ��
		if (paCfgReadValue(config_path, "general", "DELAY_CHECK_PMMODE_SEC", tmp_delay_check_pmmode_sec) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] DELAY_CHECK_PMMODE_SEC. Set to default value to " + cfg_delay_check_pmmode_sec, LV_WARN);
		}
		else
		{
			cfg_delay_check_pmmode_sec = tmp_delay_check_pmmode_sec;
		}
				
		// pmmode ���� & ���� db�� �ֱ������� Ȯ���ϱ� ���� ��
		if (paCfgReadValue(config_path, "general", "DELAY_CHECK_PMMODE_START_END_SEC", tmp_delay_check_pmmode_sec) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] DELAY_CHECK_PMMODE_START_END_SEC. Set to default value to " + cfg_delay_check_pmmode_start_end_sec, LV_WARN);
		}
		else
		{
			cfg_delay_check_pmmode_start_end_sec = tmp_delay_check_pmmode_sec;
		}

		// pmmode ���� �˸� �ð� (��)
		if (paCfgReadValue(config_path, "general", "PMMODE_END_NOTIFY_TIME_MIN", tmp_pmmode_end_notify_time_min) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] PMMODE_END_NOTIFY_TIME_MIN. Set to default value to " + cfg_pmmode_end_notify_time_min, LV_WARN);
		}
		else
		{
			cfg_pmmode_end_notify_time_min = tmp_pmmode_end_notify_time_min;
		}

		// dp ���濡 ���� EM ���� ���Ҹ� ���� delay�� �� �±� ����
		if (paCfgReadValue(config_path, "general", "BLOCK_SIZE", tmp_block_size) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] BLOCK_SIZE. Set to default value to " + cfg_block_size, LV_WARN);
		}
		else
		{
			cfg_block_size = tmp_block_size;
		}

		// pmmode ���� Ȯ���� �˷��� Ʈ���� dp
		if (paCfgReadValue(config_path, "general", "EXTEND_DP", tmp_extend_dp) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] EXTEND_DP. Set to default value to " + cfg_extend_dp, LV_WARN);
		}
		else
		{
			cfg_extend_dp = tmp_extend_dp;
		}

		// pmmode �±��� pmmode dp type
		if (paCfgReadValue(config_path, "general", "PMMODE_DP", tmp_pmmode_dp) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] PMMODE_DP. Set to default value to " + cfg_pmmode_dp, LV_WARN);
		}
		else
		{
			cfg_pmmode_dp = tmp_pmmode_dp;
		}

		// ���� ���� �ڵ�
		if (paCfgReadValue(config_path, "general", "APPROVAL_CODE", tmp_approval_code) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] APPROVAL_CODE. Set to default value to " + cfg_approval_code, LV_WARN);
		}
		else
		{
			cfg_approval_code = tmp_approval_code;
		}
    
		// ���� �ݷ� �ڵ�
		if (paCfgReadValue(config_path, "general", "REJECT_CODE", tmp_reject_code) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] REJECT_CODE. Set to default value to " + cfg_reject_code, LV_WARN);
		}
		else
		{
			cfg_reject_code = tmp_reject_code;
		}

		// ���� ��� �ڵ�
		if (paCfgReadValue(config_path, "general", "WAIT_CODE", tmp_wait_code) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] WAIT_CODE. Set to default value to " + cfg_wait_code, LV_WARN);
		}
		else
		{
			cfg_wait_code = tmp_wait_code;
		}
    
		// ��ũ��Ʈ���� ������ TH_CM_PM�� SET_CLIENT_NAME, END_CLIENT_NAME�� �� ����
		if (paCfgReadValue(config_path, "general", "USER_ID", tmp_user_id) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] USER_ID. Set to default value to " + cfg_user_id, LV_WARN);
		}
		else
		{
			cfg_user_id = tmp_user_id;
		}
		
		// v1.06 �߰� : ALARM �߻� ���� �÷� ��� ���� 
		if (paCfgReadValue(config_path, "general", "ALRM_EXT_YN", cfg_alrm_ext_yn) == RTN_VALUE_ERROR)
		{
			writeLog(g_script_name, "Failed to load : [general] ALRM_EXT_YN. Set to default value to " + cfg_alrm_ext_yn, LV_DBG1);
		}
		
		// [general] section read
		// [Parent_info]
		if (paCfgReadValue(config_path, "parent_info", "PJT_ID", cfg_pjt_id) != 0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] PJT_ID.", LV_ERR);
			is_result = false;
		}

		string msg = "Configuration Information"
			+ "\n [general]"
			+ "\n ACTIVE_CONDITION = " + ScriptActive_Condition
			+ "\n DELAY_CHECK_PMMODE_SEC = " + cfg_delay_check_pmmode_sec
			+ "\n DELAY_CHECK_PMMODE_START_END_SEC = " + cfg_delay_check_pmmode_start_end_sec
			+ "\n PMMODE_END_NOTIFY_TIME_MIN = " + cfg_pmmode_end_notify_time_min
			+ "\n BLOCK_SIZE = " + cfg_block_size
			+ "\n EXTEND_DP = " + cfg_extend_dp
			+ "\n PMMODE_DP = " + cfg_pmmode_dp
			+ "\n APPROVAL_CODE = " + cfg_approval_code
			+ "\n REJECT_CODE = " + cfg_reject_code
			+ "\n WAIT_CODE = " + cfg_wait_code
			+ "\n USER_ID = " + cfg_user_id
			+ "\n ALRM_EXT_YN = " + cfg_alrm_ext_yn
			+ "\n [parent_info]"
			+ "\n PJT_ID = " + cfg_pjt_id
			+ "\n [db_con]"
			+ "\n Connection Information = " + DB_CONN_STRING;

		writeLog(g_script_name, msg, LV_INFO);
	}
	catch
	{
		update_user_alarm(g_script_name, "Exception of loadConfig() " + getLastException());
		is_result = false;
	}
	finally
	{
		return is_result;
	}
}


//*******************************************************************************
// name         : check_pmmode_start_reservation
// argument     : 
// return value : 
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : Check PMMode start reservation status periodically in DB
//*******************************************************************************
void check_pmmode_start_reservation()
{
	// ���μ��� ���� ��� �ð� ���� variable
	time tStart, tEnd;
	int totalSecond, totalMilisecond;
	string totalTime;

	// ���� ���� Variable
	string query, set_time;
	dyn_dyn_anytype qry_result;
	int conn_idx, result;

	string pmmode_eqp_no, pmmode_pjt_id, pmmode_eqp_name, pmmode_appr_user_id, pmmode_appr_date, pmmode_req_date, pmmode_req_user_id, pmmode_actn_reason_cont;
	
	bool min_prio_changed;
	dyn_string dsParams, applylist_alert;
	string applylist_name;

	int min_prio;
	int is_alert_config;
	bool is_PMMODE_on;

	while (true)
	{
		try
		{
			// Active ���°� �ƴ� ��� �������� ����
			if (isScriptActive == false)
			{
				delay(cfg_delay_check_pmmode_start_end_sec);
				continue;
			}

			// ��ũ��Ʈ �Ϸ� Flag Off�� ����
			is_complete_check_pmmode_start_reservation = false;

			// ���� �ð� ��������
			tStart = getCurrentTime();

			//-----------------------------------------------------------
			// 1. query
			//-----------------------------------------------------------				
			// PMMode ������ �±װ� �����ϴ��� ����	

			//v1.06 �Լ� �߰� -> get_pmmode_start_query()
			query = get_pmmode_start_query(cfg_alrm_ext_yn);
			
			// binding params
			set_time = formatTime("%Y/%m/%d %H:%M:%S", tStart);
			dynClear(dsParams);
			dsParams = makeDynString(cfg_approval_code, set_time, set_time, cfg_pjt_id);

			// Excute db query
			conn_idx = get_DBConn();
			result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);
			// db conncetion ����
			if (conn_idx > 0)
			{
				if (release_DBConn(conn_idx))
				{
					conn_idx = 0;
				}
			}

			// db ���� ����
			if (result == DB_ERR_NONE)
			{
				writeLog(g_script_name, "check_pmmode_start_reservation() - Select query OK. Count = " + dynlen(qry_result), LV_DBG1);
				writeLog(g_script_name, "check_pmmode_start_reservation() - Select query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);

				// pmmode�� �����ؾ��ϴ� ����� �ִٸ�
				if (dynlen(qry_result) > 0)
				{
					int block_count = 1;
					// Apply pmmode
					for (int i = 1; i <= dynlen(qry_result); i++)
					{
						min_prio_changed = true;
						// EM ���ϰ��Ҹ� ���� ���� �������� delay
						if (block_count++ > cfg_block_size)
						{
							block_count = 1;
							delay(0, 1);
						}

						pmmode_eqp_no = qry_result[i][1];
						pmmode_pjt_id = qry_result[i][2];
						pmmode_eqp_name = qry_result[i][3];
						pmmode_appr_user_id = qry_result[i][4];
						pmmode_appr_date = qry_result[i][5];
						pmmode_req_date = qry_result[i][6];
						pmmode_req_user_id = qry_result[i][7];
						pmmode_actn_reason_cont = qry_result[i][8];
						
						//v1.06 min_prio ���� ���� : Y�� ��� �˶� 
						if(cfg_alrm_ext_yn == 1 && qry_result[i][9] == 'Y')
						{
							min_prio_changed = false; // min_prio ���� ���� ���� ����
						}
						else
						{
							min_prio_changed = true;
						}
						
						
						if (dpExists(pmmode_pjt_id + pmmode_eqp_name))
						{
							// pmmonde flag default setting
							is_PMMODE_on = true;

							//1. min_prio ���� : pmmode�� ������ dp�� ������ �����Ѵٸ� 
							// alert dpe�� �����ϴ��� ����Ʈ ��ȸ
							if(min_prio_changed == true)
							{
								applylist_alert = dpNames(pmmode_pjt_id + pmmode_eqp_name + ".alert.*");

								// alert dpe�� �����Ѵٸ�
								if (dynlen(applylist_alert) > 0)
								{
									// alert dpe�� ��ȸ�ϸ鼭 _alert_hdl.._min_prio ���� ����
									for (int j = 1; j <= dynlen(applylist_alert); j++)
									{
										applylist_name = applylist_alert[j] + ":_alert_hdl.._min_prio";
					  
										// _alert_hdl dpe (config)�� �����Ѵٸ�
										dpGet(applylist_alert[j] + ":_alert_hdl.._type", is_alert_config);
										if(is_alert_config != DPCONFIG_NONE)  
										{
											min_prio = -1;

											// min prio ���� ������
											dpGet(applylist_name, min_prio);
											
											// pmmode ���°� �ƴϰų� CCO ���� �� ���
											//v1.06 min_prio ���� ���� : min_prio_changed == true�� ���¿��� min_prio ����
											if ( min_prio == 0 || min_prio == 50 )
											{
												// ������ min prio ���� +100�� ������
												int rtchk = dpSetTimedWait(0, applylist_name, min_prio + 100);

												// dpSetTimeWait�� �����Ͽ��� ���
												if (rtchk == RTN_VALUE_ERROR)
												{
													string applylist_name_rb;
													dyn_errClass err = getLastError();
													if (dynlen(err) > 0)
													{
														writeLog(g_script_name, "check_pmmode_start_reservation() - min prio dpSetTimed error. DP = " + applylist_name + ", Value : " + (min_prio + 100), LV_ERR);
													}

													// _min_prio Rollback
													for (int rb = 1; rb <= j; rb++)
													{
														applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";

														dpSetTimedWait(0, applylist_name_rb, min_prio);
													}
													is_PMMODE_on = false;
													break;
												}
											}
											// �̹� pmmode �����̶��
											else if (min_prio == 100 || min_prio == 150)
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - min prio value is already pmmode. DP = " + applylist_name + ", Value = " + min_prio, LV_ERR);
											}
											// min_prio �� ����ó�� (�̷� Case�� �������� ����)
											else
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - min prio value is range error. DP = " + applylist_name + ", Value = " + min_prio, LV_ERR);
												is_PMMODE_on = false;
												break;
											}
										}
									}
								}
							}
							
							// pmmode�� min prio �� ������ ���������� ����Ǿ��ٸ� 
							if (is_PMMODE_on)
							{
								// pmmode dpe�� �����Ѵٸ�
								if (dpExists(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp))
								{
									// pmmode ���� ������
									bool pmmode = false;
									dpGet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, pmmode);


									//2. PMMODE �Ķ���� ����
									// pmmode�� ����Ǿ� ���� �ʴٸ�
									if (pmmode == false)
									{
										// pmmode dp�� set ��Ŵ
										int rtchk = dpSetWait(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, true);

										// dpset�� �����Ͽ��ٸ�
										if (rtchk == RTN_VALUE_ERROR)
										{
											string applylist_name_rb;
											dyn_errClass err = getLastError();
											if (dynlen(err) > 0)
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - dpSet failed. DP = " + pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp + ", Value = true", LV_ERR);
											}

											// _min_prio Rollback
											if(min_prio_changed == true)
											{
												for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
												{
													applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
													dpSetTimedWait(0, applylist_name_rb, min_prio);
												}
											}
											continue;
										}
										
										//3. PMMODE ���� �̷� ���� 
										// v1.08 ���� ���� : APPR_USER_ID �÷� �׸� �߰�
										query = "INSERT /*PMMODE.ctl-20200609-SIT*/ INTO TH_CM_PM( EQP_NO, SET_DATE, ACTN_REASON_CONT, SET_USER_ID, SET_CLIENT_NAME, REQ_USER_ID, APPR_DATE, REQ_DATE, APPR_USER_ID )"
											+ " VALUES(:child_eqp, TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS'), :reason, :set_user, :set_client, :req_user, TO_DATE(:appr_date, 'YYYY.MM.DD HH24:MI:SS'), TO_DATE(:req_date, 'YYYY.MM.DD HH24:MI:SS'), :appr_user_id)";

										// binding params
										dynClear(dsParams);
										dsParams = makeDynString(pmmode_eqp_no, set_time, pmmode_actn_reason_cont, pmmode_appr_user_id, cfg_user_id, pmmode_req_user_id, pmmode_appr_date, pmmode_req_date, pmmode_appr_user_id);

										conn_idx = get_DBConn();
										// pmmode �̷� ���̺� ���� ����
										result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
										// db conncetion ����
										if (conn_idx > 0)
										{
											if (release_DBConn(conn_idx))
											{
												conn_idx = 0;
											}
										}

										// insert ���� ��
										if (result == DB_ERR_NONE)
										{
											writeLog(g_script_name, "check_pmmode_start_reservation() - Insert query OK.", LV_DBG1);
											writeLog(g_script_name, "check_pmmode_start_reservation() - Insert query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
										}
										// insert ���� ��
										else
										{
											// _min_prio Rollback
											string applylist_name_rb;
											if(min_prio_changed == true)
											{
												for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
												{
													applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
													dpSetTimed(0, applylist_name_rb, min_prio);
													dpSet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, false);
												}
											}
                      
											if (result == DB_ERR_QUERY) // Query Fail
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - Insert query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
											}
											else
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
												create_DBConnPool();
											}

											continue;
										}

										//3. PMMODE ���� ������Ʈ 
										query = "UPDATE /*PMMODE.ctl-20200609-SIT*/ TN_CM_PM_APPR"
											+ " SET PM_START_YN = 'Y',"
											+ " MOD_DATE = TO_DATE(:mod_date, 'YYYY.MM.DD HH24:MI:SS'),"
											+ " MOD_USER_ID = :mod_user_id"
											+ " WHERE EQP_NO = :eqp_no";

										// binding params
										dynClear(dsParams);
										dsParams = makeDynString(set_time, MOD_USER_ID, pmmode_eqp_no);

										conn_idx = get_DBConn();
										// pmmode �̷� ���̺� ���� ����
										result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
										// db conncetion ����
										if (conn_idx > 0)
										{
											if (release_DBConn(conn_idx))
											{
												conn_idx = 0;
											}
										}

										// update ���� ��
										if (result == DB_ERR_NONE)
										{
											writeLog(g_script_name, "check_pmmode_start_reservation() - Update query OK.", LV_DBG1);
											writeLog(g_script_name, "check_pmmode_start_reservation() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
										}
										// update ���� ��
										else
										{
											// _min_prio Rollback
											string applylist_name_rb;
											if(min_prio_changed == true)
											{
												for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
												{
													applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
													dpSetTimed(0, applylist_name_rb, min_prio);
													dpSet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, false);
												}
											}
                      
											if (result == DB_ERR_QUERY) // Query Fail
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - Update query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
											}
											else
											{
												writeLog(g_script_name, "check_pmmode_start_reservation() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
												create_DBConnPool();
											}

											continue;
										}
									}
									else
									{
										writeLog(g_script_name, "check_pmmode_start_reservation() - pmmode value is already pmmode. DP = " + pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp + ", Value = " + pmmode, LV_ERR);
									}
								}
							}
						}
						else
						{
							writeLog(g_script_name, "check_pmmode_start_reservation() - DP is not on the server. DP = " + pmmode_pjt_id + pmmode_eqp_name, LV_ERR);
						}
					}
				}
			}
			else
			{
				if (result == DB_ERR_QUERY) // Query Fail
				{
					writeLog(g_script_name, "check_pmmode_start_reservation() - Select query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
				}
				else
				{
					writeLog(g_script_name, "check_pmmode_start_reservation() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
					create_DBConnPool();
				}
			}
		}
		catch
		{
			update_user_alarm(g_script_name, "check_pmmode_start_reservation() - Exception = " + getLastException());
		}
		finally
		{
			is_complete_check_pmmode_start_reservation = true;

			if (conn_idx > 0)
			{
				if (release_DBConn(conn_idx))
				{
					conn_idx = 0;
				}
			}

			//-----------------------------------------------------------
			// calculate function process time
			//-----------------------------------------------------------
			tEnd = getCurrentTime();
			totalSecond = period(tEnd - tStart);
			totalMilisecond = milliSecond(tEnd - tStart);
			sprintf(totalTime, "%d.%03dsec;", totalSecond, totalMilisecond);
			writeLog(g_script_name, "check_pmmode_start_reservation() - Total process timed = " + totalTime, LV_DBG2);

			delay(cfg_delay_check_pmmode_start_end_sec);
		}
	}
}

//*******************************************************************************
// name         : get_pmmode_start_query
// argument     : 
// return value : 
// date         : 2021-10-22
// developed by : Tech/Ino Group
// brief        : PMMODE ���� ���̺� ��ȸ ���� ���� (ALRM_EXT_YN �÷��� ��ȸ ���ǿ� ���� ������ �ٸ��� ����)
//*******************************************************************************
string get_pmmode_start_query(int alm_ext_yn_flag = 0)
{
	string query;
	
	try
	{
		//v1.06���� ���� �߰� : 
		if(alm_ext_yn_flag == 1)
		{
			//ALRM_EXT_YN �÷��� �߰��� ����
			query = "SELECT /*PMMODE.ctl-20211101-SIT*/ EQP.EQP_NO, EQP.PJT_ID, EQP.EQP_NAME, PM.APPR_USER_ID, TO_CHAR(PM.APPR_DATE, 'YYYY.MM.DD HH24:MI:SS') AS APPR_DATE, TO_CHAR(PM.REQ_DATE, 'YYYY.MM.DD HH24:MI:SS') AS REQ_DATE, PM.REQ_USER_ID, PM.ACTN_REASON_CONT, PM.ALRM_EXT_YN " // v1.06 : PM.ALRM_EXT_YN �߰�
			+ " FROM TN_CM_EQP EQP, "
			+ " (SELECT PM.EQP_NO, PM.APPR_USER_ID, PM.APPR_DATE, PM.REQ_DATE, PM.REQ_USER_ID, PM.ACTN_REASON_CONT , PM.ALRM_EXT_YN" // v1.06 : PM.ALRM_EXT_YN �߰�
			+ " FROM TN_CM_PM_APPR PM"
			+ " WHERE PM.APPR_STATUS_CODE = :cfg_approval_code"					// PM ���� ����
			+ " AND PM.START_DATE <= TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"	// PM ���� �ð��� ���� ����
			+ " AND PM.END_DATE > TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"		// PM ���� �ð��� �����ִ� ����
			+ " AND PM.PM_START_YN = 'N'"										// PM �̽��� ����
			+ " AND PM.PM_END_YN = 'N') PM"										// PM ������ ����
			+ " WHERE PM.EQP_NO = EQP.EQP_NO"
			+ " AND EQP.PJT_ID =  :cfg_pjt_id";
			
		}
		else
		{
			query = "SELECT /*PMMODE.ctl-20200609-SIT*/ EQP.EQP_NO, EQP.PJT_ID, EQP.EQP_NAME, PM.APPR_USER_ID, TO_CHAR(PM.APPR_DATE, 'YYYY.MM.DD HH24:MI:SS') AS APPR_DATE, TO_CHAR(PM.REQ_DATE, 'YYYY.MM.DD HH24:MI:SS') AS REQ_DATE, PM.REQ_USER_ID, PM.ACTN_REASON_CONT "
			+ " FROM TN_CM_EQP EQP, "
			+ " (SELECT PM.EQP_NO, PM.APPR_USER_ID, PM.APPR_DATE, PM.REQ_DATE, PM.REQ_USER_ID, PM.ACTN_REASON_CONT "
			+ " FROM TN_CM_PM_APPR PM"
			+ " WHERE PM.APPR_STATUS_CODE = :cfg_approval_code"					// PM ���� ����
			+ " AND PM.START_DATE <= TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"	// PM ���� �ð��� ���� ����
			+ " AND PM.END_DATE > TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"		// PM ���� �ð��� �����ִ� ����
			+ " AND PM.PM_START_YN = 'N'"										// PM �̽��� ����
			+ " AND PM.PM_END_YN = 'N') PM"										// PM ������ ����
			+ " WHERE PM.EQP_NO = EQP.EQP_NO"
			+ " AND EQP.PJT_ID =  :cfg_pjt_id";
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of is_updateQuery(). Error = " + getLastException());
	}
	finally
	{
		return query;
	}
}

//*******************************************************************************
// name         : check_pmmode_end_notify
// argument     : 
// return value : 
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : Check PMMode end notify status periodically in DB
//*******************************************************************************
void check_pmmode_end_notify()
{
	// ���μ��� ���� ��� �ð� ���� variable
	time tStart, tEnd;
	int totalSecond, totalMilisecond;
	string totalTime;

	// ���� ���� Variable
	string query, set_time;

	dyn_dyn_anytype qry_result;
	int conn_idx, result;

	string eqp_no_condition;
	dyn_string pmmode_eqp_no;

	dyn_string dsParams, applylist_alert;
	string applylist_name;

	bool trigger_notify;

	while (true)
	{
		try
		{
			// Active ���°� �ƴ� ��� �������� ����
			if (isScriptActive == false)
			{
				delay(cfg_delay_check_pmmode_sec);
				continue;
			}

			// ��ũ��Ʈ �Ϸ� Flag Off�� ����
			is_complete_check_pmmode_end_notify = false;

			// ���� �ð� ��������
			tStart = getCurrentTime();

			trigger_notify = false;
			// ���� Ʈ���� ���� ������
			dpGet(cfg_extend_dp, trigger_notify);

			// ���� Ʈ���� �̺�Ʈ�� �߻����� �ʾҴٸ�
			if (trigger_notify == false)
			{
				//-----------------------------------------------------------
				// query
				//-----------------------------------------------------------
				query = "SELECT /*PMMODE.ctl-20200609-SIT*/ EQP.EQP_NO"
					+ " FROM TN_CM_EQP EQP, "
					+ " (SELECT PM.EQP_NO"
					+ " FROM TN_CM_PM_APPR PM"
					+ " WHERE PM.APPR_STATUS_CODE = :cfg_approval_code"						// PM ���� ����
					+ " AND PM.END_DATE BETWEEN TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"	// PM ���� �ð��� ���� �ð����� ������ �ð��� ������ ���
					+ " AND TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS') + :cfg_pmmode_end_notify_time_min / (24*60)"
					+ " AND PM.PM_START_YN = 'Y'"											// PM ���� ����
					+ " AND PM.PM_END_YN = 'N'"												// PM ������ ����
					+ " AND PM.PM_EXT_NOTIFY_YN = 'N') PM"									// PM ������ ����
					+ " WHERE PM.EQP_NO = EQP.EQP_NO"
					+ " AND EQP.PJT_ID =  :cfg_pjt_id";

				// binding params
				set_time = formatTime("%Y/%m/%d %H:%M:%S", tStart);
				dynClear(dsParams);
				dsParams = makeDynString(cfg_approval_code, set_time, set_time, cfg_pmmode_end_notify_time_min, cfg_pjt_id);

				// Excute db query
				conn_idx = get_DBConn();
				result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);
				if (conn_idx > 0)
				{
					if (release_DBConn(conn_idx))
					{
						conn_idx = 0;
					}
				}

				// PMMODE ���� ���� �ð��� �����ð� �̳� ��ȸ (���� �ð� : 30��)
				if (result == DB_ERR_NONE)
				{
					writeLog(g_script_name, "check_pmmode_end_notify() - Query OK. Count = " + dynlen(qry_result), LV_DBG1);
					writeLog(g_script_name, "check_pmmode_end_notify() - Query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);

					// ������ �ð��ȿ� ���ᰡ �Ǵ� pmmode�� ������ ���
					if (dynlen(qry_result) > 0)
					{
						dynClear(pmmode_eqp_no);

						for (int i = 1; i <= dynlen(qry_result); i++)
						{
							dynAppend(pmmode_eqp_no, qry_result[i][1]);
						}

						int rtchk = dpSet(cfg_extend_dp, true);

						// dpSet�� �����Ͽ��� ���
						if (rtchk == RTN_VALUE_ERROR)
						{
							string applylist_name_rb;
							dyn_errClass err = getLastError();
							if (dynlen(err) > 0)
							{
								writeLog(g_script_name, "check_pmmode_end_notify() - dpSet failed. DP = " + cfg_extend_dp + ", Value : true", LV_ERR);
							}
						}
						else	// ���� �˸� dpSet ���� ��
						{
							
							// eqp_no_condition = get_eqp_no_condition(pmmode_eqp_no);
							query = "UPDATE /*PMMODE.ctl-20210513-SIT*/ TN_CM_PM_APPR"
								+ " SET PM_EXT_NOTIFY_YN = 'Y',"
								+ " MOD_DATE = TO_DATE(:mod_date, 'YYYY.MM.DD HH24:MI:SS'),"
								+ " MOD_USER_ID = :mod_user_id"
								+ " WHERE EQP_NO IN (" + EQP_NO_CONDITION + ")";
							
							dynClear(dsParams);
							dynAppend(dsParams, set_time);
							dynAppend(dsParams, MOD_USER_ID);
							if(is_updateQuery(query, dsParams, pmmode_eqp_no) == true)
							{
								writeLog(g_script_name, "check_pmmode_end_notify() - Update query OK.", LV_DBG1);
								// writeLog(g_script_name, "check_pmmode_end_notify() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
							}
							else
							{
								writeLog(g_script_name, "check_pmmode_end_notify() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
								create_DBConnPool();
							}

						}
					}
				}
				else
				{
					if (result == DB_ERR_QUERY) // Query Fail
					{
						writeLog(g_script_name, "check_pmmode_end_notify() - Select query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
					}
					else
					{
						writeLog(g_script_name, "check_pmmode_end_notify() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
						create_DBConnPool();
					}
				}
			}
		}
		catch
		{
			update_user_alarm(g_script_name, "check_pmmode_end_notify() - Exception = " + getLastException());
		}
		finally
		{
			is_complete_check_pmmode_end_notify = true;

			//-----------------------------------------------------------
			// calculate function process time
			//-----------------------------------------------------------
			tEnd = getCurrentTime();
			totalSecond = period(tEnd - tStart);
			totalMilisecond = milliSecond(tEnd - tStart);
			sprintf(totalTime, "%d.%03dsec;", totalSecond, totalMilisecond);
			writeLog(g_script_name, "check_pmmode_end_notify() - Total process timed = " + totalTime, LV_DBG2);

			delay(cfg_delay_check_pmmode_sec);
		}
	}
}


//*******************************************************************************
// name         : check_pmmode_end_overtime
// argument     : 
// return value : 
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : PMMODE �ڵ� ���� : Check PMMode end overtime status periodically in DB
//*******************************************************************************
void check_pmmode_end_overtime()
{
	// ���μ��� ���� ��� �ð� ���� variable
	time tStart, tEnd;
	int totalSecond, totalMilisecond;
	string totalTime;;

	// ���� ���� Variable
	string query, set_time;

	dyn_dyn_anytype qry_result;
	int conn_idx, result;

	string pmmode_eqp_no, pmmode_pjt_id, pmmode_eqp_name, pmmode_appr_user_id;

	dyn_string dsParams, applylist_alert;
	string applylist_name;

	int min_prio;
	int is_alert_config;
	bool is_pmmode_off;

	while (true)
	{
		try
		{
			// Active ���°� �ƴ� ��� �������� ����
			if (isScriptActive == false)
			{
				delay(cfg_delay_check_pmmode_start_end_sec);
				continue;
			}

			// ��ũ��Ʈ �Ϸ� Flag Off�� ����
			is_complete_check_pmmode_end_overtime = false;

			// ���� �ð� ��������
			tStart = getCurrentTime();

			//-----------------------------------------------------------
			// 1. query
			//-----------------------------------------------------------		
			query = "SELECT /*PMMODE.ctl-20200609-SIT*/ EQP.EQP_NO, EQP.PJT_ID, EQP.EQP_NAME, PM.APPR_USER_ID"
				+ " FROM TN_CM_EQP EQP, "
				+ " (SELECT PM.EQP_NO, PM.APPR_USER_ID"
				+ " FROM TN_CM_PM_APPR PM"
				+ " WHERE PM.APPR_STATUS_CODE = :cfg_approval_code"			// PM ���� ����
				+ " AND PM.END_DATE <= TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')"	// PM ���� �ð��� ���� ����
				+ " AND PM.PM_START_YN = 'Y'"						// PM ���� ����
				+ " AND PM.PM_END_YN = 'N') PM"						// PM ������ ����
				+ " WHERE PM.EQP_NO = EQP.EQP_NO"
				+ " AND EQP.PJT_ID =  :cfg_pjt_id";

			// binding params
			set_time = formatTime("%Y/%m/%d %H:%M:%S", tStart);
			dynClear(dsParams);
			dsParams = makeDynString(cfg_approval_code, set_time, cfg_pjt_id);
      
			// Excute db query
			conn_idx = get_DBConn();  
			result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);
			// db conncetion ����
			if (conn_idx > 0)
			{
				if (release_DBConn(conn_idx))
				{
					conn_idx = 0;
				}
			}

			// db ���� ����
			if (result == DB_ERR_NONE)
			{
				writeLog(g_script_name, "check_pmmode_end_overtime() - Query OK. Count = " + dynlen(qry_result), LV_DBG1);
				writeLog(g_script_name, "check_pmmode_end_overtime() - Query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);

				// pmmode�� �����ؾ��ϴ� ����� �ִٸ�
				if (dynlen(qry_result) > 0)
				{
					int block_count = 1;
					// Apply pmmode
					for (int i = 1; i <= dynlen(qry_result); i++)
					{
						// EM ���ϰ��Ҹ� ���� ���� �������� delay
						if (block_count++ > cfg_block_size)
						{
							block_count = 1;
							delay(0, 1);
						}

						pmmode_eqp_no = qry_result[i][1];
						pmmode_pjt_id = qry_result[i][2];
						pmmode_eqp_name = qry_result[i][3];
						pmmode_appr_user_id = qry_result[i][4];
						
						// pmmode�� ������ dp�� ������ �����Ѵٸ�
						if (dpExists(pmmode_pjt_id + pmmode_eqp_name))
						{
							// pmmonde flag default setting
							is_pmmode_off = true;

							// alert dpe�� �����ϴ��� ����Ʈ ��ȸ
							applylist_alert = dpNames(pmmode_pjt_id + pmmode_eqp_name + ".alert.*");

							// alert dpe�� �����Ѵٸ�
							if (dynlen(applylist_alert) > 0)
							{
								// alert dpe�� ��ȸ�ϸ鼭 _alert_hdl.._min_prio ���� ����
								for (int j = 1; j <= dynlen(applylist_alert); j++)
								{
									applylist_name = applylist_alert[j] + ":_alert_hdl.._min_prio";
                  
									// _alert_hdl dpe (config)�� �����Ѵٸ�
									dpGet(applylist_alert[j] + ":_alert_hdl.._type", is_alert_config);
									
									if(is_alert_config != DPCONFIG_NONE) 
									{
										min_prio = -1;

										// min prio ���� ������
										dpGet(applylist_name, min_prio);

										// pmmode ���°� �ƴϰų� CCO ���� �� ���
										if (min_prio == 0 || min_prio == 50)
										{
											if(cfg_alrm_ext_yn == 1)		//ALRM_EXT_YN �÷��� ��� ��� DBG�� ���
												writeLog(g_script_name, "check_pmmode_end_overtime() - min prio value is already non pmmode. DP = " + applylist_name + ", Value = " + min_prio, LV_INFO);
											else
												writeLog(g_script_name, "check_pmmode_end_overtime() - min prio value is already non pmmode. DP = " + applylist_name + ", Value = " + min_prio, LV_ERR);
										}
										// pmmode ���¶��
										else if (min_prio == 100 || min_prio == 150)
										{
											// ������ min prio ���� -100�� ������
											int rtchk = dpSetTimedWait(0, applylist_name, min_prio - 100);

											// dpSetTimeWait�� �����Ͽ��� ���
											if (rtchk == RTN_VALUE_ERROR)
											{
												string applylist_name_rb;
												dyn_errClass err = getLastError();
												
												if (dynlen(err) > 0)
												{
													writeLog(g_script_name, "check_pmmode_end_overtime() - min prio dpSetTimed failed. DP = " + applylist_name + ", Value : " + (min_prio - 100), LV_ERR);
												}

												// _min_prio Rollback
												for (int rb = 1; rb <= j; rb++)
												{
													applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";

													dpSetTimedWait(0, applylist_name_rb, min_prio);
												}
												
												is_pmmode_off = false;
												break;
											}
										}
										// min_prio �� ����ó�� (�̷� Case�� �������� ����)
										else
										{
											writeLog(g_script_name, "check_pmmode_end_overtime() - min prio value is range error. DP =  " + applylist_name + ", Value : " + min_prio, LV_ERR);
											is_pmmode_off = false;
											break;
										}
									}
								}
							}

							// pmmode�� min prio �� ������ ���������� ����Ǿ��ٸ� 
							if (is_pmmode_off)
							{
								// pmmode dpe�� �����Ѵٸ�
								if (dpExists(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp))
								{
									bool pmmode = false;
									// pmmode ���� ������
									dpGet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, pmmode);

									// pmmode�� ����Ǿ� �ִٸ�
									if (pmmode == true)
									{
										// pmmode dp�� reset ��Ŵ
										int rtchk = dpSetWait(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, false);

										// dpset�� �����Ͽ��ٸ�
										if (rtchk == RTN_VALUE_ERROR)
										{
											string applylist_name_rb;
											dyn_errClass err = getLastError();
											if (dynlen(err) > 0)
											{
												writeLog(g_script_name, "check_pmmode_end_overtime() - dpSet failed. DP =  " + pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp + ", Value = false", LV_ERR);
											}

											// _min_prio Rollback
											for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
											{
												applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
												dpSetTimedWait(0, applylist_name_rb, min_prio);
											}
											continue;
										}
									}
									else
									{
										// ������ DB�� �����Ͱ� ��ġ���� ����                    
										writeLog(g_script_name, "check_pmmode_end_overtime() - pmmode value is already non pmmode. DP = " + pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp + ", Value = " + pmmode, LV_ERR);
									}
           
									// PMMODE ���� �� �Ǵ� ������ DB�� �����Ͱ� ��ġ���� ���� ��� ������ �����ϰ� DB ������ update                  
									query = "UPDATE /*PMMODE.ctl-20200609-SIT*/ TH_CM_PM"
										+ " SET END_DATE = TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS'),"
										+ " END_USER_ID = :end_user,"
										+ " END_CLIENT_NAME = :end_client"
										+ " WHERE END_DATE IS NULL"
										+ " AND EQP_NO = :child_eqp";

									// binding params
									dynClear(dsParams);
									dsParams = makeDynString(set_time, pmmode_appr_user_id, cfg_user_id, pmmode_eqp_no);

									conn_idx = get_DBConn();
									// pmmode �̷� ���̺� ���� ����
									result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
									// db conncetion ����
									if (conn_idx > 0)
									{
										if (release_DBConn(conn_idx))
										{
											conn_idx = 0;
										}
									}

									// update ���� ��
									if (result == DB_ERR_NONE)
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK.", LV_DBG1);
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
									}
									// update ���� ��
									else
									{

										// _min_prio Rollback
										string applylist_name_rb;

										for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
										{
											applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
											dpSetTimed(0, applylist_name_rb, min_prio);
											dpSet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, true);
										}
									
										if (result == DB_ERR_QUERY) // Query Fail
										{	
											writeLog(g_script_name, "check_pmmode_end_overtime() - Update query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
										}
										else
										{
											writeLog(g_script_name, "check_pmmode_end_overtime() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
											create_DBConnPool();
										}
										continue;
									}
								  
									query = "UPDATE /*PMMODE.ctl-20200609-SIT*/ TN_CM_PM_APPR"
									+ " SET PM_START_YN = 'N',"
									+ " PM_END_YN = 'Y',"
									+ " EXT_DATE = NULL,"
									+ " PM_EXT_YN = 'N',"
									+ " MOD_DATE = TO_DATE(:mod_date, 'YYYY.MM.DD HH24:MI:SS'),"
									+ " MOD_USER_ID = :mod_user_id"
									+ " WHERE EQP_NO = :eqp_no";
                                        					
									// binding params
									dynClear(dsParams);
									dsParams = makeDynString(set_time, MOD_USER_ID, pmmode_eqp_no);

									conn_idx = get_DBConn();
									// pmmode �̷� ���̺� ���� ����
									result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
									// db conncetion ����
									if (conn_idx > 0)
									{
										if (release_DBConn(conn_idx))
										{
											conn_idx = 0;
										}
									}

									// update ���� ��
									if (result == DB_ERR_NONE)
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK.", LV_DBG1);
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
									}
									// update ���� ��
									else
									{
										// _min_prio Rollback
										string applylist_name_rb;

										for (int rb = 1; rb <= dynlen(applylist_alert); rb++)
										{
											applylist_name_rb = applylist_alert[rb] + ":_alert_hdl.._min_prio";
											dpSetTimed(0, applylist_name_rb, min_prio);
											dpSet(pmmode_pjt_id + pmmode_eqp_name + cfg_pmmode_dp, true);
										}
                    
										if (result == DB_ERR_QUERY) // Query Fail
										{
											writeLog(g_script_name, "check_pmmode_end_overtime() - Update query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
										}
										else
										{
											writeLog(g_script_name, "check_pmmode_end_overtime() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
											create_DBConnPool();
										}
                    
										continue;
									}                  
								}
							}
						}
						else
						{
							writeLog(g_script_name, "check_pmmode_end_overtime() - DP is not on the server. DP = " + pmmode_pjt_id + pmmode_eqp_name, LV_ERR);

							//PMMODE ���� �� �������� TAG ������ ��� ����ó�� (v1.08 ����)
							//1. TN_CM_PM_APPR ���̺� PM ���� ������Ʈ
							query = "UPDATE /*PMMODE.ctl-20230217-HanwhaConvergence*/ TN_CM_PM_APPR"
							+ " SET PM_START_YN = 'N',"
							+ " PM_END_YN = 'Y',"
							+ " EXT_DATE = NULL,"
							+ " PM_EXT_YN = 'N',"
							+ " MOD_DATE = TO_DATE(:mod_date, 'YYYY.MM.DD HH24:MI:SS'),"
							+ " MOD_USER_ID = :mod_user_id"
							+ " WHERE EQP_NO = :eqp_no";
													
							// binding params
							dynClear(dsParams);
							dsParams = makeDynString(set_time, MOD_USER_ID, pmmode_eqp_no);

							conn_idx = get_DBConn();
							// pmmode �̷� ���̺� ���� ����
							result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
							
							// update ���� ��
							if (result == DB_ERR_NONE)
							{
								writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK.", LV_DBG1);
								writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
							}
							else
							{
									if (result == DB_ERR_QUERY) // Query Fail
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
									}
									else
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
										create_DBConnPool();
									}
							}
							
							//2. TH_CM_PM ���̺� PM ���� ������Ʈ
							query = "UPDATE /*PMMODE.ctl-20230217-HanwhaConvergence*/ TH_CM_PM"
								+ " SET END_DATE = TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS'),"
								+ " END_USER_ID = :end_user,"
								+ " END_CLIENT_NAME = :end_client"
								+ " WHERE END_DATE IS NULL"
								+ " AND EQP_NO = :child_eqp";

							// binding params
							dynClear(dsParams);
							dsParams = makeDynString(set_time, pmmode_appr_user_id, cfg_user_id, pmmode_eqp_no);
							
							conn_idx = get_DBConn();
							// pmmode �̷� ���̺� ���� ����
							result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams);
							
							// update ���� ��
							if (result == DB_ERR_NONE)
							{
								writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK.", LV_DBG1);
								writeLog(g_script_name, "check_pmmode_end_overtime() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
							}
							else
							{
									if (result == DB_ERR_QUERY) // Query Fail
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - Update query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
									}
									else
									{
										writeLog(g_script_name, "check_pmmode_end_overtime() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
										create_DBConnPool();
									}
							}

							// db conncetion ����
							if (conn_idx > 0)
							{
								if (release_DBConn(conn_idx))
								{
									conn_idx = 0;
								}
							}
						}
					}
				}
			}
			else
			{
				if (result == DB_ERR_QUERY) // Query Fail
				{
					writeLog(g_script_name, "check_pmmode_end_overtime() - Select query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
				}
				else
				{
					writeLog(g_script_name, "check_pmmode_end_overtime() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
					create_DBConnPool();
				}
			}
		}
		catch
		{
			update_user_alarm(g_script_name, "check_pmmode_end_overtime() - Exception = " + getLastException());
		}
		finally
		{
			is_complete_check_pmmode_end_overtime = true;

			if (conn_idx > 0)
			{
				if (release_DBConn(conn_idx))
				{
					conn_idx = 0;
				}
			}

			//-----------------------------------------------------------
			// calculate function process time
			//-----------------------------------------------------------
			tEnd = getCurrentTime();
			totalSecond = period(tEnd - tStart);
			totalMilisecond = milliSecond(tEnd - tStart);
			sprintf(totalTime, "%d.%03dsec;", totalSecond, totalMilisecond);
			writeLog(g_script_name, "check_pmmode_end_overtime() - Total process timed = " + totalTime, LV_DBG2);

			delay(cfg_delay_check_pmmode_start_end_sec);
		}
	}
}


//*******************************************************************************
// name         : check_pmmode_end_overtime_wait_state
// argument     : 
// return value : 
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : PMMDOE ���� ��� ���� ���� : Check PMMode end overtime (wait state) periodically in DB
//*******************************************************************************
void check_pmmode_end_overtime_wait_state()
{
	// ���μ��� ���� ��� �ð� ���� variable
	time tStart, tEnd;
	int totalSecond, totalMilisecond;
	string totalTime;;

	// ���� ���� Variable
	string query, set_time;

	dyn_dyn_anytype qry_result;
	int conn_idx, result;

	dyn_string dsParams;  

	string eqp_no_condition;
	dyn_string pmmode_eqp_no;  
  
  

	while (true)
	{
		try
		{
			// Active ���°� �ƴ� ��� �������� ����
			if (isScriptActive == false)
			{
				delay(cfg_delay_check_pmmode_sec);
				continue;
			}

			// ��ũ��Ʈ �Ϸ� Flag Off�� ����
			is_complete_check_pmmode_end_overtime_wait_state = false;

			// ���� �ð� ��������
			tStart = getCurrentTime();

			//-----------------------------------------------------------
			// 1. query
			//-----------------------------------------------------------		
			query = "SELECT /*PMMODE.ctl-20200715-SIT*/ EQP.EQP_NO"
				+ " FROM TN_CM_EQP EQP, "        
				+ " (SELECT PM.EQP_NO"
				+ " FROM TN_CM_PM_APPR PM"
				+ " WHERE PM.APPR_STATUS_CODE = :cfg_wait_code"						// PM ���� ����
				+ " AND PM.END_DATE <= TO_DATE(:time, 'YYYY.MM.DD HH24:MI:SS')) PM"	// PM ���� �ð��� ���� ����
 				+ " WHERE PM.EQP_NO = EQP.EQP_NO"
				+ " AND EQP.PJT_ID =  :cfg_pjt_id";       

			// binding params
			set_time = formatTime("%Y/%m/%d %H:%M:%S", tStart);
			dynClear(dsParams);
			dsParams = makeDynString(cfg_wait_code, set_time, cfg_pjt_id);

			// Excute db query
			conn_idx = get_DBConn();
			result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);
			// db conncetion ����
			if (conn_idx > 0)
			{
				if (release_DBConn(conn_idx))
				{
					conn_idx = 0;
				}
			}

			// db ���� ����
			if (result == DB_ERR_NONE)
			{
				writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Query OK. Count = " + dynlen(qry_result), LV_DBG1);
				writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);

				// ���� ���¸� �����ؾ� �ϴ� pmmode�� ������ ���
				if (dynlen(qry_result) > 0)
				{
					dynClear(pmmode_eqp_no);
          
					for (int i = 1; i <= dynlen(qry_result); i++)
					{
						dynAppend(pmmode_eqp_no, qry_result[i][1]);
					}
					
					//eqp_no_condition = get_eqp_no_condition(pmmode_eqp_no);
					query = "UPDATE /*PMMODE.ctl-20200715-SIT*/ TN_CM_PM_APPR"
							+ " SET APPR_STATUS_CODE = :cfg_reject_code,"
							+ " MOD_DATE = TO_DATE(:mod_date, 'YYYY.MM.DD HH24:MI:SS'),"
							+ " MOD_USER_ID = :mod_user_id"
							+ " WHERE EQP_NO IN (" + EQP_NO_CONDITION + ")";
          
					// binding params
					dynClear(dsParams);
					dynAppend(dsParams, cfg_reject_code);
					dynAppend(dsParams, set_time);
					dynAppend(dsParams, MOD_USER_ID);
					
					if(is_updateQuery(query, dsParams, pmmode_eqp_no) == true)
					{
						writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Update query OK.", LV_DBG1);
						writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Update query OK. Query = " + query + ", Params = " + dsParams, LV_DBG2);
					}
					else
					{
						writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
						create_DBConnPool();
					}
				}
			}
			else
			{
				if (result == DB_ERR_QUERY) // Query Fail
				{
					writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Select query NG. Query = " + query + ", Params = " + dsParams, LV_ERR);
				}
				else
				{
					writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - DB Connection Error. Query = " + query + ", Params = " + dsParams, LV_ERR);
					create_DBConnPool();
				}
			}
		}
		catch
		{
			update_user_alarm(g_script_name, "check_pmmode_end_overtime_wait_state() - Exception = " + getLastException());
		}
		finally
		{
			is_complete_check_pmmode_end_overtime_wait_state = true;

			//-----------------------------------------------------------
			// calculate function process time
			//-----------------------------------------------------------
			tEnd = getCurrentTime();
			totalSecond = period(tEnd - tStart);
			totalMilisecond = milliSecond(tEnd - tStart);
			sprintf(totalTime, "%d.%03dsec;", totalSecond, totalMilisecond);
			writeLog(g_script_name, "check_pmmode_end_overtime_wait_state() - Total process timed = " + totalTime, LV_DBG2);

			delay(cfg_delay_check_pmmode_sec);
		}
	}
}


//*******************************************************************************
// name         : check_pmmode_complete
// argument     : 
// return value : 
// date         : 2020-06-09
// developed by : Tech/Ino Group (Ryan, Kim)
// brief        : Update heartbeat when pmmode check is complete
//*******************************************************************************
void check_pmmode_complete()
{
	while (true)
	{
		try
		{
			// ��ũ��Ʈ�� Active �����϶����� ����
			while (isScriptActive)
			{
				// pmmode Ȯ���� ��� �Ϸ� �Ǿ��ٸ� heartbeat ������Ʈ
				if (is_complete_check_pmmode_start_reservation && is_complete_check_pmmode_end_notify 
				&& is_complete_check_pmmode_end_overtime && is_complete_check_pmmode_end_overtime_wait_state)
				{
					update_heartbeat(manager_dpname);	//Script Monitoring and Control
					break;
				}

				delay(0, 100);
			}
		}
		catch
		{
			update_user_alarm(g_script_name, "check_pmmode_complete() - Exception = " + getLastException());
		}
		finally
		{
			delay(1);
		}
	}
}


//*******************************************************************************
// name         : get_eqp_no_condition
// argument     : 
// return value : string
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Create where clause
//*******************************************************************************
string get_eqp_no_condition(int eqp_no_count)
{
	const string param = ":eqp_no";
	string query_condition;
	
	try
	{
		//Create where clause condition when there are multiple pjt names in config option
		for (int i = 1; i <= eqp_no_count; i++)
		{
			query_condition += param + i;

			if (i != eqp_no_count)
			{
				query_condition += ", ";
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_eqp_no_condition(). Error = " + getLastException());
	}
	finally
	{
		return query_condition;
	}
}


//*******************************************************************************
// name         : is_updateQuery
// argument     : update_query, in_params(���ε� ������), eqp_no_list(eqp ��ȣ ����)
// return value : string
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : eqp_no ������ 1,000�� ���� ��� �и��Ͽ� ���� ����
//*******************************************************************************
bool is_updateQuery(string orgin_update_query, const dyn_string& in_params, const dyn_string& eqp_no_list)
{
	bool result = true;
	int eqp_no_count, db_result;
	string update_query, eqp_no_bind;
	dyn_string dsParams, update_eqp_no_list;
	int conn_idx;
	const int MAX_EQP_NO_COUNT = 1000;
	
	try
	{
		dsParams = in_params;
		
		for(int i = 1; i <= dynlen(eqp_no_list); i++)
		{
			dynAppend(dsParams, eqp_no_list[i]);
			eqp_no_count = i % MAX_EQP_NO_COUNT;
			
			//1) 1,000 �� ��� or �������� ��� ����
			if(i == dynlen(eqp_no_list) || eqp_no_count == 0)
			{
				if(eqp_no_count == 0)
					eqp_no_count = MAX_EQP_NO_COUNT;
				
				//2. Update Query ����
				//WHERE EQP_NO IN (" + EQP_NO_CONDITION + ")" -> WHERE EQP_NO IN (:eqp_no1, :eqp_no2, ... )
				update_query = orgin_update_query;
				eqp_no_bind = get_eqp_no_condition(eqp_no_count);
				strreplace(update_query, EQP_NO_CONDITION, eqp_no_bind);
				
				//3. Update Query ����
				conn_idx = get_DBConn();
				db_result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], update_query, dsParams);
				
				// db conncetion ����
				if (conn_idx > 0)
				{
					if (release_DBConn(conn_idx))
					{
						conn_idx = 0;
					}
				}

				// update ���� ��
				if (db_result == DB_ERR_NONE)
				{
					writeLog(g_script_name, "is_updateQuery() - Update query OK.", LV_DBG1);
					writeLog(g_script_name, "is_updateQuery() - Update query OK. Query = " + update_query + ", Params = " + dsParams, LV_DBG2);
				}
				// update ���� ��
				else
				{
					if (db_result == DB_ERR_QUERY) // Query Fail
					{
						writeLog(g_script_name, "is_updateQuery() - Update query NG. Query = " + update_query + ", Params = " + dsParams, LV_ERR);
					}
					else
					{
						writeLog(g_script_name, "is_updateQuery() - DB Connection Error. Query = " + update_query + ", Params = " + dsParams, LV_ERR);
						create_DBConnPool();
					}
				}
				
				dsParams = in_params;
			}	
		}
	}
	catch
	{
		result = false;
		update_user_alarm(manager_dpname, "Exception of is_updateQuery(). Error = " + getLastException());
	}
	finally
	{
		// db conncetion ����
		if (conn_idx > 0)
		{
			if (release_DBConn(conn_idx))
			{
				conn_idx = 0;
			}
		}
		return result;
	}
}
