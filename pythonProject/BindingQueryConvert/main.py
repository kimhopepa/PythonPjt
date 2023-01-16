#1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

#2) 참조할 lib 파일 추가
from libConvert import *
from libConfig import *

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# #2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("BindingQueryConvert.ui")
form_class = uic.loadUiType(form)[0]

# #3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()

        #1. UI 이벤트 초기화
        self.setupUi(self)

        self._converter = ConvertManager()
        self._configer = ConfigManager()

        self.pushButton_Convert.clicked.connect(self.literalConvert)

        self.loadConfig()

    def loadConfig(self):
        try :
            binding_query = self._configer.GetConfigData(self._configer.section_main, self._configer.key_binding_query)
            binding_parameter = self._configer.GetConfigData(self._configer.section_main, self._configer.key_binding_parameter)

            self.plainTextEdit_BindingQuery.setPlainText(binding_query)
            self.plainTextEdit_BindingParameter.setPlainText(binding_parameter)

        except Exception as e:
            print("loadConfig()", e)

    def literalConvert(self):
        try :
            print("literalConvert")

            text_bindingQuery = self.plainTextEdit_BindingQuery.toPlainText()
            text_bindingParameter = self.plainTextEdit_BindingParameter.toPlainText()

            # text_bindingQuery =  r"INSERT /*hanwha.convergence-PMModeLogic(IDX_PM_INSERT) 2022.12.21*/ INTO TN_CM_PM_APPR  (EQP_NO, START_DATE, END_DATE, ACTN_REASON_CONT, APPR_STATUS_CODE, REQ_DATE, REQ_USER_ID, APPR_DATE, APPR_USER_ID  , PM_START_YN, PM_END_YN, PM_EXT_NOTIFY_YN, EXT_DATE, PM_EXT_YN, MOD_DATE, MOD_USER_ID, REG_DATE, REG_USER_ID)  VALUES(:eqp_no, TO_TIMESTAMP(:start_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), TO_TIMESTAMP(:end_date, 'YYYY.MM.DD HH24:MI:SS.FF3') + 8 /24, :actn_reason_cont, :appr_status_code, TO_TIMESTAMP(:req_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :req_user_id, TO_TIMESTAMP(:appr_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :appr_user_id  , :pm_start_yn, :pm_end_yn, :pm_ext_notify_yn, NULL, :pm_ext_yn, TO_TIMESTAMP(:mod_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :mod_user_id, TO_TIMESTAMP(:reg_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :reg_user_id )"
            # text_bindingParameter = r"3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 | SS_LOGIC | APPR_A | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | INNO_TEAM | N | N | Y | N | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | PM_LOGIC"

            #1. Literal Query 생성
            text_literal_query = self._converter.makeLiteralQuery(text_bindingQuery, text_bindingParameter)
            
            #2. UI의 lineEdit에 저장
            self.plainTextEdit_literalQuery.setPlainText(text_literal_query)
            print(text_bindingQuery, text_bindingParameter)

            self._configer.SaveConfig(self._configer.section_main, self._configer.key_binding_query, text_bindingQuery)
            self._configer.SaveConfig(self._configer.section_main, self._configer.key_binding_parameter, text_bindingParameter)

            #
            # QMessageBox.about(self, "message", text_bindingQuery + ", " + text_bindingParameter)
            # reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
            #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # self._converter.
            # self.lineEdit_bindingQuery.
            # 1. csv 파일 Read

        except Exception as e:
            print("literalConvert()", e)


#4) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

# bind_query = r"INSERT /*hanwha.convergence-PMModeLogic(IDX_PM_INSERT) 2022.12.21*/ INTO TN_CM_PM_APPR  (EQP_NO, START_DATE, END_DATE, ACTN_REASON_CONT, APPR_STATUS_CODE, REQ_DATE, REQ_USER_ID, APPR_DATE, APPR_USER_ID  , PM_START_YN, PM_END_YN, PM_EXT_NOTIFY_YN, EXT_DATE, PM_EXT_YN, MOD_DATE, MOD_USER_ID, REG_DATE, REG_USER_ID)  VALUES(:eqp_no, TO_TIMESTAMP(:start_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), TO_TIMESTAMP(:end_date, 'YYYY.MM.DD HH24:MI:SS.FF3') + 8 /24, :actn_reason_cont, :appr_status_code, TO_TIMESTAMP(:req_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :req_user_id, TO_TIMESTAMP(:appr_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :appr_user_id  , :pm_start_yn, :pm_end_yn, :pm_ext_notify_yn, NULL, :pm_ext_yn, TO_TIMESTAMP(:mod_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :mod_user_id, TO_TIMESTAMP(:reg_date, 'YYYY.MM.DD HH24:MI:SS.FF3'), :reg_user_id )"
# bind_var = r"3651139 | 2023.01.12 14:50:56.032 | 2023.01.12 14:50:56.032 | SS_LOGIC | APPR_A | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | INNO_TEAM | N | N | Y | N | 2023.01.12 14:50:56.032 | PM_LOGIC | 2023.01.12 14:50:56.032 | PM_LOGIC"
#
# _convert_manager = ConvertManager()
#
# _convert_manager.makeLiteralQuery(bind_query, bind_var)
