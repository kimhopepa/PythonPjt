import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
import re
import lib_function_info as lib

def find_variables(code):
    lines = code.splitlines()
    global_vars = []
    inside_braces = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check if we enter or exit a brace block
        if '{' in stripped_line:
            inside_braces = True
        if '}' in stripped_line:
            inside_braces = False
            continue

        if not inside_braces:
            # Handle "타입 이름, 이름,", "이름, 이름;" and "string version = 10;"
            type_and_var_pattern = re.compile(r'^(?:\w+\s+)?([\w, ]+)(?:[=;]|$)')
            match = type_and_var_pattern.match(stripped_line)
            if match:
                variables_str = match.group(1)
                variables = variables_str.split(',')
                for var in variables:
                    var_name = var.strip()
                    if var_name:
                        # Handle "문자열 띄어쓰기 문자열" and remove special characters
                        words = var_name.split()
                        if len(words) > 1:
                            var_name = words[1]
                        # Remove any trailing special characters
                        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)
                        global_vars = global_vars + [[var_name, i + 1]]
                        # global_vars.append(())  # Store name and line number

    return global_vars

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

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # True if more than one occurrence (considering the declaration line)

def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '//' in line:
            line = line.split('//')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


def find_global_variables5(code):
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
                    # Split by whitespace and take the last element as the variable name
                    words = part.split()
                    var_name = words[-1] if words else ''

                    # Remove any trailing special characters and check if it's a valid identifier
                    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

                    # Exclude numeric-only variables and ensure it starts with an alphabetic character
                    if var_name and not var_name.isdigit() and re.match(r'^[a-zA-Z_]\w*$', var_name):
                        global_vars.append((var_name, i + 1))  # Store name and line number

    return global_vars

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)
    # print(re_text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
