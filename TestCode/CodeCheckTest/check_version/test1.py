import re


def get_variable_value(c_code, variable_name):

    # Define a regex pattern for variable assignment
    pattern = re.compile(r'\b' + re.escape(variable_name) + r'\b\s*=\s*("[^"]*"|\d+|[^,;]+)')

    # Search for the pattern in the code
    match = re.search(pattern, c_code)

    if match:
        print("test",match)
        return match.group(1).strip()
    return None


# Example usage:
c_code_example = """
const string g_script_release_version = "v1.01";
const string g_script_release_date = "2024.03.07";
const string g_script_name = "Emergency_Blackout";
int a = 10, b = 20;
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
variable_name_3 = "a"
variable_name_4 = "b"

print(f'{variable_name_1}: {get_variable_value(c_code_example, variable_name_1)}')  # Output: "v1.01"
print(f'{variable_name_2}: {get_variable_value(c_code_example, variable_name_2)}')  # Output: "2024.03.07"
print(f'{variable_name_3}: {get_variable_value(c_code_example, variable_name_3)}')  # Output: 10
print(f'{variable_name_4}: {get_variable_value(c_code_example, variable_name_4)}')  # Output: 20
