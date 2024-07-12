//v1.0(2020.08.10)
//1.ConntactCutOut first version
//v1.01(2020.10.29)
//1. Add DB Connection (set_alarm_unacitve(), check_running_parent())
//v1.02(2021.02.03)
//1. Modify log when parent DP is 0 : load_parent_info()
//v1.03(2021.03.31)
//1. MIN_PRIO value -> DEFINE
//2. 일부 동작상태 정보 로그 레벨 수정(LV_INFO -> LV_DBG1) : CB_parent_status(), update_alarm_active()
//-----------------------------------------------------------
//v1.04(2021.06.30) ------------------------------------------
//1. Add config File name lookup from manager dp

//v1.05(2021.07.05) ------------------------------------------
//1. 부모 Tag 삭제시 dpDisConnect 조건 추가 : Tag가 있는 경우에만 dpDisConnect 수행 --> load_parent_info() 함수 수정

//v1.06(2023.09.25) ------------------------------------------
//1. 동작 중인 CCO 부모 Tag 감시 Thread의 synchronized 개선

#uses "CtrlADO"
#uses "library_standard.ctl"
#uses "library_DB.ctl"
#uses "hosts.ctl"

//---------------------------------------------
// configuration path & filename  
//---------------------------------------------
string script_path;      //getPath(SCRIPTS_REL_PATH);
string config_filename;
const string g_script_release_version = "v1.06";
const string g_script_release_date = "2023.09.25";
const string g_script_name = "ContactCutOut";
string manager_dpname ="";  //ex: WCCOActrl_2  (A_SIT_ADMIN_MANAGER)

string ScriptActive_Condition  = "ACTIVE";  //|BOTH|HOST1|HOST2";

//config 
string site_code, sys_code, pjt_id;
string reload_dp;
dyn_string value_leaf_list;
const int MINIMUM_DELAY = 60;
int delay_check_parent = 60;

const int CCO_MODE = 50;
const int CCO_PMMODE_MODE = 150;

const int ACTIVE_MODE = 0;
const int ACTIVE_PMMODE_MODE = 100;

const int MIN_PRIO_VALUE = 50;


// DB Connection
dbConnection CONN_DB;	//DB Connection to get the parent DP
string db_con_info;
int rs, dbc;

//dpConnect info
mapping map_dpconn;			//key = parent dp, value = eqp_no
dyn_string parent_queue ;	//Changed Parent DP Name
bool reload_flag = true;	//Flag if the DP is changed.(Check if Parent DP structure has been changed) DP = CCO_PARENT.CHG_STATE
int conn_idx;

//map key name
const string KEY_GROUP_ID = "KEY_GROUP_ID";
const string KEY_CHILD_LIST = "KEY_CHILD_LIST";
const string KEY_PARENT_EQP_NO = "KEY_PARENT_EQP_NO";

//Save the dpConnect connected DP Information on the map
mapping map_parent_info ; 		// key = parent_name, value = map( group_id, child_dp_list)

//Save the Queue when running a script, or change the parent DP
mapping map_parent_queue ;		// key = parent_name, value = CCO Status(Alarm Active = True or Unactive = False)

mapping map_parent_stauts;

//*******************************************************************************
// name         : main
// argument     : 
// return value : void
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Script Main Function
//*******************************************************************************
void main()
{
	time t;
	dyn_errClass err;
	int result, result2;
	bool is_result;
	
	string query, query_from;
	
	try
	{
		init_lib_Commmon();	//Debug-Flag Initialize
		
		writeLog(g_script_name, "0. Script Start! Release Version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
		writeLog(g_script_name, "				  lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);
		writeLog(g_script_name, "                 lib_db Version = " + g_lib_db_version + ", Date = " + g_lib_db_release_date, LV_INFO);

		manager_dpname = init_program_info(g_script_name, g_script_release_version, g_script_release_date);		//Create Script Monitoring DP
		
		//---------------------------------------------
		//1. Load config file
		//---------------------------------------------
		if(load_config() == false)
		{
			update_user_alarm(manager_dpname ,"1. Initialize(Load the Config) : NG");
			exit();
		}
		else
		{
			load_config_lib_db(config_filename);	//DB Conifg Load
			writeLog(g_script_name,"1. Initialize(Load the Config) : OK", LV_INFO);
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
		//3. DB Connect for initialize
		//---------------------------------------------
		if(init_DBConnPool() == true)
		{
			create_DBConnPool();
			int thread_ID ;
			thread_ID = startThread("queryQueue_manager", true);
			writeLog(g_script_name,"3-1. Start DB Query Thread. Thread ID = " + thread_ID, LV_INFO);
			writeLog(g_script_name,"3-2. DP Connection OK ", LV_INFO);
		}
		
		//---------------------------------------------  
		//4. Reload DP, Alert DP dpConnect
		//---------------------------------------------
		result = dpConnect("CB_reload",false, reload_dp);
		if(!result)
		{
			writeLog(g_script_name,"4-1. Reload DP monitoring(dpConnect) Success. DP Name = " + reload_dp, LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname ,"4-1. Reload DP monitoring(dpConnect) failed. DP Name = " + reload_dp);
			exit();
		}

		//---------------------------------------------  
		//5. Thread Start
		//---------------------------------------------
		result = startThread("update_alarm_active");
		
		if(result)
		{
			writeLog(g_script_name,"5. Thread Start. function = update_alarm_active" , LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname ,"5. Thread Start NG. function = update_alarm_active");
			exit();
		}
		
		//---------------------------------------------  
		//6. Thread Start
		//---------------------------------------------
		result = startThread("check_running_parent");
		
		if(result)
		{
			writeLog(g_script_name,"6. Thread Start. function = check_running_parent" , LV_INFO);
		}
		else
		{
			update_user_alarm(manager_dpname , "6. Thread Start NG. function = check_running_parent");
			exit();
		}
		
		writeLog(g_script_name,"===== Script initalize Complete =====", LV_INFO);
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of main(). Error = " + getLastException());
	}
}


//*******************************************************************************
// name         : load_config
// argument     : 
// return value : bool
// date         : 2020-07-09
// developed by : Ino-Group
// brief        : Script config information Load
//*******************************************************************************
bool load_config()
{
	string config_path;
	bool is_result = true;
	string tmp_DSN, tmp_UID, tmp_PWD, tmp_db_conn ;
	
	try
	{
		//load config File Name from Manager DP
		if(globalExists("global_config_name") == TRUE)
			config_filename = global_config_name;
			
		// load script Path
		config_path = getPath(SCRIPTS_REL_PATH) + config_filename;		
		
		writeLog(g_script_name, "load_config() - config file path = " + config_path, LV_DBG2);
				
		// [general] section 
		if(paCfgReadValue(config_path,"general","Active_Condition", ScriptActive_Condition) != 0)
		{
			writeLog(g_script_name,"Failed to load : [general] Active_Condition, Set to default value : ACTIVE", LV_WARN);
		}
		
		if(paCfgReadValue(config_path,"general","Parent_Check_Delay", delay_check_parent) != 0)
		{
			writeLog(g_script_name,"[general] Parent_Check_Delay, Set to default value : " + delay_check_parent, LV_WARN);
		}
		else
		{
			if(delay_check_parent < MINIMUM_DELAY)
			{
				delay_check_parent = MINIMUM_DELAY;
				writeLog(g_script_name,"[general] Parent_Check_Delay, This is not an appropriate value.  Minimum value = " + MINIMUM_DELAY, LV_WARN);
			}
		}
		
		// [Parent_info]
		if(paCfgReadValue(config_path,"parent_info","Site_Code", site_code) != 0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] Site_Code.", LV_ERR);
			is_result = false;
		}
		
		if(paCfgReadValue(config_path,"parent_info","Sys_Code", sys_code) != 0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] Sys_Code.", LV_ERR);
			is_result = false;
		}				
		
		if(paCfgReadValue(config_path,"parent_info","Pjt_ID", pjt_id) != 0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] Pjt_ID.", LV_ERR);
			is_result = false;
		}		
		
		if(paCfgReadValueList(config_path, "parent_info", "Value_Leaf", value_leaf_list, ",")!=0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] Value_Leaf.", LV_ERR);
			is_result = false;
		}

		if(paCfgReadValue(config_path, "parent_info", "Relaod_DP", reload_dp) != 0)
		{
			writeLog(g_script_name, "Failed to load : [parent_info] Relaod_DP.", LV_ERR);
			is_result = false;
		}

		string msg = "\n [general] \n" +
		"\n Active_Condition = " + ScriptActive_Condition +
		"\n Parent_Check_Delay = " + delay_check_parent +

		"\n [parent_info]" +
		"\n Site_Code = " + site_code +
		"\n Sys_Code = " + sys_code +
		"\n Pjt_ID = " + pjt_id +
		"\n Value_leaf = " + value_leaf_list +
		"\n Relaod_DP = " + reload_dp +
		
		"\n [db_con]" +
		// "\n DSN = " + tmp_DSN +
		// "\n UID = " + tmp_UID +
		// "\n PWD = " + tmp_PWD +
		"\n Connection Information = " + DB_CONN_STRING ;
		"\n\n";
		
		writeLog(g_script_name, msg, LV_INFO);		
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of load_config() " + getLastException());
		is_result = false;
	}
	finally
	{
		return is_result;
	}
}


//*******************************************************************************
// name         : load_parent_info
// argument     : 
// return value : bool
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Inquiry of Parent DP in DB
//*******************************************************************************
bool load_parent_info()
{
	bool is_load_result = true;
	//string query, parent_dp_name, parent_eqp_no, group_id, child_dp_name ;
	string query, parent_dp_name, group_id, child_dp_name ;
	dyn_dyn_anytype qry_result; 
	int conn_idx, result, connect_count = 0;
	
	dyn_string dsParams, child_list;
	// string pjt_id_condition1, pjt_id_condition2;	//:pjt_id1, :pjt_id2
	
	mapping map_delete_dp, map_new_parent, map_child_info;
	int rs ;
	
	try
	{
		//1. Load Parent DP 
		//1-1. Create query statement conditional clause according to config option(pjt list)
		// pjt_id_condition1 = get_pjt_condition(pjt_id_list, 1);
		// pjt_id_condition2 = get_pjt_condition(pjt_id_list, dynlen(pjt_id_list)+1);

		query = "SELECT /*ContactCutOut.ctl-20200427-SIT*/ B.eqp_name, A.ALRM_FIL_GROUP_ID, C.EQP_NAME" 
		+ " FROM TN_CM_ALRM_FIL_TAG A, TN_CM_EQP B,"
			+ " (SELECT B.EQP_NAME, B.EQP_NO " 
			+ " FROM TN_CM_ALRM_FIL_TAG A, TN_CM_EQP B " 
			+ " WHERE A.CHILD_EQP_NO = B.EQP_NO "
			+ " AND A.SITE_CODE = :site_code"
			+ " AND A.SYS_CODE = :sys_code"
			+ " AND B.PJT_ID = :pjt_id ) C "
		+ " WHERE A.PARENT_EQP_NO = B.EQP_NO"
		+ " AND A.CHILD_EQP_NO = C.EQP_NO"
		+ " AND A.SITE_CODE = :site_code"
		+ " AND A.SYS_CODE = :sys_code"
		+ " AND B.USE_YN = 'Y'"
		+ " AND B.PJT_ID = :pjt_id";
		
		//subquery binding params
		dsParams = makeDynString(site_code, sys_code, pjt_id, site_code, sys_code, pjt_id);
		
		//1-2. Inquiry of parent DP from DB
		conn_idx = get_DBConn();
		result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);	//Query 1. Inquiry of parent DP and child DP route from DB
		
		if(result == DB_ERR_NONE) //OK
		{
			map_delete_dp = map_parent_info;
			
			if(dynlen(qry_result) > 0 )
			{
				writeLog(g_script_name," Parent DP Query OK. Count = " + dynlen(qry_result) , LV_DBG1);
				writeLog(g_script_name," Parent DP Query OK. Query = " + query + ", params = " + dsParams , LV_DBG2);
			}
			else
			{
				writeLog(g_script_name," Parent DP Query NG. Count = " + dynlen(qry_result) , LV_DBG1);
				writeLog(g_script_name," Parent DP Query NG. Query = " + query + ", params = " + dsParams , LV_DBG1);
				// is_load_result = false;
			}

			//2-1. New Parent information loaded from DB --> map_new_parent
			//Save the child list information on the map with a key to the parent DP
			for(int i = 1; i <= dynlen(qry_result) ; i++)
			{
				parent_dp_name  = get_parent_name(qry_result[i][1] , value_leaf_list, map_new_parent);
				group_id = qry_result[i][2];
				child_dp_name = qry_result[i][3];
				
				//If there is a parent DP (EXIST)
				if(mappingHasKey(map_new_parent, parent_dp_name) == true)
				{
					map_child_info = map_new_parent[parent_dp_name];
					
					child_list = map_child_info[KEY_CHILD_LIST];
					dynAppend(child_list, child_dp_name);
					
					map_child_info[KEY_GROUP_ID] = group_id;
					map_child_info[KEY_CHILD_LIST] = child_list;
					
					map_new_parent[parent_dp_name] = map_child_info;
				}
				else //If you do not have a parent DP (NEW)
				{
					child_list = makeDynString(child_dp_name);
					
					map_child_info[KEY_GROUP_ID] = group_id;
					map_child_info[KEY_CHILD_LIST] = child_list;
					
					map_new_parent[parent_dp_name] = map_child_info;
				}
			}
			
			//2-2. DpConnect or dpDisConnect by comparing the existing Parent DP and the new Parent DP
			for(int i = 1; i <= mappinglen(map_new_parent) ; i++)
			{
				parent_dp_name = mappingGetKey(map_new_parent, i);
				
				//2-3. Check if there is an existing Parent DP
				if(mappingHasKey(map_delete_dp, parent_dp_name) == true)
				{
					//Exist
					check_child_info(map_parent_info[parent_dp_name], map_new_parent[parent_dp_name], parent_dp_name);	//check child list (old and new)
					map_parent_info[parent_dp_name] = map_new_parent[parent_dp_name];	//eqp 번호만 변경된 경우를 위해 필요
					mappingRemove(map_delete_dp, parent_dp_name);						//Only the parent DP to be deleted remains on the map(map_delete_dp).
				}
				else
				{
					//New
					if(dpExists(parent_dp_name) == true)
					{
						rs = dpConnect("CB_parent_status", parent_dp_name);
						
						//2-4. If DP connection is successful, save to map memory
						if(!rs)
						{
							connect_count++;
							map_parent_info[parent_dp_name] = map_new_parent[parent_dp_name];
							writeLog(g_script_name," Parent DP monitoring(dpConnect) Success. DP Name = " + parent_dp_name + ", " + connect_count + "/" + mappinglen(map_new_parent), LV_INFO);
						}
						else
						{
							update_user_alarm(manager_dpname , " Parent DP monitoring(dpConnect) failed. DP Name = " + parent_dp_name);
						}
					}
					else
					{
						update_user_alarm(manager_dpname , "parent dp Load - This parent DP does not exist on the server. DP Name = " + parent_dp_name);
					}
				}
			}

			//3. The deleted Parent DP performs dpDisConnect.
			for(int i = 1 ; i <= mappinglen(map_delete_dp) ; i++)
			{
				parent_dp_name = mappingGetKey(map_delete_dp, i);
				
				// TAG가 있는 경우에만 dpConnect 끊는 Logic 추가 (v1.05_2021.07.05)
				rs = 0;
				if(dpExists(parent_dp_name) == true)
				{				
					rs = dpDisconnect("CB_parent_status", parent_dp_name);
				}
				
				if(!rs)
				{
					writeLog(g_script_name,"The connection of the existing DP parents were released. DP Name = " + parent_dp_name, LV_INFO);
					mappingRemove(map_parent_stauts, parent_dp_name);
					mappingRemove(map_parent_info, parent_dp_name);
				}
				else
				{
					if(dpExists(parent_dp_name) == true)
					{
						writeLog(g_script_name,"The connection of the existing parent DP has failed to release. DP Name = " + parent_dp_name, LV_WARN);
						
					}
					else
					{
						writeLog(g_script_name,"It has already been deleted from the server.. DP Name = " + parent_dp_name, LV_WARN);
						mappingRemove(map_parent_info, parent_dp_name);
					}
				}
				
				delay(0,1);
			}
		}
		else if(result == DB_ERR_QUERY) // Query Fail
		{
			update_user_alarm(manager_dpname , "load_parent_info() - Query fail = " + query +", " + dsParams);
			is_load_result = false;
		}
		else
		{
			update_user_alarm(manager_dpname , "load_parent_info() - DB Connection Error");
			create_DBConnPool();
			is_load_result = false;
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of load_parent_info(). Error = " + getLastException());
		is_load_result = false;
	}
	finally
	{
		if(conn_idx > 0)
			release_DBConn(conn_idx);
		
		return is_load_result;
	}
}

//*******************************************************************************
// name         : get_parent_name
// argument     : dp_name(Parent DP name of the TN_CM_ALRM_FIL_TAG table), value_leaf_list(config)
// return value : string
// date         : 2020-06-09
// developed by : Ino-Group
// brief        : If the value leaf of DP is set to multiple in the config file, check the dpe name
//*******************************************************************************
string get_parent_name(string dp_name, dyn_string value_leaf_list, const mapping& in_map_parent_info)
{
	string parent_name, tmp_parent_name ;
	
	try
	{
		//1. When set to 1 in config
		if(dynlen(value_leaf_list) == 1)
			parent_name = dp_name + value_leaf_list[1];
		else
		{
			for(int i = 1; i <= dynlen(value_leaf_list) ; i++)
			{
				tmp_parent_name = dp_name + value_leaf_list[i];
				
				//2. Check DPE name among multiple value leafs
				if(mappingHasKey(in_map_parent_info, tmp_parent_name) == true)
				{
					parent_name = tmp_parent_name;
				}
				else if(dpExists(tmp_parent_name) == true)
				{
					parent_name = tmp_parent_name;
					break;
				}
			}
			
			if(strlen(parent_name) == 0)
				update_user_alarm(manager_dpname , "The parent dp cannot be found on the server. dp name = " + dp_name);
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of get_parent_name(). Error = " + getLastException());
	}
	finally
	{
		return parent_name; 
	}
}

//*******************************************************************************
// name         : check_child_info
// argument     : map_old_child_info(Old parent dp information), map_old_child_info(reload the parent dp information), parent_name
// return value : void
// date         : 2020-06-09
// developed by : Ino-Group
// brief        : Check if child information has been changed when DB is reloaded
//*******************************************************************************
void check_child_info(const mapping& map_old_child_info, const mapping& map_new_child_info, string parent_name)
{
	string dp_name;
	dyn_string old_child_list, new_child_list;
	anytype parent_status;
	int rs;
	
	try
	{
		old_child_list = map_old_child_info[KEY_CHILD_LIST];
		new_child_list = map_new_child_info[KEY_CHILD_LIST];
		
		if(old_child_list != new_child_list)
		{
			if(!dpGet(parent_name , parent_status))	//OK
			{
				dp_name = dpSubStr(parent_name, DPSUB_DP_EL);
				map_parent_queue[dp_name] = parent_status;
				writeLog(g_script_name,"Change child DP. Parent DP =  " + parent_name, LV_DBG2);
			}
			else	//NG
			{
				update_user_alarm(manager_dpname , "Failed to check parent DP value. Parent DP = " + parent_name);
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of check_child_info(). Error = " + getLastException());
	}
}
//*******************************************************************************
// name         : get_pjt_condition
// argument     : 
// return value : string
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Create where clause
//*******************************************************************************
string get_pjt_condition(dyn_string pjt_list)
{
	const string param = ":pjt" ;
	string query_condition;
	try
	{
		//Create where clause condition when there are multiple pjt names in config option
		for(int i = 1; i <= dynlen(pjt_list); i++)
		{
			query_condition += param + i;
			
			if(i != dynlen(pjt_list))
			{
				query_condition += ", ";
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of get_pjt_condition(). Error = " + getLastException());
	}
	finally
	{
		return query_condition;
	}
}

//*******************************************************************************
// name         : CB_reload
// argument     : userData(User-defined data), Reload DP
// return value : void
// date         : 2020-04-10
// developed by : Ino-Group
// brief        : Relaod DP monitoring
//*******************************************************************************
void CB_reload(string dp_name, bool value)
{
	try
	{
		reload_flag = value;
		writeLog(g_script_name,"Change Reload DP. DP Name =  " + dp_name + ", changed value = " + value, LV_INFO);
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of CB_reload(). Error = " + getLastException());
	}
}

//*******************************************************************************
// name         : CB_parent_status
// argument     : userData(User-defined data), Reload DP
// return value : void
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Parent DP monitoring
//*******************************************************************************
void CB_parent_status(string dp_name, anytype value)
{
	bool parent_value ;
	try
	{
		synchronized(map_parent_queue)
		{
			// When the DP is changed, it is stored in Q and processed by the Thread function.
			dp_name = dpSubStr(dp_name, DPSUB_DP_EL);
			parent_value = (bool) value;
			
			//parent_value가 동일한 값으로 변경되는 경우 -> update_alarm_active 함수에서 처리 되지 않도록 수정(2021.03.30)
			if( (mappingHasKey(map_parent_stauts, dp_name) == true && map_parent_stauts[dp_name] != parent_value)
			|| mappingHasKey(map_parent_stauts, dp_name) == false)
			{
				map_parent_queue[dp_name] = parent_value;
				map_parent_stauts[dp_name] = parent_value;
			}
			else
			{
				writeLog(g_script_name,"Parent DP value is changed to the same value. DP Name =  " + dp_name + ", changed value = " + value, LV_DBG2);
			}
			
			writeLog(g_script_name,"Change Parent DP Status. DP Name =  " + dp_name + ", changed value = " + value, LV_DBG2);
		}
	}
	catch
	{
		update_user_alarm(manager_dpname , "Exception of CB_parent_status(). Error = " + getLastException());
	}
}


//*******************************************************************************
// name         : update_alarm_active
// argument     : 
// return value : bool
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Change the alarm activation status of the child DPs of the changed parent DP
//*******************************************************************************
void update_alarm_active()
{
	bool is_result;
	bool parent_status;
	
	string parent_dp_name;
	dyn_string child_dp_list;
	string group_id;
	
	mapping map_child_info, map_error_parent;
	int rs;
	
	while(true)
	{
		try
		{
			if(isScriptActive == true)
			{
				update_heartbeat(manager_dpname);	//Script Monitoring and Control
			}
			
			//1. Check if Parent DP structure has been changed
			if(reload_flag == true)
			{
				synchronized(map_parent_queue)
				{					
					//1-1. Parent DP importing from DB stored in the memory and dpConnect
					is_result = load_parent_info();
					
					//1-2. Reload flag is changed to false after Parent DP inquiry
					if(is_result == true)
					{
						writeLog(g_script_name,"update_alarm_active() - Parent DP Load Success. Parent DP Count = " + mappinglen(map_parent_info), LV_INFO);
						
						rs = dpSet(reload_dp , false);
				
						if(!rs)
						{
							reload_flag = false;
							writeLog(g_script_name,"update_alarm_active() - Reload DP Changed to False - Success. DP Name = " + reload_dp, LV_INFO);
						}
						else
						{
							update_user_alarm(manager_dpname , "update_alarm_active() - Reload DP Changed to False - failed. DP Name = " + reload_dp);
						}
					}
					else
					{
						update_user_alarm(manager_dpname ,"update_alarm_active() - Parent DP Load Failed");
					}
				}
				
				writeLog(g_script_name,"update_alarm_active() - ContactCutOut Reload Completed", LV_INFO);
			}
			
			//2. Check if Parent DP has been changed
			synchronized(map_parent_queue)
			{
				mappingClear(map_error_parent);
				
				for(int i = 1; i <= mappinglen(map_parent_queue) ; i++)
				{
					dynClear(child_dp_list);
					parent_dp_name = mappingGetKey(map_parent_queue, i);
					parent_status = mappingGetValue(map_parent_queue, i);
					
					//3. Query child list and group ID information from memory(map_parent_info)
					if(mappingHasKey(map_parent_info, parent_dp_name ) == true)
					{
						map_child_info = map_parent_info[parent_dp_name];
						child_dp_list = map_child_info[KEY_CHILD_LIST];
						group_id = map_child_info[KEY_GROUP_ID];
					
						writeLog(g_script_name,"update_alarm_active() - Change Parent DP. Parent DP = " + parent_dp_name, LV_DBG2);
					}
					else
					{
						update_user_alarm(manager_dpname ,"update_alarm_active() - There is no changed Parnet DP information.. Parent DP = " + parent_dp_name);
						continue;
					}

					if(dynlen(child_dp_list) == 0)
					{
						writeLog(g_script_name,"update_alarm_active() - The child DP does not exist in the mamory.. Parent DP = " + parent_dp_name, LV_WARN);
						continue;
					}
					if(isScriptActive == true)
					{
						//4-1. Child DP Alarm Active (_alert_hdl.._min_prio - 50)
						if(parent_status == true)
						{
							if(set_alarm_acitve(child_dp_list, group_id) == true)
							{
								writeLog(g_script_name,"update_alarm_active() - Parent DP Alarm Active Success. Parent DP = " + parent_dp_name, LV_DBG1);
							}
							else
							{
								map_error_parent[parent_dp_name] = parent_status;
								update_user_alarm(manager_dpname , "update_alarm_active() - Parent DP Alarm active Fail. Parent DP = " + parent_dp_name);
							}						
						}
						//4-2. Child DP Alarm UnActive (_alert_hdl.._min_prio + 50)
						else
						{
							if(set_alarm_unacitve(child_dp_list, group_id) == true)
							{
								writeLog(g_script_name,"update_alarm_active() - Parent DP Alarm Unactive Success. Parent DP = " + parent_dp_name, LV_DBG1);
							}
							else
							{
								map_error_parent[parent_dp_name] = parent_status;
								update_user_alarm(manager_dpname , "update_alarm_active() - Parent DP Alarm Unactive Fail. Parent DP = " + parent_dp_name);
							}
						}
						
						writeLog(g_script_name, "update_alarm_active() - Alarm Active-Unactive processing... Parent DP = " + parent_dp_name + ", " + i + "/" +  mappinglen(map_parent_queue), LV_DBG1);
					}
					delay(0,1);
				}///for
				
				if(mappinglen(map_error_parent) == 0 )
				{
					mappingClear(map_parent_queue);
				}
				else
				{
					update_user_alarm(manager_dpname , "update_alarm_active() - There is a Parent DP whose processing is in error. Count = " + mappinglen(map_error_parent));
					writeLog(g_script_name,"update_alarm_active() - Error Parent DP -> " + map_error_parent, LV_WARN);
					map_parent_queue = map_error_parent;
				}
			}
			
			writeLog(g_script_name,"update_alarm_active() - ContactCutOut Action Logic Thread Completed", LV_DBG2);
			
		}
		catch
		{
			update_user_alarm(manager_dpname ,"Exception of update_alarm_active(). Error = " + getLastException());
		}
		finally
		{
			delay_cycle(1);
		}
	}
	
}

//*******************************************************************************
// name         : update_alarm_active
// argument     : 
// return value : bool
// date         : 2020-04-27
// developed by : Ino-Group
// brief        : Check if the parent DP that is running CCO is on the server
//*******************************************************************************
void check_running_parent()
{
	string query, set_time;
	bool is_result, reload_flag	;
	
	dyn_dyn_anytype qry_result; 
	int conn_idx, result, connect_count = 0;
	
	string parent_dp_name, parent_dp_name_pvlast, parent_eqp_no, group_id, child_dp_name ;
	dyn_string dsParams, child_list;
	
	mapping map_unactvie_parent_info, map_child_info;
	
	time tNow;
	int rs;
	
	while(true)
	{
		try
		{
			if(isScriptActive == true)
			{
				query = "SELECT /*ContactCutOut.ctl-20200427-SIT*/ EQP.EQP_NO \"parent_eqp_no\", EQP.EQP_NAME \"parent_name\", FIL_TAG.ALRM_FIL_GROUP_ID , SUB.EQP_NAME \"child_name\""
				+ " FROM TN_CM_ALRM_FIL_TAG FIL_TAG, TN_CM_EQP EQP, ("
					+ " SELECT B.CHILD_EQP_NO, A.EQP_NAME"
					+ " FROM TN_CM_EQP A, TN_CM_ALRM_FIL_TAG B, TH_CM_ALRM_FIL_CCO C"
					+ " WHERE C.END_DATE IS NULL"
					+ " AND B.ALRM_FIL_GROUP_ID = C.ALRM_FIL_GROUP_ID"
					+ " AND A.EQP_NO = B.CHILD_EQP_NO"
					+ " AND A.SITE_CODE = :site_code"
					+ " AND A.SYS_CODE = :sys_code"
					+ " AND A.PJT_ID = :pjt_id"
				+ " ) SUB "
				+ " WHERE FIL_TAG.parent_eqp_no = EQP.EQP_NO"
				+ " AND FIL_TAG.CHILD_EQP_NO =  SUB.CHILD_EQP_NO";
				
				//binding info : site_code, sys_code
				dsParams = makeDynString(site_code, sys_code, pjt_id);
										
				// 1-1. Parent DP search in UnActive progressing
				conn_idx = get_DBConn();
				result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], query, dsParams, qry_result);	//Query 5. Check if the parent DP running CCO is on the server
				if(conn_idx > 0)
				{
					release_DBConn(conn_idx);
					conn_idx = 0;
				}
				
				// 1-2. Save the CCO parents DP map found at DB
				if(result == DB_ERR_NONE) //OK
				{
					for(int i = 1; i <= dynlen(qry_result) ; i++)
					{
						parent_eqp_no = qry_result[i][1];
						parent_dp_name = qry_result[i][2];
						group_id = qry_result[i][3];
						child_dp_name = qry_result[i][4];
						
						//Save the child list information on the map with a key to the parent DP
						//END_DATE이 Null인 경우의 부모 Tag를 map에 저장
						if(mappingHasKey(map_unactvie_parent_info, parent_dp_name) == true)
						{
							map_child_info = map_unactvie_parent_info[parent_dp_name];
							
							child_list = map_child_info[KEY_CHILD_LIST];
							dynAppend(child_list, child_dp_name);
							
							map_child_info[KEY_GROUP_ID] = group_id;
							map_child_info[KEY_CHILD_LIST] = child_list;
							map_child_info[KEY_PARENT_EQP_NO] = parent_eqp_no;
							
							map_unactvie_parent_info[parent_dp_name] = map_child_info ;
						}
						else
						{
							child_list = makeDynString(child_dp_name);
												
							map_child_info[KEY_GROUP_ID] = group_id;
							map_child_info[KEY_CHILD_LIST] = child_list;
							map_child_info[KEY_PARENT_EQP_NO] = parent_eqp_no;
							
							map_unactvie_parent_info[parent_dp_name] = map_child_info ;
						}
					}
					
					//2.CCO parent DP checks on server
					reload_flag = false;
					for(int i = 1; i <= mappinglen(map_unactvie_parent_info) ; i++)
					{
						parent_dp_name = mappingGetKey(map_unactvie_parent_info, i);
						
						if(dpExists(parent_dp_name) == true)
						{
							writeLog(g_script_name,"check_running_parent() - Check UnActive Parent DP in Server - OK. Parent DP = " + parent_dp_name , LV_DBG2);
						}
						else
						{
							reload_flag = true;
							update_user_alarm(manager_dpname , "check_running_parent() - Check UnActive Parent DP in Server - It has been deleted from the server. Parent DP = " + parent_dp_name );
							
							map_child_info = mappingGetValue(map_unactvie_parent_info, i);
							child_list = map_child_info[KEY_CHILD_LIST];
							group_id = map_child_info[KEY_GROUP_ID];
							parent_eqp_no = map_child_info[KEY_PARENT_EQP_NO];

							//2-1. Change Child DP to Acitve + END_DATE Update
							bool result_active ;
							
							synchronized(map_parent_queue)
							{
								result_active = set_alarm_acitve(child_list, group_id) ;
							}
							
							//2-2. Child DP Acitve 처리 후 DB 데이터 처리 : TN_CM_ALRM_FIL_TAG, TH_CM_ALRM_FIL_MOD 테이블 변경
							if(result_active == true)
							{
								writeLog(g_script_name,"check_running_parent() - Parent DP Alarm Active Success. Parent DP = " + parent_dp_name, LV_DBG1);

								//2-3. Update to parent DP Null value in TN_CM_ALRM_FIL_TAG Table
								query = " Update TN_CM_ALRM_FIL_TAG"
								+ " SET PARENT_EQP_NO = NULL"
								+ " WHERE SITE_CODE = :site_code"
								+ " AND SYS_CODE = :sys_code"
								+ " AND PARENT_EQP_NO = :parent_eqp_no" ;
								
								dsParams = makeDynString(site_code, sys_code, parent_eqp_no);
								queryQueue_append(query, dsParams);		//Query 5. Delete the parent DP not in the server from the DB (TN_CM_ALRM_FIL_TAG Table)

								//2-4. Save TH_CM_ALRM_FIL_MOD Table exception handling history if there is no parent DP --> TH_CM_ALRM_FIL_MOD
								query = "INSERT /*ContactCutOut.ctl-20200427-SIT*/ " 
								+ " INTO TH_CM_ALRM_FIL_MOD(HIST_SEQ, EVENT_OCCUR_DATE, SYS_CODE, SITE_CODE, ALRM_FIL_GROUP_ID, CHG_ITEM_CONT, CHG_CONT, BEFORE_VAL, USER_ID)"
								+ " VALUES (SQ_CM_ALRM_FIL_MOD.NEXTVAL, TO_DATE(:set_date, 'YYYY.MM.DD HH24:MI:SS'), :sys_code, :site_code, :group_id, :chid_dp, 'PARENT_TAG', :parent_dp, 'SYSTEM') ";
								
								tNow = getCurrentTime();
								set_time = formatTime("%Y/%m/%d %H:%M:%S", tNow);
								
								for(int j = 1 ; j <= dynlen(child_list) ; j++)
								{
									dsParams = makeDynString(set_time, sys_code, site_code, group_id , child_list[j], parent_dp_name);
									queryQueue_append(query, dsParams);		//Query 6. Insert a parent DP delete history (TH_CM_ALRM_FIL_MOD Table)
								}
							
								delay(0,100);
							}
							else
							{
								update_user_alarm(manager_dpname , "check_running_parent() - Parent DP Alarm Unactive Fail. Parent DP = " + parent_dp_name);
							}
						}
						
						delay(0,1);
						
					}	//for
					
					//2-5. ContactCutOut 기준 정보 ReLoad					
					if(reload_flag == true)
					{
						reload_flag = false;
						
						synchronized(map_parent_queue)
						{
							if(load_parent_info() == true)
							{
								writeLog(g_script_name,"check_running_parent() - Parent DP Load Success. Parent DP Count = " + mappinglen(map_parent_info), LV_INFO);
							}
							else
							{
								update_user_alarm(manager_dpname ,"check_running_parent() - Parent DP Load Failed");
							}
						}
					}
					
					mappingClear(map_unactvie_parent_info);
				}
				else if(result == DB_ERR_QUERY) // Query Fail
				{
					update_user_alarm(manager_dpname , "check_running_parent() - Query fail = " + query +", " + dsParams);
				}
				else
				{
					update_user_alarm(manager_dpname , "check_running_parent() - DB Connection Error ");
					create_DBConnPool();
				}
				
				writeLog(g_script_name,"check_running_parent() - Active server thread operation completed", LV_DBG2);
			}
			
			writeLog(g_script_name,"check_running_parent() - Check completion of thread operation", LV_DBG2);
		}
		catch
		{
			update_user_alarm(manager_dpname ,"Exception of check_running_parent(). Error = " + getLastException());
		}
		finally
		{
			if(conn_idx > 0)
				release_DBConn(conn_idx);
			delay(delay_check_parent);
		}
	}
}

//*******************************************************************************
// name         : set_alarm_acitve
// argument     : child_list, group_id
// return value : bool
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Change the min prio value of the child DP list to the alarm active value.(-50)
//*******************************************************************************
bool set_alarm_acitve(const dyn_string& child_list, const string& group_id )
{
	dyn_string alert_list;
	dyn_int min_prio;
	int tmp_min_prio;
	
	dyn_string set_dp_names;
	dyn_int set_values;
	
	string update_query, end_time ;
	dyn_anytype dsParams ;
	time tNow;
	
	bool is_set_result = true;
	
	try
	{
		for(int i = 1 ; i <= dynlen(child_list); i++)
		{
			//1. Check alarm list of child DP
			alert_list = dpNames(child_list[i] + ".alert.*");
			
			if(dynlen(alert_list) == 0)
			{
				writeLog(g_script_name,"There is no DP alarm list. child DP = " + child_list[i] , LV_WARN);
				continue;
			}
			
			for(int k = 1 ; k <= dynlen(alert_list) ; k++)
				alert_list[k] = alert_list[k] + ":_alert_hdl.._min_prio";

			rs = dpGet(alert_list, min_prio);
			
			if(!rs)
			{
				writeLog(g_script_name,"set_alarm_acitve() - min_prio dpGet Success, alert_list = " + alert_list + ", min_prio list = " + min_prio, LV_DBG2);
				
				//2. Check the alarm's min_prio value
				for(int j = 1 ; j <= dynlen(alert_list) ; j++)
				{
					if(dynlen(min_prio) == j)
					{
						tmp_min_prio = min_prio[j];
					}
					else
					{
						tmp_min_prio = -1;
						dpGet(alert_list[j], tmp_min_prio);
					}
					
					//3. The min_prio value is changed to -50 only when the alarm is disabled.
					if( tmp_min_prio == CCO_MODE || tmp_min_prio == CCO_PMMODE_MODE)
					{
						tmp_min_prio = tmp_min_prio - MIN_PRIO_VALUE;
						dynAppend(set_dp_names, alert_list[j]);
						dynAppend(set_values, tmp_min_prio);
					}
				}
			}
			else
			{
				writeLog(g_script_name,"set_alarm_acitve() - dpGet Error, alert_list = " + alert_list, LV_WARN);
				is_set_result = false;
				continue;
			}
		}	
			
		//4. Update DP stored in array
		writeLog(g_script_name,"set_alarm_acitve() - Update Request : " + dynlen(set_dp_names), LV_DBG1);
		if( dynlen(set_dp_names) > 0)
		{
			if(!dpSetTimed(0, set_dp_names, set_values))
			{
				writeLog(g_script_name,"set_alarm_acitve() - change min_prio(-50) Success. \n set_dp_list " + set_dp_names + " \n set_value_list = " + set_values, LV_DBG2);
				
				update_query = "UPDATE /*ContactCutOut.ctl-20200427-SIT*/ TH_CM_ALRM_FIL_CCO" 
				+ " SET END_DATE = TO_DATE(:end_time, 'YYYY.MM.DD HH24:MI:SS')"
				+ " WHERE END_DATE IS NULL"
				+ " AND SITE_CODE = :site_code"
				+ " AND SYS_CODE = :sys_code"
				+ " AND ALRM_FIL_GROUP_ID = :group_id";
				
				tNow = getCurrentTime();
				end_time = formatTime("%Y/%m/%d %H:%M:%S", tNow);
				
				dsParams = makeDynString(end_time, site_code, sys_code, group_id);
				queryQueue_append(update_query, dsParams);		//Query 4. Update CCO release history to DB
			}
			else
			{
				is_set_result = false;
				writeLog(g_script_name,"set_alarm_acitve() - change min_prio(-50) Fail. ", LV_WARN);
			}
		}
	}
	catch
	{
		update_user_alarm(manager_dpname ,"Exception of set_alarm_acitve(). Error = " + getLastException());
	}
	finally
	{
		return is_set_result;
	}
}


//*******************************************************************************
// name         : set_alarm_unacitve
// argument     : child_list, group_id
// return value : bool
// date         : 2020-04-20
// developed by : Ino-Group
// brief        : Change the min prio value of the child DP list to the alarm unactive value.(+50)
//*******************************************************************************
bool set_alarm_unacitve(const dyn_string& child_list, const string& group_id )
{
	dyn_string alert_list;
	dyn_int min_prio;
	int tmp_min_prio;
	
	dyn_string set_dp_names;
	dyn_int set_values;
	time tNow;
		
	string select_query, insert_query, set_time ;
	dyn_anytype dsParams ;
	dyn_dyn_anytype qry_result; 
		
	bool is_set_result = true;
	int conn_idx, result;

	try
	{
		for(int i = 1 ; i <= dynlen(child_list); i++)
		{
			//1. Check alarm list of child DP
			alert_list = dpNames(child_list[i] + ".alert.*");
			
			if(dynlen(alert_list) == 0)
			{
				writeLog(g_script_name,"There is no DP alarm list. child DP = " + child_list[i] , LV_WARN);
				continue;
			}

			for(int k = 1 ; k <= dynlen(alert_list) ; k++)
				alert_list[k] = alert_list[k] + ":_alert_hdl.._min_prio";

			rs = dpGet(alert_list, min_prio);
			
			if(!rs)
			{
				writeLog(g_script_name,"set_alarm_unacitve() - dpGet Success, alert_list = " + alert_list + ", min_prio list = " + min_prio, LV_DBG2);
				
				//2. Check the alarm's min_prio value
				for(int j = 1 ; j <= dynlen(alert_list) ; j++)
				{
					
					if(dynlen(min_prio) == j)
						tmp_min_prio = min_prio[j];
					else
					{
						tmp_min_prio = -1;
						dpGet(alert_list[j], tmp_min_prio);
					}
					
					//3. The min_prio value is changed to +50 only when the alarm is disabled.
					if( tmp_min_prio == ACTIVE_MODE || tmp_min_prio == ACTIVE_PMMODE_MODE)
					{
						tmp_min_prio = tmp_min_prio + MIN_PRIO_VALUE;
						dynAppend(set_dp_names, alert_list[j]);
						dynAppend(set_values, tmp_min_prio);
						
					}
				}
			}
			else
			{
				writeLog(g_script_name,"set_alarm_unacitve() - dpGet Error, alert_list = " + alert_list, LV_WARN);
				is_set_result = false;
				continue;
			}
		}	
			
		//4. Update DP stored in array
		writeLog(g_script_name,"set_alarm_unacitve() - Update Request : " + dynlen(set_dp_names), LV_DBG1);
		
		if(dynlen(set_dp_names) > 0)
		{
			if(!dpSetTimed(0, set_dp_names, set_values))
			{
				writeLog(g_script_name,"set_alarm_unacitve() - change min_prio(+50) Success. \n set_dp_list " + set_dp_names + " \n set_value_list = " + set_values, LV_DBG2);
			}
			else
			{
				is_set_result = false;
				writeLog(g_script_name,"set_alarm_unacitve() - change min_prio(+50) Fail. \n set_dp_list " + set_dp_names + " \n set_value_list = " + set_values, LV_WARN);
			}
		}
		
		//5. CCO Insert
		select_query = "SELECT /*ContactCutOut.ctl-20200427-SIT*/ SET_DATE "
				+ " FROM TH_CM_ALRM_FIL_CCO"
				+ " WHERE END_DATE IS NULL"
				+ " AND SITE_CODE = :site_code"
				+ " AND SYS_CODE = :sys_code"
				+ " AND ALRM_FIL_GROUP_ID = :group_id";
				
		dsParams = makeDynString(site_code, sys_code, group_id);

		//4-1 Check if group id record exists in DB table
		conn_idx = get_DBConn();
		result = rdbSelectSingle_Bind(g_dbConn_pool[conn_idx], select_query, dsParams, qry_result);		//Query 2. Check in the DB to see if there is a parent DP with CCO status
		
		if(result == DB_ERR_NONE) //OK
		{
			if(dynlen(qry_result) == 0)
			{
				insert_query = "INSERT /*ContactCutOut.ctl-20200427-SIT*/ " 
				+ " INTO TH_CM_ALRM_FIL_CCO(ALRM_FIL_GROUP_ID, SET_DATE, SITE_CODE, SYS_CODE)"
				+ " VALUES (:group_id, TO_DATE(:set_date, 'YYYY.MM.DD HH24:MI:SS'), :site_code, :sys_code)" ;
				
				tNow = getCurrentTime();
				set_time = formatTime("%Y/%m/%d %H:%M:%S", tNow);
				
				dsParams = makeDynString(group_id, set_time, site_code, sys_code);
				queryQueue_append(insert_query, dsParams);		//Query 3. Insert CCO status occurrence history into DB
			}
		}		
		else if(result == DB_ERR_QUERY) // Query Fail
		{
			writeLog(g_script_name,"set_alarm_unacitve() - Query fail = " + select_query +", " + dsParams, LV_WARN);
			is_set_result = false;
		}
		else
		{
			writeLog(g_script_name,"set_alarm_unacitve() - DB Connection Error ", LV_WARN);
			create_DBConnPool();
			is_set_result = false;
		}
	}
	catch
	{
		update_user_alarm(manager_dpname ,"Exception of set_alarm_unacitve(). Error = " + getLastException());
	}
	finally
	{
		if(conn_idx > 0)
			release_DBConn(conn_idx);
			
		return is_set_result;
	}
}
