// **************************************************//
// Alarm Data Insert to Database Server
//
// 2016-04-11, DEV_TEAM
//
// CONTROL MANAGER Registration
// --> AlarmInsert.ctl -lang ko_KR.CP949 => Problems displaying alarm messages in Korean
// **************************************************//

//v1.03 (2016.11.21)-----------------------------------------
//1. set_var_column() function add (dynamic VAR column setting)
//2. CB_AlarmEvent() update (to process dynamic VAR columns)
//3. ack_update() update (error modification)
//4. load_config_AlarmInsert() update (to process VAR configs)
//5. parse_VAR() update (logic modification)
//-----------------------------------------------------------
//v1.04 (2017.01.31)-----------------------------------------
//1. Add item to VAR-Column (PMMODE, ALM_INFO, CATEGORY)
//2. Add option : AlamText_DpeAlias for China Site
//3. Fixed the DB Reconnection Issue & Error Handling
//4. Add DB Query option : executeQuery_Single() + bool USE_BULK_QUERY
//5. Change DB log save path : pjt_path\log\DBLog\
//6. Changed comment language : KOREAN->ENGLISH
//-----------------------------------------------------------
//v1.05 (2017.02.20)-----------------------------------------
//1. Improved Query Option
//   : Bulk or Single Query -> Set the number of queries
//   : Limit the maximum number of query queues(prevent memory issues)
//2. Change rdb library : rdb.ctl -> rdb_STD.ctl
//   : Modify the rdbExecuteBulk() -> Rollback when query fails
//3. Change config-file path : pjt_path\scripts\config\
//4. Delete UPDATE_MISSING_ALM Option
//5. Add DB_CONN Alarm
//-----------------------------------------------------------
//v1.06 (2017.04.04)-----------------------------------------
//1. Add Config for processing DB_CONN Alarm
//   : main() function modified.
//-----------------------------------------------------------
//v1.07 (2017.07.17)-----------------------------------------
//1. Add cfg_query_blocking_time variable
//2. dpQueryConnectSingle() function edited to use "cfg_query_blocking_time"
//-----------------------------------------------------------
//v1.08 (2017.12.04)-----------------------------------------
//1. CB_ALarmEvent() : exclude alm_discrete
//2. executeQuery_Bulk(), executeQuery_Single(), executeQuery_Thread() : edit CHECK_DB_STATE() order
//3. Edit comments
//4. Add delete procedure (Interval : hour)
//-----------------------------------------------------------
//v1.09 (2018.04.02)-----------------------------------------
//1. Delete public function
//-----------------------------------------------------------
//v1.10 (2018.05.24)-----------------------------------------
//1. Added option for alarm ID
//   : Number of digits in parameter ID (dpe)
//-----------------------------------------------------------
//-----------------------------------------------------------
//v1.11 (2018.07.02)-----------------------------------------
//1. Fixed error in query statement: "single quotes" conversion
//-----------------------------------------------------------
//v2.01 (2019.03.20)-----------------------------------------
//1. rdb_STD.ctl Replace : "rdb_STD.ctl" -> "lib_db.ctl"
//2. Only DB Standard Mode
//-----------------------------------------------------------
//v2.02 (2019.04.16)-----------------------------------------
//1. Reconnection add
//2. Cleanup in addition to DB standardized version
//-----------------------------------------------------------
//v2.03 (2019.04.16)-----------------------------------------
//1. Q thread mode or Single connection mode
//-----------------------------------------------------------
//v2.04 (2019.05.15)-----------------------------------------
//1. main, lib file merge -> SvrCommunication_Send_lib file delete
//-----------------------------------------------------------
//v2.05 (2019.05.17)-----------------------------------------
//1. "NON.\" " --> "ALERT_CLS_D.\" " Alarm Level name modify
//-----------------------------------------------------------
//v2.07 (2019.05.24)-----------------------------------------
//1. Add DP control monitoring
//-----------------------------------------------------------
//v2.08 (2019.09.04)-----------------------------------------
//1. Update Query exception while disconnected
//2. Add alarm exclusion setting : cfg_alarm_non_class
//-----------------------------------------------------------
//v2.09 (2020.01.23)-----------------------------------------
//1. PM_YN Log Lever Change (LV_INFO -> LV_DBG1)
//-----------------------------------------------------------
//v2.10 (2020.09.01)-----------------------------------------
//1. Standard renewal
//2. config add : alarm Exception - EXCEPTION_FILTER, EXCEPTION_CLASS
//3. PY_YN config add : ALRM_FIL_YN
//-----------------------------------------------------------
//v2.11 (2021.02.02)-----------------------------------------
//1. description Fixed duplicate handling of single quotes : 'temp -> ''temp (x)  'temp -> 'temp (ok)
//-----------------------------------------------------------
//v2.12(2021.06.30) ------------------------------------------
//1. Add config File name lookup from manager dp
//v2.13(2021.08.04) ------------------------------------------
//1. 알람 Callback 함수 (CB_AlarmEvent)에서 필터링 조건 수정 : "._class" 없는 경우에도 동작 --> Ack(확인), Release(해제) 동작
//v2.14(2021.10.29) ------------------------------------------
//1. 기준 정보 조회(EQP_NO, PARAM_CODE)를 Insert, Update의 쿼리에서 조회하도록 적용 : get_TagInfo() 함수 삭제
//v2.15(2022.01.28) ------------------------------------------
//1. config 파일의 cfg_alarm_non_class 등급 DB 저장 필터링 기능 개선 : Callback 함수에서 필터링 기능 추가
//v2.16(2022.08.12) ------------------------------------------
//1. Alarm 발생시 Spec 정보 연동 기능 추가
//	- init_spec_info, load_spec_info, check_spec_load_time, is_period_time, CB_manager_dp 함수 추가 
//v2.17(2022.09.13) ------------------------------------------
//1. Spec 기준 정보 초기화 조건 수정
//	- Spec 기준 정보 Query 결과 0개인 경우 Log 출력 (v2.16 버전에서 스크립트 종료 --> 로그 출력으로 변경)
//v2.18(2022.10.06) ------------------------------------------
//1. Spec 기준 정보가 없는 경우 DB 저장 조건 수정
//	- ALRM_SPEC_PARAM_CODE -> Null값으로 저장 되도록 수정 (기존 공백(' ')->NULL 저장 변경)
//v2.19(2024.07.01) ------------------------------------------
//1. 알람이 발생시 KTC 타입 변경하는 경우 알람 등급 조회 실패 현상 개선



#uses "CtrlADO"
#uses "dist.ctl"
#uses "library_DB.ctl"
#uses "hosts.ctl"
#uses "CtrlPv2Admin" // need for WinCC OA v3.11

//---------------------------------------------
// configuration path & filename
//---------------------------------------------
string config_filename;

//---------------------------------------------
// general option
//---------------------------------------------
const string g_script_release_version = "v2.19";
const string g_script_release_date = "2024.07.01";
const string g_script_name = "AlarmInsert";
string manager_dpname = "";  			// ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)
string ScriptActive_Condition = "ACTIVE";  //|ACTIVE|BOTH|HOST1|HOST2";
int cfg_query_blocking_time = 500;

//---------------------------------------------
// dpQuery for Alarm Monitoring
//---------------------------------------------
string query_condition = "*.alert.*, *.alert.*.*";
bool cfg_alarm_text_dpe_alias = false;  //Get the Alarm Text from Alam DPE Description(not use _alert_hdl.._text) -> for CHINA M1
bool cfg_alrm_fil_yn = false;
//---------------------------------------------
// IO_INFO
//---------------------------------------------
int cfg_alarm_param_format = 3;


//---------------------------------------------
// VAR1~4 DEFINE
//---------------------------------------------
//mapping map_ALM_TYPE;   //e.g: Key="PVHHALM|PVHIALM|...", Value="HH|HI|.."
//mapping map_ACK_USER;   //e.g: Key="USER", Value="ALM_ACK.userName", Key="CLIENT", Value="ALM_ACK.client"
mapping map_alarm_class;  //e.g: Key="JNL|WARN|...", Value="1|2|.."
string cfg_item_var_pmmode;
string cfg_alarm_ack_client = "A.ALARM_ACK_CLIENT", cfg_alarm_ack_username = "A.ALARM_ACK_USERNAME", cfg_alarm_ack_type = "A.ALARM_ACK_TYPE";
string cfg_alarm_non_class = "ALERT_CLS_D";

//---------------------------------------------
// DB Option
//---------------------------------------------
string TBNAME_DEFAULT = "TH_CM_ALRM";
string TIME_FORMAT = "%Y.%m.%d %H:%M:%S";  //"2016.03.17 22:30:22.279";
string TIME_FORMAT_MS = ".%03d";              //"2016.03.17 22:30:22.279";


//---------------------------------------------
// 알람 Spec 기준 정보 옵션
//---------------------------------------------
bool cfg_use_spec_info = true;		//Spec 설정 연동 적용 여부
int cfg_spec_digit = 3;				//spec 데이터 DB 저장시 소수점 자릿수
string cfg_spec_min = "30m";									//SPEC 기준 정보 조회 시간 간경 : "30m" -> 30분간경, "30s" -> 30초 간격, "1h" -> 1시간 간격
string cfg_manager_dp_para = ".UserDefine.BOOL_01";				//Spec 기준 정보 조회 Triiger Manager DP Parameter

//---------------------------------------------
// DB Connection
//---------------------------------------------
// int dbc;
// dbConnection CONN_INFO;	//dbConnection for select_query

dyn_string exception_dpe_list;	// = makeDynString("*.emergency", "*.alarm", "*.warning", "*S*EL*");
dyn_string exception_dpe_class;

// SPEC 기준 정보 데이터 저장
mapping g_map_spec_info;	//key = "DP TYPE, Alarm Param", value = "Spec Param"
							//ex) key = "A_SIT_AI, PVHHALM", value = ".cmd.PVHH"
time g_mod_max_time;	//Spec 기준 정보 다음 Load 할 시간을 저장(DB 쿼리 결과를 저장 : MOD_DATE)

string g_pjt_id;	//ex) "P1154EM:"



//*******************************************************************************
// name         : main()
// argument     :
// return value :
// date         : 2016-03-21
// script by    : Dev Team
// brief        : RealDataInsert main
//*******************************************************************************
void main()
{
	dyn_errClass err;
	string query;

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
		//----------------------------------
		// 1. Initialize (Load the Config)
		//----------------------------------
		if (load_config() == false)
		{
			update_user_alarm(manager_dpname, "1. Initialize(Load the Config) : NG");
			exit();
		}
		else
		{
			load_config_lib_db(config_filename);	//DB Conifg Load
			writeLog(g_script_name, "1. Initialize(Load the Config) : OK", LV_INFO);
		}

		//---------------------------------------------
		// 2. Apply script active conditions
		//---------------------------------------------
		writeLog(g_script_name, "2. Apply Script Active Condition", LV_INFO);
		if (dpExists(manager_dpname + ".Action.ActiveCondition"))
		{
			dpConnect("CB_ChangeActiveCondition", manager_dpname + ".Action.ActiveCondition");
		}
		else
		{
			init_script_active();
		}

		// Initialize user alarm
		init_user_alarm(manager_dpname);	//Reset user User-defined alarm to OFF

		delay(1);
		
		g_pjt_id = getSystemName();

		//---------------------------------------------
		// 3. DB Connect
		//---------------------------------------------
		if (init_DBConnPool() == true)
		{
			create_DBConnPool();
			int thread_ID;
			thread_ID = startThread("queryQueue_manager", true);
			writeLog(g_script_name, "3. Start DB Query Thread. Thread ID = " + thread_ID, LV_INFO);
		}
		
		//---------------------------------------------
		// 3-2. 알람 SPEC 기준 연동 Logic : SPEC 기준 정보 Load, 일정 시간 SPEC 기준 정보 Load Thread, Spec 기준 정보 Load Trigger
		//---------------------------------------------
		if(cfg_use_spec_info == true)
		{
			if(init_spec_info() == true)
			{
				writeLog(g_script_name, "3-2. Alarm Spec Info Logic works.", LV_INFO);
			}
			else
			{
				update_user_alarm(manager_dpname, "3-2. Alarm Spec Info Logic works - NG.");
				exit();
			}
		}

		//----------------------------------
		// 4. AlarmMonitoring
		//----------------------------------
		query = "SELECT ALERT '_alert_hdl.._came_time','_alert_hdl.._ack_time','_alert_hdl.._gone_time'"
				  + ",'_alert_hdl.._discrete_states','_alert_hdl.._act_range','_alert_hdl.._partner'" ;
		query += " FROM '{" + query_condition + "}'" ;
		query += " WHERE '_alert_hdl.._class' != \"" + getSystemName() + cfg_alarm_non_class + ".\" " ;

		writeLog(g_script_name, "4. Alert DP Callback Query = " + query, LV_INFO);

		if (dpQueryConnectSingle("CB_AlarmEvent", false, "", query, cfg_query_blocking_time) == 0)
		{
			err = getLastError();
			if (dynlen(err) > 0)
			{
				update_user_alarm(manager_dpname, "4. Alert DP Connected : NG --> Exit the script.");
				exit();
			}
			else
			{
				writeLog(g_script_name, "4. Alert DP Connected : OK", LV_INFO);
			}
			writeLog(g_script_name, "AlarmInsert Script - Initialize Complete. ", LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname, "4. Alert DP Connected : NG --> Exit the script.");
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
// name         : load_config
// argument     : (string) section("main" or "other")
// return value : (bool)config value loading success state
// date         : 2016-03-21
// developer    : Dev Team
// brief        : config value Load
//*******************************************************************************
bool load_config()
{
	bool ret = true;
	string config_path;

	int tmp_cfg_alarm_text_dpe_alias, tmp_cfg_query_blocking_time, tmp_cfg_alrm_fil_yn , tmp_cfg_alarm_param_format ;
	int tmp_cfg_use_spec_info;
	string tmp_cfg_alarm_class;

	try
	{
		//load config File Name from Manager DP
		if(globalExists("global_config_name") == TRUE)
			config_filename = global_config_name;
			
		// load script Path
		config_path = getPath(SCRIPTS_REL_PATH) + config_filename;
		writeLog(g_script_name, "load_config() - config file path = " + config_path, LV_INFO);

		//[general] -------------------------------------------------------------------

		if (paCfgReadValue(config_path, "general", "Active_Condition", ScriptActive_Condition) != 0)
		{
			writeLog(g_script_name, "Failed to load : [general] Active_Condition. Set to default value : " + ScriptActive_Condition, LV_WARN);
		}

		if (paCfgReadValue(config_path, "general", "Query_Blocking_Time", tmp_cfg_query_blocking_time) != 0)
		{
			writeLog(g_script_name, "Failed to load : [general] Query_Blocking_Time. Set to default value : " + cfg_query_blocking_time, LV_WARN);
		}
		else
		{
			cfg_query_blocking_time = tmp_cfg_query_blocking_time;
		}


		//[dpquery]
		if (paCfgReadValue(config_path, "dpquery", "FROM", query_condition) != 0)
		{
			writeLog(g_script_name, "Failed to load : [dpquery] FROM. Default value is " + query_condition, LV_WARN);
		}

		if (paCfgReadValue(config_path, "dpquery", "AlamText_DpeAlias", tmp_cfg_alarm_text_dpe_alias) != 0)
		{
			writeLog(g_script_name, "Failed to load : [dpquery]AlamText_DpeAlias. Default value is " + cfg_alarm_text_dpe_alias, LV_WARN);
		}
		else
		{
			cfg_alarm_text_dpe_alias = tmp_cfg_alarm_text_dpe_alias;
		}
		
		if (paCfgReadValue(config_path, "dpquery", "Spec_Load_Param", cfg_manager_dp_para) != 0)
		{
			writeLog(g_script_name, "[dpquery]Spec_Load_Param. Default value is " + cfg_manager_dp_para, LV_DBG2);
		}
		
		//[io_info]
		if (paCfgReadValue(config_path, "io_info", "ALARM_PARAM_FORMAT", tmp_cfg_alarm_param_format) != 0)
		{
			writeLog(g_script_name, "Failed to load : [dpquery]ALARM_PARAM_FORMAT. Default value is " + cfg_alarm_param_format, LV_WARN);
		}
		else
		{
			cfg_alarm_param_format = tmp_cfg_alarm_param_format;
		}

		//[var]
		if (paCfgReadValue(config_path, "var", "ALM_CLASS", tmp_cfg_alarm_class) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]ALM_CLASS", LV_WARN);
			ret = false;
		}
		else
		{
			convert_mapData(tmp_cfg_alarm_class, map_alarm_class);
			if (mappinglen(map_alarm_class) == 0)
			{
				writeLog(g_script_name, "Failed to load : [var]ALM_CLASS", LV_WARN);
			}
		}

		if (paCfgReadValue(config_path, "var", "ALM_CLASS_NON", cfg_alarm_non_class) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]ALM_CLASS_NON. Apply default value is " + cfg_alarm_non_class, LV_WARN);
		}

		if (paCfgReadValue(config_path, "var", "PMMODE", cfg_item_var_pmmode) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]PMMODE. Apply default value(null).", LV_WARN);
			ret = false;
		}

		if (paCfgReadValue(config_path, "var", "ALM_ACK_CLIENT", cfg_alarm_ack_client) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]ALM_ACK_CLIENT. Apply default value is " + cfg_alarm_ack_client, LV_WARN);
		}

		if (paCfgReadValue(config_path, "var", "ALM_ACK_USERNAME", cfg_alarm_ack_username) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]ALM_ACK_USERNAME. Apply default value is " + cfg_alarm_ack_username, LV_WARN);
		}

		if (paCfgReadValue(config_path, "var", "ALM_ACK_TYPE", cfg_alarm_ack_type) != 0)
		{
			writeLog(g_script_name, "Failed to load : [var]ALM_ACK_TYPE. Apply default value is " + cfg_alarm_ack_type, LV_WARN);
		}

		//[db_query] -------------------------------------------------------------------
		if (paCfgReadValue(config_path, "db_query", "TBNAME_DEFAULT", TBNAME_DEFAULT) != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]TBNAME_DEFAULT", LV_WARN);
		}

		if (paCfgReadValue(config_path, "db_query", "TIME_FORMAT", TIME_FORMAT) != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]TIME_FORMAT. Default value is " + TIME_FORMAT, LV_WARN);
		}

		if (paCfgReadValue(config_path, "db_query", "TIME_FORMAT_MS", TIME_FORMAT_MS) != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]TIME_FORMAT_MS. Default value is " + TIME_FORMAT_MS, LV_WARN);
		}
		
		if (paCfgReadValue(config_path, "db_query", "ALRM_FIL_YN", tmp_cfg_alrm_fil_yn) != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]ALRM_FIL_YN. ", LV_DBG1);
		}
		else
		{
			cfg_alrm_fil_yn = tmp_cfg_alrm_fil_yn;
		}
		
		if (paCfgReadValueList(config_path, "db_query", "EXCEPTION_FILTER", exception_dpe_list, ",") != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]EXCEPTION_FILTER. ", LV_DBG2);
		}

		if (paCfgReadValueList(config_path, "db_query", "EXCEPTION_CLASS", exception_dpe_class, ",") != 0)
		{
			writeLog(g_script_name, "Failed to load : [db_query]EXCEPTION_FILTER. ", LV_DBG2);
		}
		
		if (paCfgReadValue(config_path, "db_query", "Spec_Load_Cycle", cfg_spec_min) != 0)
		{
			writeLog(g_script_name, "[db_query] Spec_Load_Cycle. Set to default value : " + cfg_spec_min, LV_INFO);
		}
		
		if (paCfgReadValue(config_path, "db_query", "Spec_Valud_Digit", cfg_spec_digit) != 0)
		{
			writeLog(g_script_name, "[db_query] Spec_Valud_Digit. Set to default value : " + cfg_spec_digit, LV_INFO);
		}
		
		if (paCfgReadValue(config_path, "db_query", "Use_Spec_Info", tmp_cfg_use_spec_info) != 0)
		{
			writeLog(g_script_name, "[db_query] Use_Spec_Info. Set to default value : " + cfg_use_spec_info, LV_INFO);
		}
		else
		{
			cfg_use_spec_info = (bool)tmp_cfg_use_spec_info;
		}
		
		string msg = "Configuration Information \n"
			+ "[general] \n"
			+ "ScriptName = " + g_script_name + "\n"
			+ "ScriptActive_Condition = " + ScriptActive_Condition + "\n"
			+ "[dpquery]\n"
			+ "query_condition = " + query_condition + "\n"
			+ "AlamText_DpeAlias = " + cfg_alarm_text_dpe_alias + "\n"
			+ "Query_Blocking_Time = " + cfg_query_blocking_time + "\n"
			+ "Spec_Load_Param = " + cfg_manager_dp_para + "\n"
			+ "[io_info]\n"
			+ "ALARM_PARAM_FORMAT = " + cfg_alarm_param_format + "\n"
			+ "[var]\n"
			+ "ALM_CLASS = " + tmp_cfg_alarm_class + "\n"
			+ "ALM_CLASS_NON = " + cfg_alarm_non_class + "\n"
			+ "PMMODE = " + cfg_item_var_pmmode + "\n"
			+ "ALM_ACK_CLIENT = " + cfg_alarm_ack_client + "\n"
			+ "ALM_ACK_USERNAME = " + cfg_alarm_ack_username + "\n"
			+ "ALM_ACK_TYPE = " + cfg_alarm_ack_type + "\n"
			+ "[db_query]\n"
			+ "TBNAME_DEFAULT = " + TBNAME_DEFAULT + "\n"
			+ "TIME_FORMAT = " + TIME_FORMAT + "\n"
			+ "TIME_FORMAT_MS = " + TIME_FORMAT_MS + "\n"
			+ "ALRM_FIL_YN = " + cfg_alrm_fil_yn + "\n"
			+ "EXCEPTION_FILTER = " + exception_dpe_list + "\n"
			+ "EXCEPTION_CLASS = " + exception_dpe_class + "\n"
			+ "Spec_Load_Cycle = " + cfg_spec_min + "\n"
			+ "Spec_Valud_Digit = " + cfg_spec_digit + "\n"
			+ "Use_Spec_Info = " + cfg_use_spec_info ;

		writeLog(g_script_name, msg, LV_INFO);
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
		ret = false;
	}
	finally
	{
		return ret;
	}
}


//*******************************************************************************
// name         : convert_mapData
// argument     : (string)  txt  = "PVHHALM=HH,PVHIALM=HI,PVLOALM=LO,PVLLALM=LL,...";
// return value : (mapping) //Key="PVHHALM",Value="HH", Key="PVHIALM",Value="HI",...
// date         : 2016-04-11
// developer    : Dev Team
// brief        : config value converting (mapping)
//*******************************************************************************
void convert_mapData(string txt, mapping &mapData)
{
	dyn_string tmp_arr = strsplit(txt, ',');
	dyn_string tmp_map;

	try
	{
		if (dynlen(tmp_arr) == 0)
		{
			mappingClear(mapData);
		}
		else
		{
			for (int i = 1; i <= dynlen(tmp_arr); i++)
			{
				strreplace(tmp_arr[i], " ", "");
				tmp_map = strsplit(tmp_arr[i], '=');

				if (dynlen(tmp_map) == 2)
				{
					mapData[tmp_map[1]] = tmp_map[2];
				}
				else  //mapping
				{
					mappingClear(mapData);
				}
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of convert_mapData(). Error = " + getLastException());
	}
}


//*******************************************************************************
// name         : CB_AlarmEvent
// argument     :
// return value :
// date         : 2016-04-11
// developer    : Dev Team
// brief        : Alarm State change
//*******************************************************************************
void CB_AlarmEvent(anytype userData, dyn_dyn_anytype tab)
{
	//1. AlarmInsert Active? ====================================================

	if (!isScriptActive)
	{
		return;
	}

	update_heartbeat(manager_dpname);//ADD3

	//[ Query Data ]-----------------------------------------------------------------------------------
	//string strSelect = "'_alert_hdl.._came_time','_alert_hdl.._ack_time','_alert_hdl.._gone_time'";
	//strSelect += ",'_alert_hdl.._discrete_states','_alert_hdl.._act_range','_alert_hdl.._partner'";
	//-----------------------------------------------------------------------------------------------
	string alm_dp, alm_dpe, alm_class, alm_sys_dp, sys_name;

	// TH_CM_ALARM_HIST Table Columns
	int eqp_no, pmmode;
	string param_code, alarm_time, alarm_desc, alarm_grade, pmYN;

	dyn_string tmp_dyn_str;
	time i_time, a_time, n_time, p_time, s_time;

	int alm_act_range;
	uint dp_id;
	int dpe_id;
	dyn_dyn_anytype qry_result;

	int cnt_db_query;         		//Number of New DB Query
	string tmp_query;
	string alm_type;
	int conn_idx;
	int ret;
	
	bool is_pmmode_yn;
	
	string spec_param_code, spec_dp_name;


	for (int i = 2; i <= dynlen(tab); i++)
	{
		try
		{
			//value init
			alm_dp = alm_dpe = alm_class = alarm_grade = alarm_desc = "";
			i_time = a_time = n_time = 0;

			//2. Alarm Data Basic info parsing ==============================================
			alm_dp = dpSubStr(tab[i][1], DPSUB_DP);
			alm_dpe = dpSubStr(tab[i][1], DPSUB_DP_EL);
			alm_sys_dp = dpSubStr(tab[i][1], DPSUB_SYS_DP);
			sys_name = dpSubStr(tab[i][1], DPSUB_SYS);

			//i_time -> alarm_time
			i_time = tab[i][3];	//_came_time
			a_time = tab[i][4];	//_ack_time
			n_time = tab[i][5];   //_gone_time
			alm_act_range = tab[i][7];	//_act_range
			p_time = tab[i][8];	//_partner
			is_pmmode_yn = false;
			
			spec_param_code = "";
			anytype spec_value ;
			
			//Spec 기준 연동 동작 Logic
			if(cfg_use_spec_info == true && get_spec_name(alm_dpe, spec_dp_name, spec_param_code) == true)
			{
				int result_dpGet = dpGet(alm_dpe + ":_alert_hdl." + alm_act_range + "._text", alarm_desc,
				alm_dpe + ":_alert_hdl." + alm_act_range + "._class", alm_class,
				alm_dp + spec_dp_name, spec_value);
				
				if(result_dpGet != 0)
				{
					dpGet(alm_dpe + ":_alert_hdl." + alm_act_range + "._text", alarm_desc,
					alm_dpe + ":_alert_hdl." + alm_act_range + "._class", alm_class);
					writeLog(g_script_name, "CB_AlarmEvent() - Spec Value dpGet - Fail. dp name = " + alm_dpe + ", spec_dp_name = " + alm_dp + spec_dp_name , LV_INFO);
				}
			}
			else
			{
				dpGet(alm_dpe + ":_alert_hdl." + alm_act_range + "._text", alarm_desc,
				alm_dpe + ":_alert_hdl." + alm_act_range + "._class", alm_class);
			}
			
			//v2.19 개선 사항 추가 : KTC 변경 시점에 알람 발생하는 경우 : 알람 등급이 조회 되지 않는 경우 1회 더 조회 
			if(alm_class == "")
			{
				alm_act_range = 2;
				string alarm_dpe_desc = alm_dpe + ":_alert_hdl." + alm_act_range + "._text";
				string alarm_dpe_class = alm_dpe + ":_alert_hdl." + alm_act_range + "._class";
				
				if(dpGet(alarm_dpe_desc, alarm_desc, alarm_dpe_class, alm_class) != 0)
				{
					writeLog(g_script_name, "CB_AlarmEvent() - Alarm class dpGet failed. alarm_desc name = " + alarm_dpe_desc + ", alarm_class name = " + alarm_dpe_class , LV_ERR);
				}
			}
			
			//config에서 EXCEPTION_FILTER 설정한 알람 패턴을 알람 저장 대상에서 제외 : isExceptionCheck 함수에서 패턴 확인하여 처리
			if(isExceptionCheck(alm_dpe, alm_class) == true)
			{
				writeLog(g_script_name, "CB_AlarmEvent() - Alarm Event Pass. dp name = " + alm_dpe + ", alert class = " + alm_class , LV_DBG2);
				continue;
			}
			
			//3. Alarm Event processing followed Type(ACK/Release/Occurrence)==============================
			//3-1. Alarm Ack Event processing (확인)
			//------------------------------------------------------------------------
			if (a_time != 0 && (p_time == i_time || p_time == 0))
			{
				//if _partner_time is same with _came_time or empty, normal ACK message
				ack_update(alm_dpe, sys_name, i_time, a_time, true, alm_dpe);
			}
			//------------------------------------------------------------------------
			//3-2. Alarm Release event processing (해제)
			//------------------------------------------------------------------------
			else if (n_time != 0 && p_time == i_time)
			{
				//if _partener_time is same with _came_time, normal Release message
				ntime_update(alm_dpe, sys_name, i_time, n_time, true, alm_dpe);
			}
			//-----------------------------------------------------------------------
			//3-3. Alarm Occurrence event processing
			//------------------------------------------------------------------------
			else if (p_time == 0)  //if _partner_time is empty, new alarm occurrence
			{				
				//ALRM_TMSTP
				alarm_time = formatTime(TIME_FORMAT, i_time, TIME_FORMAT_MS);

				//for China
				if(cfg_alarm_text_dpe_alias)
				{
					alarm_desc = dpGetAlias(alm_dpe);
				}

				//error  Modified : ' --> '' (2018.07.02)
				// strreplace(alarm_desc, "'", "''");
				
				if(strlen(alarm_desc) == 0)
					alarm_desc = " ";

				//ALRM_GRADE
				alm_class = dpSubStr(alm_class, DPSUB_DP); //"S3HVAC:NONJ." --> "NONJ"

				if (alm_class != "" && mappingHasKey(map_alarm_class, alm_class))
				{
					alarm_grade = map_alarm_class[alm_class];
				}

				//PM_YN
				if (dpExists(alm_sys_dp + cfg_item_var_pmmode) == true)
				{
					dpGet(alm_sys_dp + cfg_item_var_pmmode, pmYN);
					
					if (is_pmmode_yn == true || pmYN == "TRUE")
					{
						pmYN = "Y";
					}
					else
					{
						pmYN = "N";
					}
				}
				else
				{
					writeLog(g_script_name, "[" + alm_sys_dp + cfg_item_var_pmmode + "] is not Exist.", LV_DBG1);
					pmYN = "N";
				}

				dyn_anytype dsParams;
				if(cfg_alrm_fil_yn == false)	//FT Alarm Insert Query
				{
					if(cfg_use_spec_info == true)
					{
						// Spec Value number인 경우
						if(is_check_number(spec_value) == true)
						{							
							float f_spec_value = (float)spec_value;
							string str_spec_value = (string)float_truncate(f_spec_value, cfg_spec_digit);		//소수점 자릿수 설정 : Defualt 3으로 설정
							tmp_query = get_occur_query(false, true, true);										//FT, spec 저장 (v2.16)
						
							//바인딩 파라미터 8: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, HMI_FULL_TAG_NAME, ALRM_SPEC_VAL, ALRM_SPEC_PARAM_CODE, PJT_ID
							dsParams = makeDynAnytype(alarm_time, alarm_desc, alarm_grade, pmYN, str_spec_value, spec_param_code, alm_dpe, sys_name);
						}
						// Spec Value 값이 번호가 아닌 경우 : NG --> ALRM_SPEC_VAL컬럼 Null 저장
						else
						{
							//바인딩 파라미터 7: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, HMI_FULL_TAG_NAME, ALRM_SPEC_PARAM_CODE, PJT_ID
							//--> ALRM_SPEC_VAL = NULL 로 저장
							tmp_query = get_occur_query(false, true, false);					//FT, spec 저장 (v2.16)
							dsParams = makeDynAnytype(alarm_time, alarm_desc, alarm_grade, pmYN, alm_dpe, sys_name);
						}
					}
					else
					{
						tmp_query = get_occur_query(false, false);	//FT, spec 저장 X
			
						//바인딩 파라미터 6: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, HMI_FULL_TAG_NAME, PJT_ID
						dsParams = makeDynAnytype(alarm_time, alarm_desc, alarm_grade, pmYN, alm_dpe, sys_name);
					}
				}
				else	//GCS Alarm Insert Query
				{
					//TODO : 송현국
					tmp_query = get_occur_query(true, false);	//GCS
					
					//바인딩 파라미터 5: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, HMI_FULL_TAG_NAME, PJT_ID
					dsParams = makeDynAnytype(alarm_time, alarm_desc, alarm_grade, alm_dpe, sys_name);
				}

				writeLog(g_script_name, "Alarm Insert query : " + tmp_query, LV_DBG2);
				writeLog(g_script_name, "Alarm Insert query arg: " + dsParams, LV_DBG2);

				queryQueue_append(tmp_query, dsParams);
			}   //end else if(p_time == 0)
		}
		catch
		{
			update_user_alarm(manager_dpname, "Exception of CB_AlarmEvent(). Error = " + getLastException());
		}
	}//end for-loop

} //End CB_AlarmEvent()


//*******************************************************************************
// name         : get_occur_query
// argument     : is_gcs_pmmode(GCS 시스템 여부)
// return value : string(알람 발생 Insert 쿼리)
// date         : 2022-07-04
// developed by : Ino-Group
// brief        : 알람 발생 쿼리
//*******************************************************************************
string get_occur_query(bool is_gcs_pmmode = false, bool use_spec_data , bool is_get_sucess = true)
{
	string result_query;
	try
	{		
		//FT
		if(is_gcs_pmmode == false)
		{
			// spec 데이터를 입력할 경우 : ALRM_SPEC_VAL 컬럼 사용
			if(use_spec_data == true)
			{
				// spec 데이터를 dpGet을 성공한 경우
				if(is_get_sucess == true)
				{
					//바인딩 파라미터 8 : 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, ALRM_SEC_VAL, ALRM_SPEC_PARAM_CODE, HMI_FULL_TAG_NAME, PJT_ID
					result_query = "INSERT INTO /*AlarmInsert.get_occur_query_FMCS.SIT-20211029*/ " + TBNAME_DEFAULT + " (ALRM_TMSTP, EQP_NO, PARAM_CODE, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, UPDATE_DATE, ALRM_SPEC_VAL, ALRM_SPEC_PARAM_CODE) "
					+ " SELECT TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3'), EQP_NO, PARAM_CODE, :ALRM_DESC, :ALRM_GRADE_CODE, :PM_YN, SYSDATE, :spec_val, :spec_param_code"
					+ " FROM TN_CM_HMI_FULL_TAG_NAME WHERE HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME AND PJT_ID = :PJT_ID;";
					
					
				}
				// spec 데이터를 dpGet을 실패한 경우
				else
				{
					//바인딩 파라미터 7 : 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, ALRM_SPEC_PARAM_CODE, HMI_FULL_TAG_NAME, PJT_ID
					result_query = "INSERT INTO /*AlarmInsert.get_occur_query_FMCS.SIT-20211029*/ " + TBNAME_DEFAULT + " (ALRM_TMSTP, EQP_NO, PARAM_CODE, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, UPDATE_DATE) "
					+ " SELECT TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3'), EQP_NO, PARAM_CODE, :ALRM_DESC, :ALRM_GRADE_CODE, :PM_YN, SYSDATE"
					+ " FROM TN_CM_HMI_FULL_TAG_NAME WHERE HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME AND PJT_ID = :PJT_ID;";
					
				}
					
			}
			else	// spec 데이터를 입력안할 경우 : ALRM_SPEC_VAL 컬럼 미사용
			{
				//바인딩 파라미터 6: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, HMI_FULL_TAG_NAME, PJT_ID
				result_query = "INSERT INTO /*AlarmInsert.get_occur_query_FMCS.SIT-20211029*/ " + TBNAME_DEFAULT + " (ALRM_TMSTP, EQP_NO, PARAM_CODE, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, UPDATE_DATE) "
				+ " SELECT  TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3'), EQP_NO, PARAM_CODE, :ALRM_DESC, :ALRM_GRADE_CODE, :PM_YN, SYSDATE "
				+ " FROM TN_CM_HMI_FULL_TAG_NAME WHERE HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME AND PJT_ID = :PJT_ID;";
			}
			

		}
		else //GCS
		{
			//바인딩 파라미터 5: 발생 시간, ALRM_DESC, ALRM_GRADE_CODE, HMI_FULL_TAG_NAME, PJT_ID
			result_query = "INSERT INTO /*AlarmInsert.get_occur_query_GCS.SIT-20211021*/ " + TBNAME_DEFAULT + " ( ALRM_TMSTP, EQP_NO, PARAM_CODE, ALRM_DESC, ALRM_GRADE_CODE, PM_YN, UPDATE_DATE) "
			+ " SELECT TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3'), TAG.EQP_NO, TAG.PARAM_CODE, :ALRM_DESC, :ALRM_GRADE_CODE, ATTR.ALRM_FIL_YN, SYSDATE "
			+ " FROM TN_CM_HMI_FULL_TAG_NAME  TAG, TN_CM_TAG_ATTR ATTR "
			+ " WHERE TAG.HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME AND TAG.PJT_ID = :PJT_ID AND TAG.EQP_NO = ATTR.EQP_NO (+) AND TAG.PARAM_CODE = ATTR.PARAM_CODE (+); ";
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_occur_query(). Error = " + getLastException());
	}
	finally
	{
		return result_query;
	}
}

//*******************************************************************************
// name         : get_release_query
// argument     : 
// return value : string(알람 해재 Update 쿼리)
// date         : 2021-08-19
// developed by : Ino-Group
// brief        : 알람 해제 쿼리
//*******************************************************************************
string get_release_query()
{
	string result_query;
	try
	{
		//바인딩 파라미터 5 : HMI_FULL_TAG_NAME, PJT_ID, 발생시간, 해제시간, ALRM_LEADTIME
		result_query = "MERGE INTO  /*AlarmInsert.get_release_query_FMCS.SIT-20211029*/ " + TBNAME_DEFAULT + " ALM " 
		+ " USING TN_CM_HMI_FULL_TAG_NAME TAG ON ( TAG.HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME "
		+ " AND TAG.PJT_ID = :PJT_ID "
		+ " AND ALM.EQP_NO = TAG.EQP_NO "
		+ " AND ALM.PARAM_CODE = TAG.PARAM_CODE "
		+ " AND ALM.ALRM_TMSTP = TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3') ) "
		+ " WHEN MATCHED THEN "
		+ " UPDATE SET ALM.END_TMSTP = TO_TIMESTAMP(:END_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3') "
		+ " , ALM.ALRM_LEADTIME = :ALRM_LEADTIME "
		+ " , ALM.UPDATE_DATE = SYSDATE; ";
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_release_query(). Error = " + getLastException());
	}
	finally
	{
		return result_query;
	}
}


//*******************************************************************************
// name         : get_ack_query
// argument     : 
// return value : string(알람 해재 Update 쿼리)
// date         : 2021-08-19
// developed by : Ino-Group
// brief        : 알람 Ack 쿼리
//*******************************************************************************
string get_ack_query()
{
	string result_query;
	try
	{
		//바인딩 파라미터 6 : HMI_FULL_TAG_NAME, PJT_ID, 발생 시간, Ack 시간, ALRM_ACK_USER_ID, ALRM_ACK_CLIENT_NAME
		result_query = "MERGE INTO /*AlarmInsert.get_ack_query_FMCS.SIT-20211029*/ " + TBNAME_DEFAULT + " ALM " 
		+ " USING TN_CM_HMI_FULL_TAG_NAME TAG ON ( TAG.HMI_FULL_TAG_NAME = :HMI_FULL_TAG_NAME "
		+ " AND TAG.PJT_ID = :PJT_ID "
		+ " AND ALM.EQP_NO = TAG.EQP_NO " 
		+ " AND ALM.PARAM_CODE = TAG.PARAM_CODE " 
		+ " AND ALM.ALRM_TMSTP = TO_TIMESTAMP(:ALRM_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3') ) " 
		+ " WHEN MATCHED THEN UPDATE " 
		+ " SET ALM.ACK_TMSTP = TO_TIMESTAMP(:ACK_TMSTP, 'YYYY.MM.DD HH24:MI:SS.FF3') "
		+ " , ALM.ALRM_ACK_USER_ID = :ALRM_ACK_USER_ID "
		+ " , ALM.ALRM_ACK_CLIENT_NAME = :ALRM_ACK_CLIENT_NAME "
		+ " , ALM.UPDATE_DATE = SYSDATE " ;
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of get_ack_query(). Error = " + getLastException());
	}
	finally
	{
		return result_query;
	}
}


//*******************************************************************************
// name         : isExceptionCheck
// argument     : dpe_name(alert dpe name), alert_class(alert class)
// return value : bool
// date         : 2020-08-07
// developed by : Ino-Group
// brief        : Script config information Load
//*******************************************************************************
bool isExceptionCheck(string dpe_name, string alert_class)
{
	bool is_result = false;
	try
	{
		//1. config 파일 EXCEPTION_FILTER 옵션 처리
		for(int i = 1; i <= dynlen(exception_dpe_list); i++)
		{
			if(patternMatch(exception_dpe_list[i], dpe_name) == true)
			{
				writeLog(g_script_name, "isExceptionCheck() -Pass(exception_dpe_list). dpName = " + dpe_name, LV_DBG2);
				is_result = true;
				break;
			}
		}
		
		//2. config 파일 EXCEPTION_CLASS 옵션 처리
		if(dynlen(exception_dpe_class) > 0 )
		{
			if(alert_class == exception_dpe_class[2] && patternMatch(exception_dpe_class[1], dpe_name) == true)
			{
				writeLog(g_script_name, "isExceptionCheck() - Pass(exception_dpe_class). dpName = " + dpe_name + ", alaert class = " + alert_class, LV_DBG2);
				is_result = true;
			}
		}
		
		//3. config 파일의 ALM_CLASS_NON (D 등급) 저장 제외
		if(strpos(alert_class, cfg_alarm_non_class) >= 0)
		{
			writeLog(g_script_name, "isExceptionCheck() - Pass(cfg_alarm_non_class). dpName = " + dpe_name + ", alaert class = " + alert_class, LV_DBG2);	
			is_result = true;
		}
		
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of isExceptionCheck(). Error = " + getLastException());
	}
	finally
	{
		return is_result;
	}
}


//*******************************************************************************
// name         : ack_update
// string tag   : tag name
// time i_time   : alarm occurrence time
// time a_time   : alarm check time
// return value : created db query
// date         : 2013-10-07 -> 2016-04-11
// developer    : Park. -> DEV Team edit(string->time)
// brief        : when alarm is checked(ack), update sql execution
//*******************************************************************************
bool ack_update(string dpe_name, string sys_name, time i_time, time a_time, bool is_get_info, string tag_name)
{
	string update_query, ack_client, ack_username;
	int ackType;
	string str_itime, str_atime;
	int conn_idx;

	//Apply TimeFormat
	try
	{
		//1. 날짜 포맷 변경
		str_itime = formatTime(TIME_FORMAT, i_time, TIME_FORMAT_MS);
		str_atime = formatTime(TIME_FORMAT, a_time, TIME_FORMAT_MS);

		//2. Ack 정보 조회
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

		//3. 쿼리 생성
		update_query = get_ack_query();

		//바인딩 파라미터 6 : HMI_FULL_TAG_NAME, PJT_ID, 발생 시간, Ack 시간, ALRM_ACK_USER_ID, ALRM_ACK_CLIENT_NAME
		dyn_anytype dsParams = makeDynAnytype( dpe_name, sys_name, str_itime,  str_atime, ack_username, ack_client);

		if (is_get_info == true)
		{
			writeLog(g_script_name, "Alarm Ack Update query : " + update_query, LV_DBG2);
			writeLog(g_script_name, "Alarm Ack Update query arg : " + dsParams, LV_DBG2);
			queryQueue_append(update_query, dsParams);
		}
		else
		{
			DROP_FILE("DBLog/" + g_script_name + "_Loss", "\"" + tag_name + "\" \"" + update_query + "\" \"" + dsParams + "\"");
		}

	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of ack_update(). Error = " + getLastException());
		return false;
	}
	return true;
}


//*******************************************************************************
// name         : ntime_update
// string tag   : tag name
// time i_time  : alarm creation time
// time n_time  : alarm releasing time
// int dur      : alarm duration(second)
// return value : creaed dp query
// date         : 2013-10-07 -> 2016-04-11
// developer    : Park. -> DEV Team edit(string->time)
// brief        : when alarm is released, update sql execution
//*******************************************************************************
bool ntime_update(string dpe_name, string sys_name, time i_time, time n_time, bool is_get_info, string tag_name)
{
	string str_itime, str_ntime;
	int dur, conn_idx;
	string update_query;

	try
	{
		//1. 날짜 포맷 변경
		str_itime = formatTime(TIME_FORMAT, i_time, TIME_FORMAT_MS);
		str_ntime = formatTime(TIME_FORMAT, n_time, TIME_FORMAT_MS);
		
		//2. 알람 발생 기간 계산
		dur = period(n_time - i_time);

		//3. 쿼리 생성
		update_query = get_release_query();
		
		////바인딩 파라미터 5 : HMI_FULL_TAG_NAME, PJT_ID, 발생시간, 해제시간, ALRM_LEADTIME
		dyn_anytype dsParams = makeDynAnytype( dpe_name, sys_name, str_itime, str_ntime, dur);

		if (is_get_info == true)
		{
			writeLog(g_script_name, "Alarm Release Update query : " + update_query, LV_DBG2);
			writeLog(g_script_name, "Alarm Release Update query arg: " + dsParams, LV_DBG2);
			queryQueue_append(update_query, dsParams);
		}
		else
		{
			DROP_FILE("DBLog/" + g_script_name + "_Loss", "\"" + tag_name + "\" \"" + update_query + "\" \"" + dsParams + "\"");
		}
	}
	catch
	{
		update_user_alarm(manager_dpname, "Exception of ntime_update(). Error = " + getLastException());
		return false;
	}
	return true;
}


//*******************************************************************************
// name         : get_spec_name
// argument     : 
// return value : spec 이름 조회 성공 여부
// date         : 2022-08-09
// script by    : Inno Team
// brief        : 알람 DP 이름을 입력받아, 알람의 spec dpe 이름을 확인 -> spec_dp_name
//*******************************************************************************
bool get_spec_name(string alarm_dpe_name, string& spec_param_name, string& spec_param_code)
{
	bool result = true;
	string dp_type, alarm_param ;
	dyn_string split_list;
	string spec_key;
	
	try
	{
		//1. 알람 Param Code 분리 : "BTR_1F11A_TEMP.alert.PVHHALM" -> "PVHHALM"
		split_list = strsplit(alarm_dpe_name, ".");
		
		//BTR_1F11A_TEMP | alert | PVHHALM -> "PVHHALM"
		alarm_param = split_list[dynlen(split_list)];
		
		//2. 알람 DP의 type 확인 "BTR_1F11A_TEMP.alert.PVHHALM" -> "AI"
		dp_type = dpTypeName(alarm_dpe_name);
		
		//3. spec 파라미터 Key 생성 : "AI&PVHHALM"
		spec_key = dp_type + "&" + alarm_param;
		
		//"AI", "PVHHALM"-> PVHH
		//g_map_spec_info --> "AI" + "PVHHALM" (key) : "PVHH" (value), "AI" + "PVHIALM" (key) : "PVHI" (value), ...
		
		if(mappingHasKey(g_map_spec_info, spec_key) == true)
		{
			dyn_string value_list = g_map_spec_info[spec_key];
			spec_param_code = value_list[1];
			spec_param_name = value_list[2];
		}
		else
		{
			writeLog(g_script_name, "get_spec_name() -  There is no parameter information for Spec. spec_key = " + spec_key, LV_DBG1);
			result = false;
		}
	}
	catch
	{
		result = false;
		update_user_alarm(manager_dpname , "Exception of get_spec_name(). Error = " + getLastException());
	}
	finally
	{
		return result;
	}
}


//*******************************************************************************
// name         : init_spec_info
// argument     : 
// return value : Spec 기준 정보 Logic 정상 동작 여부
// date         : 2022-08-09
// script by    : Inno Team
// brief        : Spec 기준 정보 전체 조회, Spec 기준 정보 수동 조회 Trigger 감시, Spec 기준 정보 조회 Thread(설정 시간)
//*******************************************************************************
bool init_spec_info()
{
	bool result = true;
	
	try
	{
		//1. Spec 기준 정보 전체 조회 -> g_map_spec_info 메모리에 저장
		if(load_spec_info(false) == true)
		{
			writeLog(g_script_name,"init_spec_info() - Load Spec info - OK", LV_INFO);
			
			//1-1. Spec 기준 정보 최초 DB 테이블에서 조회시 0개인 경우 로그 출력
			if(mappinglen(g_map_spec_info) == 0)
			{
				writeLog(g_script_name,"init_spec_info() - Spec info query result. Count = 0", LV_INFO);
			}
		}
		else
		{
			writeLog(g_script_name,"init_spec_info() - Load Spec info - NG", LV_WARN);
			result = false;
		}
		
		//2. Spec 기준 정보 조회 Thread 호출
		if(scheduled_task("load_spec_info", cfg_spec_min) == true)
		{
			writeLog(g_script_name,"init_spec_info() - scheduled_task start OK. schedule function = load_spec_info()"  , LV_INFO);
		}
		else
		{
			writeLog(g_script_name,"init_spec_info() - scheduled_task start NG. " , LV_ERR);
			result = false;
		}
		
		//3. Spec 기준 정보 조회 Trigger 감시
		string manager_dpe = manager_dpname + cfg_manager_dp_para;
		int result_cnn = dpConnect("CB_manager_dp", manager_dpe);
		if(result_cnn == 0)
		{
			writeLog(g_script_name,"init_spec_info() - Manager DP Monitoring " + manager_dpe + ". OK", LV_INFO);
		}
		else
		{
			writeLog(g_script_name,"init_spec_info() - Manager DP Monitoring " + manager_dpe + ". NG", LV_ERR);
			result = false;
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of init_spec_info(). Error = " + getLastException());
		result =false;
	}
	finally
	{
		return result;
	}
}


//*******************************************************************************
// name         : load_spec_info()
// argument     :
// return value : DB Query 성공 여부
// date         : 2022-08-09
// script by    : Inno Team
// brief        : 알람 Param에 따른 Spec 기준 정보를 DB에서 Load -> g_map_spec_info 메모리 저장
//*******************************************************************************
bool load_spec_info(bool is_only_changed_data = true)
{
	string query;
	dyn_string dsParams;
	dyn_dyn_anytype qry_result;
	int conn_index;
	bool result = true;
	
	try
	{
		//1. 알람 Spec 파라미터 기준 정보 조회 : DPTYPE_CODE, PARAM_CODE, SPEC_PARAM_NAME
		query = "SELECT /* findAlarmSpecParamCode-20220701-jun94.jang */ "
		
		//DPTYPE_CODE, PARAM_CODE, ALRM_SPEC_PARAM_CODE
		+ " DPTP.DPTYPE_CODE AS DPTYPE_CODE, DPTP.PARAM_CODE AS PARAM_CODE, DPTP.ALRM_SPEC_PARAM_CODE AS ALRM_SPEC_PARAM_CODE, "
		
		//SPEC_PARAM_NAME, USE_YN
		+ " ( SELECT REAL_PARAM_NAME FROM TN_CM_DPTYPE_PARAM " 
		+ " WHERE PJT_ID = DPTP.PJT_ID "
		+ " AND DPTYPE_CODE = DPTP.DPTYPE_CODE "
		+ " AND PARAM_CODE = DPTP.ALRM_SPEC_PARAM_CODE "
		+ " AND USE_YN = 'Y' "
		+ " ) AS SPEC_PARAM_NAME, LEAST(DPT.USE_YN, DPTP.USE_YN) AS USE_YN, "
		
		//MOD_DATE
		+ " TO_CHAR( "
		+ " GREATEST( NVL ( DPT.MOD_DATE, TO_DATE('1970', 'YYYY')), NVL(DPTP.MOD_DATE, TO_DATE('1970', 'YYYY')), "
		+ " NVL ( "
			+ " ( SELECT MOD_DATE FROM TN_CM_DPTYPE_PARAM " 
			+ " WHERE PJT_ID = DPTP.PJT_ID AND DPTYPE_CODE = DPTP.DPTYPE_CODE AND PARAM_CODE = DPTP.ALRM_SPEC_PARAM_CODE"
			+ " ), TO_DATE('1970', 'YYYY'))),'YYYYMMDDHH24MISS') AS MOD_DATE "
			
		+ " FROM TN_CM_DPTYPE DPT, TN_CM_DPTYPE_PARAM DPTP "
		+ " WHERE DPT.PJT_ID = DPTP.PJT_ID "
		+ " AND DPT.PJT_ID = :pjt_id "
		+ " AND DPT.DPTYPE_CODE = DPTP.DPTYPE_CODE "
		+ " AND DPTP.PARAM_TYPE_CODE = 'ALARM' " ;
		
		if(is_only_changed_data == true)	//변경된 데이터만 조회
		{
			query += " AND ( "
			+  " ( DPT.MOD_DATE > TO_DATE(:mod_date, 'YYYYMMDDHH24MISS') AND DPT.MOD_DATE < SYSDATE - 2 / 24 / 3600) "
			+  " OR ( DPTP.MOD_DATE > TO_DATE(:mod_date, 'YYYYMMDDHH24MISS') AND DPTP.MOD_DATE < SYSDATE - 2 / 24 / 3600) " 
			+  " OR EXISTS ( SELECT /* findUpdatedSpecParamCodeByModDate-20220701-jun94.jang */ 1 "
				+  " FROM TN_CM_DPTYPE_PARAM "
				+  " WHERE PJT_ID = DPTP.PJT_ID "
				+  " AND DPTYPE_CODE = DPTP.DPTYPE_CODE " 
				+  " AND PARAM_CODE = DPTP.ALRM_SPEC_PARAM_CODE "
				+  " AND MOD_DATE > TO_DATE(:mod_date, 'YYYYMMDDHH24MISS') AND MOD_DATE < SYSDATE - 2 / 24 / 3600 "
			+ " ) ) ";
			
			string mod_date = formatTime("%Y%m%d%H%M%S" , g_mod_max_time);
			dsParams = makeDynString(g_pjt_id, mod_date, mod_date, mod_date);
		}
		else  								// 초기 전체 데이터 조회
		{
			query += " AND DPT.USE_YN = 'Y' "
			+ " AND DPTP.USE_YN = 'Y' " 
			+ " AND DPTP.ALRM_SPEC_PARAM_CODE IS NOT NULL " ;
			
			dsParams = makeDynString(g_pjt_id);
		}
		
		//2. DB Query 동작		
		conn_index = get_DBConn();
		int result_db = rdbSelectSingle_Bind(g_dbConn_pool[conn_index], query, dsParams, qry_result);
		
		if(result_db == DB_ERR_NONE) //OK
		{
			g_schedule_function_result = true;
			if(dynlen(qry_result) > 0)
			{
				writeLog(g_script_name,"load_spec_info() - Spec info Query OK. count = " + dynlen(qry_result) , LV_DBG1);
				
				//3. Spec 기준 정보 map에 저장
				for(int i = 1; i <= dynlen(qry_result); i++)
				{
					//ex) AI(DP Type), PVHHALM(Alarm Param Code) -> "AI&PVHHALM"
					string db_key_dpType = qry_result[i][1];			// "AI"
					string db_key_alrm_parama_code = qry_result[i][2];	// "PVHHALM"
					string db_value_spec_param_code = qry_result[i][3];	// "PVHH"
					string db_value_spec_param_name = qry_result[i][4];	// ".cmd.PVHH"
					string db_use_yn = qry_result[i][5];				// "Y"					
					string db_mod_time = qry_result[i][6];				// "20220712130000"
					time t_mod_time = getConverTime(db_mod_time);
					
					if(t_mod_time > g_mod_max_time)
						g_mod_max_time = t_mod_time;					// "2022.08.09 13:00:00"
					
					string spec_key = db_key_dpType + "&" + db_key_alrm_parama_code;	//"AI&PVHHALM"
					
					//3-1. 기준 정보 유효성 조건 확인 : USE_YN 컬럼 = "Y" or Spec의 REAL_PARAM_NAME not null
					if(db_use_yn == "Y" && strlen(db_value_spec_param_name) > 0)
					{
						//메모리에 저장할 value 값 생성
						dyn_string value_list = makeDynString(db_value_spec_param_code, db_value_spec_param_name);
						g_map_spec_info[spec_key] = value_list;
						
						if(is_only_changed_data == true)
						{
							writeLog(g_script_name,"load_spec_info() - changed DB Data. key = " + spec_key + ", value = " + (string)value_list, LV_INFO);
						}
					}
					else
					{
						//유효 데이터가 아닌 경우 메모리에서 삭제 : g_map_spec_info에서 key 삭제
						if(mappingHasKey(g_map_spec_info, spec_key) == true)
						{
							mappingRemove(g_map_spec_info, spec_key);
							writeLog(g_script_name,"load_spec_info() - memory remove Data. key = " + spec_key , LV_INFO);
						}
					}
				}
			}
			else
			{
				writeLog(g_script_name,"load_spec_info() - Spec info Query Data empty. query = " + query + ", params = " + dsParams, LV_DBG1);
			}
		}
		else if(result_db == DB_ERR_QUERY)	//Query Fail
		{
			writeLog(g_script_name, "load_spec_info() - DB Query Fail. query = " + query + ", params = " + dsParams, LV_WARN);
			result = false;
		}
		else	//DB Connection Error
		{
			create_DBConnPool();
			writeLog(g_script_name, "load_spec_info() - DB Connection Fail. query = " + query + ", params = " + dsParams, LV_WARN);
			g_schedule_function_result = false;
			result = false;
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of load_spec_info(). Error = " + getLastException());
		g_schedule_function_result = false;
		result = false;
	}
	finally
	{
		if(conn_index > 0)
			release_DBConn(conn_index);
		return result ;
	}
}

//string 타입을 time 타입으로 변경 : ex) "20220712171848" --> 2022.07.12 17:18:48.000000000
time getConverTime(string str_time)
{
    const int time_length = 14;
    time convert_time;
    string srt_year, str_month, str_day, str_h, str_m, str_s;

    if(strlen(str_time) == time_length)
    {
        srt_year = substr(str_time, 0, 4);
        str_month = substr(str_time, 4, 2);
        str_day = substr(str_time, 6, 2);
        str_h = substr(str_time, 8, 2);
        str_m = substr(str_time, 10, 2);
        str_s = substr(str_time, 12, 2);
        
        convert_time = makeTime(srt_year, str_month, str_day, str_h, str_m, str_s);
    }
    else
    {
        writeLog(g_script_name, "getConverTime() - It is not a string of type time. str_time = " + str_time , LV_WARN);
    }
    
    return convert_time;
}

//*******************************************************************************
// name         : check_spec_load_time()
// argument     : dpe_name(Manager DP), value(트리거 실행 값 -> True인 경우 Spec 기준 정보 조회)
// return value : void
// date         : 2022-08-09
// script by    : Inno Team
// brief        : Manager DP 감시 -> True 변경 시 Spec 기준 정보 Load
//*******************************************************************************
void CB_manager_dp(string dpe_name, anytype value)
{
	try
	{
		// Manager DP True 변경시 수동 조회 : Spec 기준 데이터 조회
		if(value == true)
		{
			//1. 스케쥴링 수동 호출 -> g_scheduled_trigger 조건으로 동작
			writeLog(g_script_name, "CB_manager_dp() - Spec Info Load Trigger On.", LV_INFO);
			g_scheduled_trigger = true;									//library_standard.schedule_thread() -> false로 변경

			//2. Manager DP False 변경
			string changed_dpe_name = dpSubStr(dpe_name, DPSUB_DP_EL);
			dpSet(changed_dpe_name, false);
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of CB_manager_dp(). Error = " + getLastException());
	}
}

//*******************************************************************************
// name         : is_check_number()
// argument     : value(숫자 타입인지 확인해야할 변수)
// return value : bool(숫자 타입인 경우 True, 아닌 경우 False)
// date         : 2022-08-09
// script by    : Inno Team
// brief        : 입력받는 anytype의 데이터 타입이 숫자인지 확인하는 함수
//*******************************************************************************
bool is_check_number(const anytype& value)
{
	int result = false;
	int type_number = getType(value);
	
	if(type_number == INT_VAR 
	|| type_number == UINT_VAR 
	|| type_number == FLOAT_VAR)
	{
		result = true;
	}
	
	return result;
}