from libConvert import *

bind_query = r"INSERT /*hanwha.convergence-PMModeLogic(IDX_PM_INSERT) 2022.12.21*/ INTO TN_CM_PM_APPR  (EQP_NO, START_DATE, END_DATE, ACTN_REASON_CONT, APPR_STATUS_CODE, REQ_DATE, REQ_USER_ID, APPR_DATE, APPR_USER_ID  , PM_START_YN, PM_END_YN, PM_EXT_NOTIFY_YN, EXT_DATE, PM_EXT_YN, MOD_DATE, MOD_USER_ID, REG_DATE, REG_USER_ID)  VALUES(:eqp_no, TO_TIMESTAMP(:start_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), TO_TIMESTAMP(:end_date, 'YYYY.MM.DD HH24:MI:SS.FF3') + 8 /24, :actn_reason_cont, :appr_status_code, TO_TIMESTAMP(:req_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :req_user_id, TO_TIMESTAMP(:appr_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :appr_user_id  , :pm_start_yn, :pm_end_yn, :pm_ext_notify_yn, NULL, :pm_ext_yn, TO_TIMESTAMP(:mod_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :mod_user_id, TO_TIMESTAMP(:reg_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :reg_user_id )"
bind_var = r"3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 | SS_LOGIC | APPR_A | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | INNO_TEAM | N | N | Y | N | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | PM_LOGIC"

_convert_manager = ConvertManager()

_convert_manager.makeLiteralQuery(bind_query, bind_var)
