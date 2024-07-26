const define_dp_name = "master_dp";
void _Func1()
{
	DebugTN("test func1()");			
	int dp_name ="test2.value.PVLAST";	//NG
	dpSet(dp_name, false);		
	dpSet(dp_name, 50);				//NG
}

void func2(int value)
{
	if(value > 50)					//NG
	{	
		DebugTN("test func2()");
		WriteLog("test");
	}
		
	value += 50;					//NG
	string dp_name = dp_name + ".value.PVLAST";	// 대입 연산자 하드코딩 사용 - 문자열 상수 사용
	int min_prio = min_prio + 50;				// 대입 연산자 하드코딩 사용 - 상수 사용
	dpSet(dp_name , 0);							// 함수 호출 or 괄호 안에 하드코딩 사용 - 문자열 or 상사 사용
	
}

void func_3(int a, int b)
{
	dpQueryConnectSingle("cmd_update_AI", false, cfg_use_multi_instance, query, cfg_query_blocking_time);
	DebugTN("test func3()");
	Debug(123);
    writeLog("test");
    Thread(456);
    dpQueryConnectSingle("example");
    func(789);
    call(tag_name);
    dpConnect("CB_Value");
    processConnection(tag_list);
    if(value > 50)
	{
		DebugTN("test1");
	}
    if(value < 50) || if(value ==100)
		dpSet("tag", 50);
	
    dpGet(dp_name + CHECK,CHECK_TAG,
    dp_name + TIME,VOLT_TIME,
    dp_name + MIN,TMP_MIN_VALUE,
    dp_name + MAX,TMP_MAX_VALUE,
    dp_name + HOLDTIME,Delay_time,
    dp_name + ".OFFSET",OFFSET_VALUE);
	
}

void func_44()
{
	string min_para = ":_alert_hdl.._min_prio";
	string tag_name = "AA.alert.HHALM";
	bool result = true;
	int eqp_no_count, db_result;
	string update_query, eqp_no_bind;
	dyn_string dsParams, update_eqp_no_list;
	int conn_idx;
	const int MAX_EQP_NO_COUNT = 1000;
	
	try
	{
		dsParams = in_params;
		string test_dpe_name = tag_name + min_para;
		for(int i = 1; i <= dynlen(eqp_no_list); i++)
		{
			dynAppend(dsParams, eqp_no_list[i]);
			eqp_no_count = i % MAX_EQP_NO_COUNT;
			
			//1) 1,000 인 경우 or 마지막인 경우 수행
			if(i == dynlen(eqp_no_list) || eqp_no_count == 0)
			{
				if(eqp_no_count == 0)
					eqp_no_count = MAX_EQP_NO_COUNT;
				
				dpSet(tag_name + min_para, false);
				//2. Update Query 생성
				//WHERE EQP_NO IN (" + EQP_NO_CONDITION + ")" -> WHERE EQP_NO IN (:eqp_no1, :eqp_no2, ... )
				update_query = orgin_update_query;
				eqp_no_bind = get_eqp_no_condition(eqp_no_count);
				strreplace(update_query, EQP_NO_CONDITION, eqp_no_bind);
				
				//3. Update Query 실행
				conn_idx = get_DBConn();
				db_result = rdbExecuteSingle_Bind(g_dbConn_pool[conn_idx], update_query, dsParams);
				
				// db conncetion 해제
				if (conn_idx > 0)
				{
					if (release_DBConn(conn_idx))
					{
						conn_idx = 0;
					}
					
				}

				// update 성공 시
				if (db_result == DB_ERR_NONE)
				{
					writeLog(g_script_name, "is_updateQuery() - Update query OK.", LV_DBG1);
					writeLog(g_script_name, "is_updateQuery() - Update query OK. Query = " + update_query + ", Params = " + dsParams, LV_DBG2);
				}
				// update 실패 시
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
		// db conncetion 해제
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

void func_5(int a, int b)
{

result = dpConnect("CB_reload",false, reload_dp);
	while(true)
	{
		
		try
		{
			if(test == true)
			{
				dpSet();
			}
		}
		catch
		{
			
		}
		
		delay(1);
	}

}





void func_6(int a, int b)
{
	result = dpConnect("CB_reload",false, reload_dp);
	while(true)
	{
		delay(10);
		try
		{
			delay(1);
			if(test == true)
			{
			}
		}
		catch
		{
			
		}
		finnally
		{
			delay(1);
		}
		
	}

}

void func_7(int a, int b)
{
	string dp_name = "test1.pvlast" ; 
	string dp_name2 = "test2.pvlast" ; 
	float value;
	dyn_string dp_list;
	dyn_anytype list;
	
	for(int i = 1 ; i <= dynlen(dp_list); i++)
	{
		dpGet(dp_list[i], list[i]);
	}
	
	delay(1);
	
	for(int i = 1 ; i <= dynlen(list); i++)
	{
		dpSet(list[i], 0);
	}

}