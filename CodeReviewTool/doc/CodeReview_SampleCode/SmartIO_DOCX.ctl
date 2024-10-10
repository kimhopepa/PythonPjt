//v1.0(2024.10.10)
//1.First Version
#uses "CtrlADO"
#uses "dist.ctl"
#uses "hosts.ctl"
#uses "library_standard.ctl"

//---------------------------------------------
// configuration path & filename
//---------------------------------------------
string script_path;      //getPath(SCRIPTS_REL_PATH);
string config_filename;
const string g_script_release_version = "v1.0";
const string g_script_release_date = "2024.10.10";
const string g_script_name = "SmartIO_DOCX";
string manager_dpname = "";
//---------------------------------------------
// general option
//---------------------------------------------
string ScriptActive_Condition = "ACTIVE";  //|BOTH|HOST1|HOST2";
int cfg_query_blocking_time = 500;

dyn_string cfg_dp_type_list;
string cfg_opman_para, cfg_opauto_para, cfg_on_command_alm_para, cfg_opsource_para, cfg_opmomdlytm_para, cfg_cmdchktm_para;
string cfg_cx_para;
string cfg_pvlast_para, cfg_oplast_para;

string cfg_source_filter, cfg_target_filter;

// �˶� ���� �� �޸� ����
mapping g_map_alarm	;		// ON, OFF �˶� ���� ����
mapping g_map_thread_key ;	// ���� ���� ���� DP�� Thread ID�� ����
mapping g_map_cmd ;  // CMD ���� ����
mapping g_map_value ;  // OPAUTO, OPMAN VALUE ����

const string ctrl_manager = "CTRL";

//�ڵ�, ����
const bool SOURCE_AUTO = false;
const bool SOURCE_MANUAL = true;

// CMD Setting Case
const int TYPE_AUTO_CXST_ON = 1;		// �ڵ� ON
const int TYPE_AUTO_CXST_OFF = 2;		// �ڵ� OFF
const int TYPE_AUTO_CXONLY = 3;			// �ڵ� (ST ���� ���)
const int TYPE_MANUAL_CXST_ON = 4;
const int TYPE_MANUAL_CXST_OFF = 5;
const int TYPE_MANUAL_CXONLY = 6;

const int OPMOMDLYTM_DEFAULT = 3;

//*******************************************************************************
// name         : main
// argument     :
// return value :
// date         : 2021-11-19
// developed by : INNO Team
// brief        : Main Logic
//*******************************************************************************
void main()
{
    string query, from_query, where_query;
    dyn_dyn_anytype tbval;

    try
    {
        //1. ǥ�� ��ũ��Ʈ �ʱ�ȭ ���� ���� : ���� �α�, ����� Flag, Manager DP üũ, ����ȭ ���� ����, �˶� �ʱ�ȭ
        if(init_standard_script() == 0)
        {
            writeLog(g_script_name, "1. init standard script : OK", LV_INFO);
        }
        else
        {
            writeLog(g_script_name, "1. init standard script : NG", LV_ERR);
            exit();
        }

        delay(1);

        init_user_alarm(manager_dpname);	//Reset user User-defined alarm to OFF

        //----------------------------------
        // 2. Initialize (Load the Config)
        //----------------------------------
        if (load_config() == false)
        {
            update_user_alarm(manager_dpname, "1. Initialize(Load the Config) : NG");
            exit();
        }
        else
        {
            writeLog(g_script_name, "1. Initialize(Load the Config) : OK", LV_INFO);
        }

        //3. Alarm State, Cmd Vaule, OPValue �޸� ����
        // DPTYPE ������ �ٸ��� �����Ƿ�, �ʼ��Ķ���Ͱ� ���ų�, Default �� Ȯ��
        for(int i = 1; i <= dynlen(cfg_dp_type_list); i++)
        {
            string dp_type = cfg_dp_type_list[i];
            query = "SELECT '_online.._value' FROM " + str_from(makeDynString(cfg_on_command_alm_para, cfg_oplast_para, cfg_opman_para, cfg_opauto_para, cfg_opsource_para, cfg_opmomdlytm_para, cfg_cmdchktm_para)) + " WHERE " + str_where(dp_type);

            if (init_mapping(query) == true)
            {
                writeLog(g_script_name, "3. init_mapping() - init_mapping Load OK. query = " + query, LV_INFO);
            }
            else
            {
                writeLog(g_script_name, "3. init_mapping() - init_mapping Load NG. query = " + query, LV_ERR);
                exit();
            }
        }

        //4-1. OPSOURCE, OPMOMDLYTM, CMDCHKTM ���� ����
        query = "SELECT '_online.._value' FROM " + str_from(makeDynString(cfg_opsource_para, cfg_opmomdlytm_para, cfg_cmdchktm_para)) + " WHERE " + str_where(cfg_dp_type_list);

        //TODO : [����] dpQueryConnectSingle �Ű����� �ϵ� �ڵ� ���� 500 -> cfg_query_blocking_time
        if (dpQueryConnectSingle("CB_cmd", false, "", query, 500) == 0)
        {
            writeLog(g_script_name, "4. CB_cmd() Callback OK. query = " + query, LV_INFO);
        }
        else
        {
            writeLog(g_script_name, "4. CB_cmd() Callback NG. query = " + query, LV_ERR);
            exit();
        }

        //4-2. OPMAN, OPAUTO ���� ����
        query = "SELECT '_online.._value' FROM " + str_from(makeDynString(cfg_opman_para, cfg_opauto_para)) + " WHERE " + str_where(cfg_dp_type_list);

        //TODO : [����] dpQueryConnectSingle �Ű����� �ϵ� �ڵ� ���� 500 -> cfg_query_blocking_time
        if (dpQueryConnectSingle("CB_value", false, "", query, 500) == 0)
        {
            writeLog(g_script_name, "4. CB_value() Callback OK. query = " + query, LV_INFO);
        }
        else
        {
            writeLog(g_script_name, "4. CB_value() Callback NG. query = " + query, LV_ERR);
            exit();
        }

        writeLog(g_script_name, "===== Script initalize Complete =====", LV_INFO);
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of main(). Error = " + getLastException());
    }
}

//*******************************************************************************
// name         : load_config
// argument     :
// return value : (bool)config ���� Load ���
// date         : 2021-11-19
// developed by : INNO Team
// brief        : config ������ Load
//*******************************************************************************
bool load_config()
{
    bool result = true;
    string config_filename, msg;
    dyn_string tmp_list;

    try
    {
        if (globalExists("global_config_name") == TRUE)
            config_filename = global_config_name;

        // load script Path
        set_config_path(getPath(SCRIPTS_REL_PATH) + config_filename);

        //[general] -------------------------------------------------------------------
        read_config("general", "Active_Condition", ScriptActive_Condition, CFG_MODE, true);
        read_config("general", "Query_Blocking_Time", cfg_query_blocking_time, CFG_MODE, true);
        //TODO : read_config ������ �Ű����� false�� ����
        read_config("main", "DP_TYPE", cfg_dp_type_list, CFG_LIST_SEPARATOR_MODE, false);
        read_config("main", "OPMAN_PARA", cfg_opman_para, CFG_MODE, false);
        read_config("main", "OPAUTO_PARA", cfg_opauto_para, CFG_MODE, false);
        read_config("main", "OPSOURCE_PARA", cfg_opsource_para, CFG_MODE, false);
        read_config("main", "OPMOMDLYTM_PARA", cfg_opmomdlytm_para, CFG_MODE, false);
        read_config("main", "CMDCHKTM_PARA", cfg_cmdchktm_para, CFG_MODE, false);
        read_config("main", "ON_ALM_PARA", cfg_on_command_alm_para, CFG_MODE, false);
        read_config("main", "CX_PARA", cfg_cx_para, CFG_MODE, false);
        read_config("main", "CX_DPNAME", cfg_source_filter, CFG_MODE, false);
        read_config("main", "ST_DPNAME", cfg_target_filter, CFG_MODE, false);
        read_config("main", "PVLAST_PARA", cfg_pvlast_para, CFG_MODE, false);
        read_config("main", "OPLAST_PARA", cfg_oplast_para, CFG_MODE, false);

        // config ���� ��ȸ ���� üũ
        if (check_config_complete() == true)
        {

            writeLog(g_script_name, "load_config() - operates normally without errors.", LV_INFO);

            //TODO : ��� ���� �ʳ�?
            if(cfg_opsource_para == "")
                writeLog(g_script_name, "load_config() - opsource config not exist -> default value = " + SOURCE_AUTO, LV_INFO);
            if(cfg_opmomdlytm_para == "")
                writeLog(g_script_name, "load_config() - opmomdlytm config not exist -> default value = " + OPMOMDLYTM_DEFAULT, LV_INFO);
        }
        else
        {
            writeLog(g_script_name, "load_config() - check_config_complete Error.", LV_ERR);
            result = false;
        }
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
        result = false;
    }
    return result;
}
//*******************************************************************************
// name         : init_mapping
// argument     : dp Query
// return value : (bool) Alarm State, CMD Value, OPValue �޸� ���� ���
// date         : 2024-10-07
// developed by : JSH
// brief        : Alarm State, CMD Value, OPValue �޸� ����
//                -> g_map_cmd, g_map_value, g_map_alarm
//*******************************************************************************
bool init_mapping(string query)
{
    bool result = true;
    dyn_dyn_anytype tbval;
    dyn_string set_dp_list, set_value_list;
    dyn_string get_dp_list, get_value_list;

    try
    {
        if (dpQuery(query, tbval) == 0)
        {
            writeLog(g_script_name, "init_alarm_status() - dpQuery Sucess. query = " + query, LV_DBG1);
        }
        else
        {
            writeLog(g_script_name, "init_alarm_status() - dpQuery Fail. query = " + query, LV_ERR);
            result = false;
        }

        for (int i = 2 ; i <= dynlen(tbval); i++)
        {
            string dp_name = dpSubStr(tbval[i][1], DPSUB_DP);
            string dpe_name = dpSubStr(tbval[i][1], DPSUB_DP_EL);
            anytype value = tbval[i][2];

            dynAppend(get_dp_list, dp_name + cfg_cx_para);

            if(strpos(dpe_name, cfg_opsource_para) > 0 || strpos(dpe_name, cfg_opmomdlytm_para) > 0 || strpos(dpe_name, cfg_cmdchktm_para) > 0)
            {
                g_map_cmd[dpe_name] = value;
            }
            else if(strpos(dpe_name, cfg_opman_para) > 0 || strpos(dpe_name, cfg_opauto_para) > 0 || strpos(dpe_name, cfg_oplast_para) > 0)
            {
                g_map_value[dpe_name] = value;
            }
            else if(strpos(dpe_name, cfg_on_command_alm_para) > 0)
            {
                g_map_alarm[dpe_name] = value;
            }
            else
            {
                writeLog(g_script_name,"init_mapping() - A value that cannot be saved. dpe_name = " +  dpe_name, LV_WARN);
                result = false;
            }
        }

        // Momentary ��� True Check
        if(isScriptActive == true && dynlen(get_dp_list) > 0)
        {
            if(dpGet_block(get_dp_list, get_value_list) == false)
            {
                writeLog(g_script_name,"init_mapping() - dpGet - NG. set_points = " + dynlen(get_dp_list) + ", get_values = " + dynlen(get_value_list), LV_ERR);
            }
            else
            {
                for(int i = 1 ; i <= dynlen(get_value_list); i++)
                {
                    if(get_value_list[i] == true)
                    {
                        writeLog(g_script_name,"init_mapping() - Momentary Type And Output True -> Output False Set. dpe_name = " +  get_dp_list[i], LV_INFO);
                        dynAppend(set_dp_list, get_dp_list[i]);
                        dynAppend(set_value_list, false);
                    }
                }
            }
        }


        if(dynlen(get_dp_list) > 0)
        {
            dynClear(get_dp_list);
            dynClear(get_value_list);
        }

        // �ʼ� �Ķ���� Check
        for (int i = 2 ; i <= dynlen(tbval); i++)
        {
            string dp_name = dpSubStr(tbval[i][1], DPSUB_DP);

            if(i == 2)
            {
                //�ʼ� �Ķ���Ͱ� callback ���Դ��� Ȯ��
                if(strlen(cfg_oplast_para) >= 0 && mappingHasKey(g_map_value, dp_name + cfg_oplast_para) == false)
                {
                    writeLog(g_script_name,"init_mapping() - essential parameter not exist. dpe_name = " +  dp_name + cfg_oplast_para, LV_WARN);
                    result = false;
                }
                else if(strlen(cfg_opman_para) >= 0 && mappingHasKey(g_map_value, dp_name + cfg_opman_para) == false)
                {
                    writeLog(g_script_name,"init_mapping() - essential parameter not exist. dpe_name = " +  dp_name + cfg_opman_para, LV_WARN);
                    result = false;
                }
            }
            //cmd mapping ���� ��� Default ó��
            if(mappingHasKey(g_map_cmd, dp_name + cfg_opsource_para) == false)
            {
                g_map_cmd[dp_name + cfg_opsource_para] = SOURCE_AUTO;

                if(i == 2)
                {
                    writeLog(g_script_name,"init_mapping() - parameter not exist -> default value set. dpe_name = " +  dp_name + cfg_opsource_para, LV_INFO);
                }
            }

            if(mappingHasKey(g_map_cmd, dp_name + cfg_opmomdlytm_para) == false)
            {
                g_map_cmd[dp_name + cfg_opmomdlytm_para] = OPMOMDLYTM_DEFAULT;

                if(i == 2)
                {
                    writeLog(g_script_name,"init_mapping() - parameter not exist -> default value set. dpe_name = " +  dp_name + cfg_opmomdlytm_para, LV_INFO);
                }
            }
            if(mappingHasKey(g_map_alarm, dp_name + cfg_on_command_alm_para) == false)
            {
                g_map_alarm[dp_name + cfg_on_command_alm_para] = false;
            }
        }

        // ��� ���� ���� ������Ʈ
        if(isScriptActive == true && dynlen(set_dp_list) > 0)
        {
            writeLog(g_script_name,"init_mapping() - Update Request : " + dynlen(set_dp_list), LV_DBG1);

            if(setDpValue_block(set_dp_list, set_value_list) == false)
            {
                writeLog(g_script_name,"init_mapping() - dpSet - NG. set_points = "
                         + dynlen(set_dp_list) + ", set_values = " + dynlen(set_value_list), LV_ERR);
            }
        }
        if(dynlen(set_dp_list) > 0)
        {
            dynClear(set_dp_list);
            dynClear(set_value_list);
        }
    }
    catch
    {
        result = false;
        update_user_alarm(manager_dpname, "Exception of init_mapping(). Error = " + getLastException());
    }
    finally
    {
        delay(1);
        return result;
    }
}

//*******************************************************************************
// name         : CB_value
// argument     : OPMAN, OPAUTO ���� ��
// return value : void
// date         : 2024-10-07
// developed by : JSH
// brief        : OPMAN, OPAUTO ���� �����Ͽ� OPLAST ���
//*******************************************************************************
void CB_value(anytype user, dyn_dyn_anytype tbval)
{
    if(isScriptActive == true)
        update_heartbeat(manager_dpname);

    for (int i = 2 ; i <= dynlen(tbval); i++)
    {
        try
        {
            string dp_name = dpSubStr(tbval[i][1], DPSUB_DP);
            string dpe_name = dpSubStr(tbval[i][1], DPSUB_DP_EL);

            synchronized(g_map_cmd)
            {
                //�ű� Tag �߰� ��Ȳ�� ��� Skip Logic
                if(mappingHasKey(g_map_value, dp_name + cfg_oplast_para) == false)
                {
                    writeLog(g_script_name, "CB_value() - New Tag Skip Logic", LV_DBG1);
                    continue;
                }

                anytype opsource_value = g_map_cmd[dp_name + cfg_opsource_para];
                bool opman_value;

                if(dpGet(dp_name + cfg_opman_para, opman_value) == 0)
                {
                    writeLog(g_script_name,"CB_value() - dpGet OK" + " tag: " + dp_name, LV_INFO);
                }
                else
                {
                    writeLog(g_script_name,"CB_value() - dpGet NG" + " tag: " + dp_name, LV_ERR);
                }

                anytype old_value = g_map_value[dpe_name];
                anytype new_value = tbval[i][2];

                g_map_value[dpe_name] = new_value;

                // �ڵ�, OPAuto / ����, OPMan
                if((opsource_value == SOURCE_AUTO && strpos(dpe_name, cfg_opauto_para) > 0)
                        || (opsource_value == SOURCE_MANUAL && strpos(dpe_name, cfg_opman_para) > 0 && opman_value == true))
                {
                    if(old_value != new_value)  //OPAUTO(1,0), OPMAN(1) ������ Ȯ��
                    {
                        if(g_map_value[dp_name + cfg_oplast_para] != new_value)
                        {
                            g_map_value[dp_name + cfg_oplast_para] = new_value;
                            dpSetActive(dp_name + cfg_oplast_para, new_value);
                            Oplast_Result(dp_name + cfg_oplast_para);
                        }
                    }
                }
				//TODO : Check_Thread ���� �ʱ�ȭ �����ؼ� �ߺ�??
                else if(opsource_value == SOURCE_MANUAL && strpos(dpe_name, cfg_opman_para) > 0 && opman_value == false)
                {
                    if(old_value != new_value)  //OPMAN(0) ������ Ȯ�� -> oplast �ʱ�ȭ�� ��Ű�� �������� X
                    {
                        if(g_map_value[dp_name + cfg_oplast_para] != new_value)
                        {
                            g_map_value[dp_name + cfg_oplast_para] = new_value;
                            dpSetActive(dp_name + cfg_oplast_para, new_value);
                        }
                    }
                }
            }
        }
        catch
        {
            update_user_alarm(manager_dpname, "Exception of CB_value(). Error = " + getLastException());
        }
    }
}

//*******************************************************************************
// name         : Oplast_Result
// argument     : OPLAST ���� ��
// return value : void
// date         : 2024-10-07
// developed by : JSH
// brief        : OPLAST ���� �����Ͽ� OPRAW ���
//*******************************************************************************
void Oplast_Result(string dpe_name)
{
    dyn_string set_dp_list, set_value_list;
    int logic_type = 0;
    string pvlast_name;

    try
    {
        string dp_name = dpSubStr(dpe_name, DPSUB_DP);
        anytype new_value = g_map_value[dpe_name];

        dynAppend(set_dp_list, dp_name + cfg_cx_para);
        dynAppend(set_value_list, new_value);

        // "AH_3F20201A_CX" -> "AH_3F20201A_ST.value.ST"
        pvlast_name = get_status_name(dp_name);

        // LOGIC TYPE �з� -> ����(ST����O), ����(ST����X), �ڵ�(ST����O), �ڵ�(ST����X)
        if(g_map_cmd[dp_name + cfg_opsource_para])
        {
            if(dpExists(pvlast_name))
            {
                if(g_map_value[dp_name + cfg_opman_para])
                {
                    logic_type = TYPE_MANUAL_CXST_ON;
                }
                else
                {
                    logic_type = TYPE_MANUAL_CXST_OFF;
                }
            }
            else
            {
                logic_type = TYPE_MANUAL_CXONLY;
            }
        }
		//TODO : else �� ����
        else if(!(g_map_cmd[dp_name + cfg_opsource_para]))
        {
            if(dpExists(pvlast_name))
            {
                if(g_map_value[dp_name + cfg_opauto_para])
                {
                    logic_type = TYPE_AUTO_CXST_ON;
                }
                else
                {
                    logic_type = TYPE_AUTO_CXST_OFF;
                }
            }
            else
            {
                logic_type = TYPE_AUTO_CXONLY;
            }
        }

        // �˶� �ʱ�ȭ
        if(g_map_alarm[dp_name + cfg_on_command_alm_para] == true)
        {
            g_map_alarm[dp_name + cfg_on_command_alm_para] = false;
            dynAppend(set_dp_list, dp_name + cfg_on_command_alm_para);
            dynAppend(set_value_list, false);
        }

        // ��� ���� ���� ������Ʈ
        if(isScriptActive == true && dynlen(set_dp_list) > 0)
        {
            writeLog(g_script_name,"Oplast_Result() - Update Request : " + dynlen(set_dp_list), LV_DBG1);

            if(setDpValue_block(set_dp_list, set_value_list) == false)
            {
                writeLog(g_script_name,"Oplast_Result() - dpSet - NG. set_points = "
                         + dynlen(set_dp_list) + ", set_values = " + dynlen(set_value_list), LV_ERR);
            }
        }

        if(dynlen(set_dp_list) > 0)
        {
            dynClear(set_dp_list);
            dynClear(set_value_list);
        }
        //3. ���� ���� ����
        if(mappingHasKey(g_map_thread_key, dp_name) == true)
        {
            //3-1. ���� �������� Thread ID ��ȸ
            int working_thread_id = g_map_thread_key[dp_name];

            //3-2. ���� ���� Thread ID �ߴ�
            if(stopThread(working_thread_id) == 0)
            {
                writeLog(g_script_name, "Oplast_Result() - The running thread was normally stopped. Thread ID = " + working_thread_id, LV_INFO);
            }
            else
            {
                writeLog(g_script_name, "Oplast_Result() - Failed to stop running thread. Thread ID = " + working_thread_id, LV_ERR);
            }
        }
        //4. PVLAST ��� �� Ȯ�� Thread ȣ��
        int thread_id = startThread("Check_Thread", dp_name, logic_type);

        if(thread_id > 0)
        {
            g_map_thread_key[dp_name] = thread_id ;

            string msg ;
            sprintf(msg, "Oplast_Result() : dp_name = %s, logic_type = %d. Check Thread ID = %d",  dp_name, logic_type, thread_id);
            writeLog(g_script_name, msg, LV_INFO);
        }
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of Oplast_Result(). Error = " + getLastException());
    }
}

//*******************************************************************************
// name         : CB_cmd
// argument     : OPSource, OPMomdlytm, Cmdchktm
// date         : 2024-10-07
// developed by : KWH
// brief        : cmd value �޸� ����(���氪) -> g_map_cmd
//*******************************************************************************
void CB_cmd(anytype usrdt, dyn_dyn_anytype tbval)
{
    dyn_string set_dp_list, set_value_list;
    dyn_string get_dp_list, get_value_list;
    mapping map_new_tag;

    try
    {
        if(isScriptActive == true)
            update_heartbeat(manager_dpname);

        for (int i = 2; i <= dynlen(tbval); i++)
        {
            string dp_name = dpSubStr(tbval[i][1], DPSUB_DP);
            string dpe_name = dpSubStr(tbval[i][1], DPSUB_DP_EL);
            anytype cmd_value = tbval[i][2];

            writeLog(g_script_name, "CB_cmd() - Changed. dpe_name = " + dpe_name +", value = " + cmd_value, LV_INFO);

            synchronized(g_map_cmd)
            {
                // ���� Tag ���� ���
				// TODO :  mappingHasKey ��� ���� �³���? g_map_value, g_map_cmd
				// TODO :  �� �ּ� �߰�
                if(mappingHasKey(g_map_value, dp_name + cfg_oplast_para) == true)
                {
                    // �������� ���̰� �ִ� ��츸 Update
                    if(g_map_cmd[dpe_name] != cmd_value)
                    {
                        g_map_cmd[dpe_name] = cmd_value;

                        // OPSOURCE ���� �� ����� ���� ������ �ϴ� Logic (��� ����)
                        if(strpos(dpe_name, cfg_opsource_para) > 0)
                        {
                            //�ڵ� -> ���� :  OPMAN = OPLAST ���� ����
                            if(g_map_cmd[dpe_name] == SOURCE_MANUAL)
                            {
                                dynAppend(set_dp_list, dp_name + cfg_oplast_para);
                                dynAppend(set_value_list, g_map_value[dp_name + cfg_opman_para]);
                                g_map_value[dp_name + cfg_oplast_para] = g_map_value[dp_name + cfg_opman_para];
                                Oplast_Result(dp_name + cfg_oplast_para);

                                writeLog(g_script_name, "CB_cmd() - opsource auto -> manual changed", LV_INFO);
                            }
                            //���� -> �ڵ� : OPAUTO = OPLAST�� ����� ����
                            else
                            {
                                dynAppend(set_dp_list, makeDynString(dp_name + cfg_opman_para, dp_name + cfg_oplast_para));
                                dynAppend(set_value_list, makeDynString(false, g_map_value[dp_name + cfg_opauto_para]));
                                g_map_value[dp_name + cfg_opman_para] = g_map_value[dp_name + cfg_oplast_para];
                                g_map_value[dp_name + cfg_oplast_para] = g_map_value[dp_name + cfg_opauto_para];
                                Oplast_Result(dp_name + cfg_oplast_para);
                                writeLog(g_script_name, "CB_cmd() - opsource manual -> auto changed", LV_INFO);
                            }
                        }
                        else
                        {
                            writeLog(g_script_name, "CB_cmd() - Oplast_Result Logic Pass", LV_INFO);
                        }
                    }
                }
                else
                {
                    // �ű� �߰� Logic
                    //A.OPSource, A.OPType, A.OPDir, ...
                    g_map_cmd[dpe_name] = cmd_value;
                    map_new_tag[dp_name] = true;
                }
            }
        }//for

        //�ű� Tag Logic ����
        for(int i = 1 ; i <= mappinglen(map_new_tag); i++)
        {
            // CMD Parameter ���� ��� Default �� �Է�
            string dp_name = mappingGetKey(map_new_tag, i);
            if(mappingHasKey(g_map_cmd, dp_name + cfg_opsource_para) == false)
            {
                g_map_cmd[dp_name + cfg_opsource_para] = SOURCE_AUTO;
            }
            if(mappingHasKey(g_map_cmd, dp_name + cfg_opmomdlytm_para) == false)
            {
                g_map_cmd[dp_name + cfg_opmomdlytm_para] = OPMOMDLYTM_DEFAULT;
            }

            // alarm�� Default
            if(mappingHasKey(g_map_alarm, dp_name + cfg_on_command_alm_para) == false)
            {
                g_map_alarm[dp_name + cfg_on_command_alm_para] = false;
            }

            // OPMAN �ʱⰪ �Է�
            if(mappingHasKey(g_map_value, dp_name + cfg_opman_para) == false && cfg_opman_para != "")
            {
                if(dpGet(dp_name + cfg_opman_para, g_map_value[dp_name + cfg_opman_para]) == 0)
                {
                    writeLog(g_script_name,"CB_cmd() - dpGet OK" + " tag: " + dp_name, LV_INFO);
                }
                else
                {
                    writeLog(g_script_name,"CB_cmd() - dpGet NG" + " tag: " + dp_name, LV_ERR);
                }
            }
            // OPAUTO �ʱⰪ �Է�
            if(mappingHasKey(g_map_value, dp_name + cfg_opauto_para) == false && cfg_opauto_para != "")
            {
                if(dpGet(dp_name + cfg_opauto_para, g_map_value[dp_name + cfg_opauto_para]) == 0)
                {
                    writeLog(g_script_name,"CB_cmd() - dpGet OK" + " tag: " + dp_name, LV_INFO);
                }
                else
                {
                    writeLog(g_script_name,"CB_cmd() - dpGet NG" + " tag: " + dp_name, LV_ERR);
                }
            }

            // �ű� �߰��� Tag�� Logic ����
            // �ڵ�, OPAuto
            if(g_map_cmd[dp_name + cfg_opsource_para] == SOURCE_AUTO)
            {
                g_map_value[dp_name + cfg_oplast_para] = g_map_value[dp_name + cfg_opauto_para];
                dpSetActive(makeDynString(dp_name + cfg_oplast_para, dp_name + cfg_opauto_para),
                            makeDynAnytype(g_map_value[dp_name + cfg_oplast_para], g_map_value[dp_name + cfg_opauto_para]));
                Oplast_Result(dp_name + cfg_oplast_para);
            }

            // ����, OPMan
            else if(g_map_cmd[dp_name + cfg_opsource_para] == SOURCE_MANUAL)
            {
                g_map_value[dp_name + cfg_oplast_para] = g_map_value[dp_name + cfg_opman_para];
                dpSetActive(makeDynString(dp_name + cfg_oplast_para, dp_name + cfg_opman_para),
                            makeDynAnytype(g_map_value[dp_name + cfg_oplast_para], g_map_value[dp_name + cfg_opman_para]));
                Oplast_Result(dp_name + cfg_oplast_para);
            }
        }
    }

    catch
    {
        update_user_alarm(manager_dpname, "Exception of CB_cmd() - for. Error = " + getLastException());
    }

    finally
    {
        if(isScriptActive == true && dynlen(set_dp_list) > 0)
        {
            writeLog(g_script_name,"Oplast_Result() - Update Request : " + dynlen(set_dp_list), LV_DBG1);

            if(setDpValue_block(set_dp_list, set_value_list) == false)
            {
                writeLog(g_script_name,"Oplast_Result() - dpSet - NG. set_points = "
                + dynlen(set_dp_list) + ", set_values = " + dynlen(set_value_list), LV_ERR);
            }
        }

        if(dynlen(set_dp_list) > 0)
        {
            dynClear(set_dp_list);
            dynClear(set_value_list);
        }
    }
}


//*******************************************************************************
// name         : Check_Thread
// argument     : dp �̸�, opman ��
// return value : void
// date         : 2024-10-07
// developed by : JSH
// brief        : opman ���� ���� ���� PVLAST Ȯ���Ͽ� �˶� ó�� Thread
//*******************************************************************************
void Check_Thread(string dp_name, anytype logic_type)
{
    string pvlast_name;
    anytype pvlast_value, opsource_value;
    string cx_dpe_name = dp_name + cfg_cx_para;
    dyn_string off_dp_list, off_dp_value;
    time current_time;

    current_time = getCurrentTime();

    try
    {
        writeLog(g_script_name, "Check_Thread() - Thread Start. dp_name = " + dp_name + ", new_value = " + logic_type, LV_DBG1);

        //"AH_3F20101A_CX" -> "AH_3F20101A_STATUS.PVLAST" �� ��ȸ
        pvlast_name = get_status_name(dp_name);

        // ���� ������ ���, �ڵ� CX-ON ���� ���� + ���� ���� ����
        if(logic_type == TYPE_MANUAL_CXST_ON || logic_type == TYPE_AUTO_CXST_ON)
        {

            // ��������ð� �� ��� �� �Ķ���� �ʱ�ȭ
            if(Check_Dlytm_Status(dp_name, pvlast_name, true, g_map_cmd[dp_name + cfg_opmomdlytm_para], current_time) == true)
            {
                writeLog(g_script_name,"Check_Dlytm() - Dlytm Check OK. TAG = " + dp_name, LV_INFO);
                dpSetActive(dp_name + cfg_cx_para, false);
                g_map_value[dp_name + cfg_cx_para] = false;
                // ���������� ���, ��������ð� �� ������� �ʱ�ȭ
                if(logic_type == TYPE_MANUAL_CXST_ON)
                {
					off_dp_list = makeDynString(dp_name + cfg_opman_para, dp_name + cfg_oplast_para);
					off_dp_value = makeDynString(false, false);
                    dpSetActive(off_dp_list, off_dp_value);
                    g_map_value[dp_name + cfg_opman_para] = false;
                    g_map_value[dp_name + cfg_oplast_para] = false;
                }
            }
            else
            {
                writeLog(g_script_name,"Check_Dlytm() - Dlytm Check NG. TAG = " + dp_name, LV_ERR);
            }
			
            // Ȯ�νð� �� on_command �˶� �߻�
            if(Check_Status(dp_name, pvlast_name, true, g_map_cmd[dp_name + cfg_cmdchktm_para], g_map_cmd[dp_name + cfg_opmomdlytm_para], current_time) == true)
            {
                writeLog(g_script_name,"Control_Thread() - Status Check OK. TAG = " + pvlast_name, LV_INFO);
            }
            else
            {
                dpSetActive(dp_name + cfg_on_command_alm_para, true);
                g_map_alarm[dp_name + cfg_on_command_alm_para] = true;
                // ���� ������, ���¹ٲ�� �˶� �ʱ�ȭ
				// TODO : ȣ�� ���� ó�� �α� �߰�
                dpConnectUserData("CB_alarm", true, pvlast_name);
                writeLog(g_script_name,"Control_Thread() - Status Check NG. TAG = " + pvlast_name, LV_ERR);
            }
        }
        // ���� ���� ���ϴ� ���, ��/���� ���� + ���� ������ ���, �ڵ� CX-OFF ����
        else if(logic_type == TYPE_MANUAL_CXONLY || logic_type == TYPE_AUTO_CXONLY || 
		logic_type == TYPE_AUTO_CXST_OFF || logic_type == TYPE_MANUAL_CXST_OFF)
		//TODO : logic_type == TYPE_AUTO_CXST_OFF || logic_type == TYPE_MANUAL_CXST_OFF  ���ִ°� ���� �ʳ�??
        {

            // ��������ð� �� ��� �� �Ķ���� �ʱ�ȭ
            if(Check_Dlytm(dp_name, g_map_cmd[dp_name + cfg_opmomdlytm_para], current_time) == true)
            {
                writeLog(g_script_name,"Check_Dlytm() - Dlytm Check OK. TAG = " + dp_name, LV_INFO);
                dpSetActive(dp_name + cfg_cx_para, false);
                g_map_value[dp_name + cfg_cx_para] = false;
				
                // ���������� ���, ��������ð� �� ������� �ʱ�ȭ
                if(logic_type == TYPE_MANUAL_CXONLY)
                {
					off_dp_list = makeDynString(dp_name + cfg_opman_para, dp_name + cfg_oplast_para);
					off_dp_value = makeDynString(false, false);
			
                    dpSetActive(off_dp_list, off_dp_value);
                    g_map_value[dp_name + cfg_opman_para] = false;
                    g_map_value[dp_name + cfg_oplast_para] = false;
                }
            }
            else
            {
                writeLog(g_script_name,"Check_Dlytm() - Dlytm Check NG. TAG = " + dp_name, LV_ERR);
            }
        }
        else
        {
            writeLog(g_script_name, "Check_Thread() - This target is not DOCX Type, dp_name = " + dp_name, LV_WARN);
        }
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of Check_Thread(). Error = " + getLastException());
    }

    finally
    {
        // Thread �Լ��� �Ϸ�� ��� Thread key map ���� ����(���� ���� ���� Thread�� map���� ������ ����)
        // �ߺ� ������ �ȵǵ��� map���� ����
        mappingRemove(g_map_thread_key, dp_name);
        writeLog(g_script_name, "Check_Thread() - Thread exit. dp_name = " + dp_name + ", logic_type = " + logic_type, LV_DBG1);
    }
}

//*******************************************************************************
// name         : get_status_name
// argument     : dp �̸�, opman ��
// return value : void
// date         : 2024-10-07
// developed by : JSH
// brief        : ���� DP �̸����� ���� �̸� ��ȯ �Լ�
//*******************************************************************************
string get_status_name(string dp_name)
{
    string source_dpe_name, result_dpe_name;
    dyn_string split_dp;

    try
    {
        source_dpe_name = dp_name;				//"AH_3F20101A_CX"
        split_dp = strsplit(source_dpe_name, "_");
        if(split_dp[dynlen(split_dp)] == cfg_source_filter)
        {
            split_dp[dynlen(split_dp)] = cfg_target_filter;
        }
        result_dpe_name = split_dp[1];
        for(int i=2; i<=dynlen(split_dp); i++)
        {
            if(split_dp[i] == "")
            {
                break;
            }
            result_dpe_name += "_" + split_dp[i];
        }
        result_dpe_name = result_dpe_name + cfg_pvlast_para;				//"AH_3F20101A_STATUS.PVLAST"

        //TODO : ���� DebugTN
        DebugTN(result_dpe_name);
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of get_status_name(). Error = " + getLastException());
    }

    return result_dpe_name;
}

//*******************************************************************************
// name         : get_alarm_name
// argument     : dp �̸�, opman ��
// return value : void
// date         : 2024-10-07
// developed by : JSH
// brief        : ���� DP �̸����� �߻��ϴ� �˶� �̸� ��ȯ �Լ� cfg_source_filter / cfg_target_filter
//********************************************************************************
string get_alarm_name(string dp_name, string alarm_type)
{
    string source_dpe_name, result_dpe_name;
    dyn_string split_dp;

    try
    {
		//TODO : ���� �� �α� �߰�
        source_dpe_name = dp_name;				//"AH_3F20101A_STATUS.PVLAST" -> ""

        strreplace(source_dpe_name, cfg_pvlast_para, ""); //"AH_3F20101A_STATUS

        split_dp = strsplit(source_dpe_name, "_");
        if(split_dp[dynlen(split_dp)] == cfg_target_filter)
        {
            split_dp[dynlen(split_dp)] = cfg_source_filter;
        }
        if(cfg_target_filter == "")
        {
            split_dp[dynlen(split_dp)+1] = cfg_source_filter;
        }
        result_dpe_name = split_dp[1];
        for(int i=2; i<=dynlen(split_dp); i++)
        {
            if(split_dp[i] == "")
            {
                break;
            }
            result_dpe_name += "_" + split_dp[i];
        }

        if(alarm_type == "ON")
        {
            result_dpe_name += cfg_on_command_alm_para;  //"AH_3F20101A_CX.alert.ONCOMERR"
        }
    }
    catch
    {
        //TODO : ���� update_user_alarm �α� ���� ����
        update_user_alarm(manager_dpname, "Exception of get_status_name(). Error = " + getLastException());
    }

    return result_dpe_name;
}

//*******************************************************************************
// name         : str_from
// argument     : �Ķ���� ����Ʈ
// return value : string
// date         : 2022.12.20
// developed by : Inno-Team
// brief        : Callback From�� ������ ����
//*******************************************************************************
string str_from(dyn_string parameters)
{
    string from ;

    try
    {
        from = "'{";

        for (int i = 1 ; i <= dynlen(parameters); i++)
        {
            if(parameters[i] != "")
            {
                from += "*" + parameters[i];

                if (i != dynlen(parameters))
                    from += ", ";
            }
        }
        from += " }'";
        // ������ , } ������ �κ� ó��
        strreplace(from, ",  }", " }");
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of str_from(). Error = " + getLastException());
    }

    return from;
}
//*******************************************************************************
// name         : str_where
// argument     : DP Type ����Ʈ
// return value : string
// date         : 2022.12.20
// developed by : Inno-Team
// brief        : Callback Where�� ������ ����
//*******************************************************************************
string str_where(dyn_string dp_type_list)
{
    string where;

    try
    {
        where = " _DPT IN (";

        for (int i = 1; i <= dynlen(dp_type_list); i++)
        {
            if (i < dynlen(dp_type_list))
            {
                where += "\"" + dp_type_list[i] + "\", ";
            }
            else
            {
                where += "\"" + dp_type_list[i] + "\")";
            }
        }
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of str_where(). Error = " + getLastException());
    }

    finally
    {
        return where;
    }
}
//*******************************************************************************
// name         : CB_alarm
// argument     : di pvlast
// return value : void
// date         : 2024.10.07
// developed by : JSH
// brief        : on command error alarm �߻� ����, di ���¸� ������ alarm reset
//*******************************************************************************
void CB_alarm(bool userdt, string di_dpname, bool state)
{
    try
    {
        string alarm_tag;
        strreplace(di_dpname,":_online.._value","");
        if((userdt == true && state == true) || userdt == false && state == false)
        {
            // ON ����
            if(userdt == true)
            {
                alarm_tag = get_alarm_name(di_dpname, "ON");
            }
			
			//TODO : OFF �˶� �ڵ� ����
            // OFF ����
            // else
            // {
                // alarm_tag = get_alarm_name(di_dpname, "OFF");
            // }
            dpSetActive(alarm_tag, false);
			
            if(dpDisconnectUserData("CB_alarm", userdt, di_dpname) == 0)
            {
                writeLog(g_script_name, "===== dpDisconnect Sucess ===== dp name : " + di_dpname, LV_INFO);
            }
            else
            {
                writeLog(g_script_name, "===== dpDisconnect NG ===== dp name : " + di_dpname, LV_ERR);
            }
        }
    }
    catch
    {
        update_user_alarm(manager_dpname, "Exception of str_where(). Error = " + getLastException());
    }
}

//*******************************************************************************
// name         : dpSetActive
// argument     : dpSet
// return value : void
// date         : 2024.10.07
// developed by : JSH
// brief        : dpSet���� ��, isScriptActive Check
//*******************************************************************************
void dpSetActive(dyn_string dpe_names, dyn_anytype values)
{
    //TODO : try,catch ����
    if(isScriptActive == true)
    {
        if(dpSetWait(dpe_names, values) == 0)
        {
            writeLog(g_script_name,"dpSetActive() OK. - Update Request : " + dpe_names, LV_INFO);
        }
        else
        {
            writeLog(g_script_name,"dpSetActive() NG. - Update Request : " + dpe_names, LV_ERR);
        }
    }
}

//*******************************************************************************
// name         : Check_Status()
// argument     :
// return value : 1 / 0
// date         : 2024.10.07
// developed by : JSH
// brief        : Ȯ�νð� ���� �����±� �ٲ���� üũ + ���� �ٲ�� �Լ� ����
//*******************************************************************************
bool Check_Status(string control_dp, string check_dp, anytype check_val, int cmdchktm_sec, int opmomdlytm_sec, time control_time)
{
    bool result = false;
    int diff_sec;
    diff_sec = cmdchktm_sec - opmomdlytm_sec;
    try
    {
        anytype dp_val;

        if(!(diff_sec == 0))
        {
            for(int i = 1; i <= diff_sec; i++)
            {
                writeLog(g_script_name,"Check_Status() " + check_dp + "-" + i, LV_INFO, LV_INFO);

                if(period(getCurrentTime() - control_time) > cmdchktm_sec)
                {
                    break;
                }

                if(dpGet(check_dp, dp_val) == 0)
                {
                    writeLog(g_script_name,"Check_Status() - dpGet OK" + " tag: " + check_dp, LV_INFO);
                }
                else
                {
                    writeLog(g_script_name,"Check_Status() - dpGet NG" + " tag: " + check_dp, LV_ERR);
                }
                if(dp_val == check_val)
                {
                    result = true;
                    return result;
                }
                delay(1);
            }
        }
        return result;
    }
    catch
    {
        result = false;
        update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
    }
}

//*******************************************************************************
// name         : Check_Dlytm()
// argument     :
// return value : 1 / 0
// date         : 2024.10.07
// developed by : JSH
// brief        : ��������ð����� ��� ����
//*******************************************************************************
bool Check_Dlytm(string control_dp, int opmomdlytm_sec, time control_time)
{
    bool result = true;
    try
    {
        for(int i = 1; i <= opmomdlytm_sec; i++)
        {
            writeLog(g_script_name,"Check_Dlytm() " + control_dp + "-" + i, LV_INFO);

            if(period(getCurrentTime() - control_time) > opmomdlytm_sec)
            {
                result = true;
                break;
            }
            delay(1);
        }
        return result;
    }
    catch
    {
        result = false;
        update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
    }
}

//*******************************************************************************
// name         : Check_Dlytm_Status()
// argument     :
// return value : 1 / 0
// date         : 2024.10.07
// developed by : JSH
// brief        : ��������ð����� ��� ���� + ���¹ٲ�� ��� OFF
//*******************************************************************************
bool Check_Dlytm_Status(string control_dp, string check_dp, anytype check_val, int opmomdlytm_sec, time control_time)
{
    bool result = true;
    try
    {
        anytype dp_val;
        for(int i = 1; i <= opmomdlytm_sec; i++)
        {
            writeLog(g_script_name,"Check_Dlytm() " + control_dp + "-" + i, LV_INFO);

            if(dpGet(check_dp, dp_val) == 0)
            {
                writeLog(g_script_name,"Check_Status() - dpGet OK" + " tag: " + check_dp, LV_INFO);
            }
            else
            {
                writeLog(g_script_name,"Check_Status() - dpGet NG" + " tag: " + check_dp, LV_ERR);
            }

            if(dp_val == check_val)
            {
                result = true;
                return result;
            }
            if(period(getCurrentTime() - control_time) > opmomdlytm_sec)
            {
                result = true;
                break;
            }
            delay(1);
        }
        return result;
    }
    catch
    {
        result = false;
        update_user_alarm(manager_dpname, "Exception of load_config(). Error = " + getLastException());
    }
}
