import re


def is_variable_declared(c_code :str , variable_name:str):
    """
  Checks if a variable is declared in the given C code.

  Parameters:
  c_code (str): The C code to search through.
  variable_name (str): The variable name to check for.

  Returns:
  bool: True if the variable is declared, False otherwise.
  """
    # Remove comments from the code to avoid false positives
    # c_code_no_comments = re.sub(r'//.*|/\*[\s\S]*?\*/', '', c_code)

    # Define a regex pattern for variable declaration, ignoring type and modifiers
    # \b : 단어 경계, escape : 특수문자 이스케이프 처리, \s* : 변수 이름 뒤 공백, (?:=|;|,) : "=",  ";", "," 문자 포함

    pattern = re.compile(r'\b' + re.escape(variable_name) + r'\b\s*(?:=|;|,)')

    # Search for the pattern in the code
    if re.search(pattern, c_code):
        return True
    return False


# Example usage:
c_code_example = """
const string g_script_release_version = "v1.01";
const string g_script_release_date = "2024.03.07";
const string g_script_name = "Emergency_Blackout";
int a, b;
mapping g_script_release_version ;
/*
string sSystem, ctrlName;
*/
void main()
{
    init_lib_Commmon();    //Debug-Flag Initialize

    writeLog(g_script_name, "0. Script Start! Release Version = " + g_script_release_version + ", Date = " + g_script_release_date, LV_INFO);
    writeLog(g_script_name, "                  lib_standard Version = " + g_lib_standard_version + ", Date = " + g_lib_standard_release_date, LV_INFO);

    used_function();
}
"""

variable_name_1 = "g_script_release_version"
variable_name_2 = "g_script_release_date"
variable_name_3 = "g_script_name"
variable_name_4 = "a"
variable_name_5 = "b"

print(is_variable_declared(c_code_example, variable_name_1))  # Output: True
print(is_variable_declared(c_code_example, variable_name_2))  # Output: True
print(is_variable_declared(c_code_example, variable_name_3))  # Output: True
print(is_variable_declared(c_code_example, variable_name_4))  # Output: True
print(is_variable_declared(c_code_example, variable_name_5))  # Output: True
