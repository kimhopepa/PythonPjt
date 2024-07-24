code = """
int a, b, c = 10;

main()
{
    int local1;
    if (true) {
        int local2;
    }
}

bool function_a(int a, int b, int c= make_dyn_string())
{
    int local3;
}
"""


def extract_global_code(code):
    depth = 0
    global_code = []

    lines = code.splitlines()
    for line in lines:
        line_strip = line.strip()

        if '{' in line_strip:
            depth += 1
        if '}' in line_strip:
            depth -= 1

        if depth == 0 and line_strip.endswith(';'):
            global_code.append(line_strip)

    return '\n'.join(global_code)


global_code = extract_global_code(code)
print(global_code)
