import re


def find_variables3(code):
    lines = code.splitlines()
    global_vars = []
    brace_depth = 0

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Update brace depth
        brace_depth += stripped_line.count('{')
        brace_depth -= stripped_line.count('}')

        if brace_depth == 0:  # We're not inside any function or block
            # Split by delimiters and ignore '=' assignment parts
            parts = re.split(r'[=,;]', stripped_line)
            for part in parts:
                part = part.strip()
                # Ignore parts containing parentheses
                if '(' in part or ')' in part:
                    continue
                if part:
                    # Handle "문자열 띄어쓰기 문자열"
                    words = part.split()
                    if len(words) > 1:
                        var_name = words[1]
                    else:
                        var_name = words[0]

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars


def find_global_variables4(code):
    lines = code.splitlines()
    global_vars = []
    brace_depth = 0

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Update brace depth
        brace_depth += stripped_line.count('{')
        brace_depth -= stripped_line.count('}')

        if brace_depth == 0:  # We're not inside any function or block
            # Split the line at '=' and consider only the left side
            left_side = re.split(r'=', stripped_line, 1)[0]
            # Further split by delimiters ',', ';' and process each part
            parts = re.split(r'[;,]', left_side)
            for part in parts:
                part = part.strip()
                # Ignore parts containing parentheses
                if '(' in part or ')' in part:
                    continue
                if part:
                    # Handle "문자열 띄어쓰기 문자열"
                    words = part.split()
                    if len(words) > 1:
                        var_name = words[1]
                    else:
                        var_name = words[0]

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars


# Example usage
code_text = """
string version = 10, name = "123";
int g_1, g_2; 
int func(int a, b);
{
    타입 a, b, c;
}
타입 m, n, 
 z;
문자열 str1, str2;
"""

global_vars = find_global_variables4(code_text)
for var_name, line in global_vars:
    print(f"Variable '{var_name}' found at line {line}")
