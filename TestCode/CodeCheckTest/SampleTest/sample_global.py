import re
import lib_function_info as lib

def extract_global_variables(code):
    variables = []
    lines = code.splitlines()
    in_block = False
    block_depth = 0
    temp_line = ""

    for line_num, line in enumerate(lines):
        stripped_line = line.strip()

        # Check for block start or end
        if '{' in stripped_line:
            block_depth += stripped_line.count('{')
        if '}' in stripped_line:
            block_depth -= stripped_line.count('}')

        in_block = block_depth > 0

        # Skip lines inside blocks
        if in_block:
            continue

        # Remove comments from the line
        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line)

        # Concatenate lines that don't end with a semicolon
        temp_line += stripped_line
        if not stripped_line.endswith(';'):
            continue
        else:
            stripped_line = temp_line
            temp_line = ""

        # Extract variable declarations
        if '=' in stripped_line or ';' in stripped_line:
            # Remove the type declarations
            stripped_line = re.sub(r'\b(int|float|double|char|long|short|void)\b', '', stripped_line)
            stripped_line = stripped_line.strip()

            # Split by commas and semicolons
            parts = re.split(r'[;,]', stripped_line)
            for part in parts:
                part = part.strip()
                if part:
                    # Check if it contains an assignment
                    if '=' in part:
                        var_name = part
                    else:
                        tokens = re.split(r'\s+', part)
                        var_name = tokens[0].strip()

                    if re.match(r'^[a-zA-Z_]\w*$', var_name):
                        variables.append((var_name, line_num + 1))

    return variables


# Example usage:
code = """
int globalVar1, globalVar2 = 10;
float globalVar3;
version_name = "test";
globalVar2 = 10;
void function() {
    int localVar1;
    {
        int localVar2;
    }
    globalVar3 = 20.0;
}
"""

def get_global_variables(code : str) -> dict :
    result_dict = {}
    lines = code.splitlines()

    for index, line in enumerate(lines) :
        if(index == 0) :
            break
        print(index, line)

    return result_dict

# variables = extract_global_variables(code)
if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    global_var = get_global_variables(text)
    # fnc_list = lib.get_function_body2(text)
    #
    # total_fnc_list = []
    # check_list = get_dpconnect_function(text)
    # unique_list = list(set(check_list))
    # print(unique_list)
