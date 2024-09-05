//v1.0 (2024.02.22)
//첫 배포 버전
//v1.01 (2024.03.07)
//- Secondary 서버에서 Dist 연결 확인 부분 수정
//- Ma, MB 출력 후 Status 확인 Logic 개선 (On 상태시 바로 다음 Step 실행)

#uses "CtrlADO"			
#uses "library_standard.ctl"	//DB Connection이 필요없는 경우

//---------------------------------------------
// configuration path & filename  
//---------------------------------------------
string script_path;      //getPath(SCRIPTS_REL_PATH);
string config_filename = "config/config.Emergency_Blackout";

const string g_script_release_version = "v1.01";
const string g_script_release_date = "2024.03.07";
const string g_script_name = "Emergency_Blackout";

void main()
{
	init_lib_Commmon();	//Debug-Flag Initialize
		
	writeLog(g_script_name, "0. Script Start! Release Version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
	writeLog(g_script_name, "		          lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);
		
}