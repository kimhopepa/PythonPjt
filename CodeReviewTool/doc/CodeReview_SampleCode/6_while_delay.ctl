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

//func_4(){
//	DebugTN("test func4()");
//}

void func_5(int a, int b)
{

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
			delay(1);
		}
		
	}

}

void func_7(int a, int b)
{
	while(true)
	{

	}

}