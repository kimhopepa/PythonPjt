import re

def find_global_variables(text_code):
    lines = text_code.splitlines()
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

            # Check for exclusion condition: single word without ',', '=', ';'
            if ',' not in left_side and '=' not in stripped_line and ';' not in stripped_line:
                continue

            # Further split by delimiters ',', ';' and process each part
            parts = re.split(r'[;,]', left_side)
            for part in parts:
                part = part.strip()
                # Ignore parts containing parentheses
                if '(' in part or ')' in part:
                    continue
                if part:
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

# Example usage
text_code = """
int a, b, c;
const int define_dp_name = "master_dp";
char d;
void func();
try
catch
"""

global_vars = find_global_variables(text_code)
for var_name, line in global_vars:
    print(f"Variable '{var_name}' found at line {line}")
