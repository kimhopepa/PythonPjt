import re

class Node:
    def __init__(self, line):
        self.line = line.strip()
        self.next = None

    def add_next(self, node):
        self.next = node

    def __str__(self):
        return self.line

def parse_functions(c_code):
    functions = {}
    lines = c_code.split('\n')
    func_pattern = re.compile(r'\b(\w+)\s*\([^)]*\)\s*{')
    current_func = None
    current_func_lines = []

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('//'):
            continue

        func_match = func_pattern.match(stripped_line)
        if func_match:
            if current_func:
                functions[current_func] = current_func_lines
            current_func = func_match.group(1)
            current_func_lines = [line]
        elif current_func:
            current_func_lines.append(line)
            if stripped_line == '}':
                functions[current_func] = current_func_lines
                current_func = None

    if current_func:
        functions[current_func] = current_func_lines

    return functions

def parse_function_body(func_lines):
    nodes = []
    current_node = None

    for line in func_lines:
        stripped_line = line.strip()
        if stripped_line == '{' or stripped_line == '}':
            continue

        if stripped_line.endswith(';'):
            node = Node(line)
            nodes.append(node)
            if current_node:
                current_node.add_next(node)
            current_node = node

    return nodes

def parse_main_function(functions):
    nodes = []
    main_lines = functions.get('main', [])
    current_node = None

    for line in main_lines:
        stripped_line = line.strip()
        if stripped_line == '{' or stripped_line == '}':
            continue

        if stripped_line.endswith(';'):
            node = Node(line)
            nodes.append(node)
            if current_node:
                current_node.add_next(node)
            current_node = node

            func_call_match = re.match(r'(\w+)\s*\([^)]*\)\s*;', stripped_line)
            if func_call_match:
                func_name = func_call_match.group(1)
                if func_name in functions:
                    func_nodes = parse_function_body(functions[func_name])
                    if func_nodes:
                        current_node.add_next(func_nodes[0])
                        current_node = func_nodes[-1]
                        nodes.extend(func_nodes)

    return nodes

def print_nodes(nodes):
    visited = set()
    def dfs(node):
        if not node or node in visited:
            return
        visited.add(node)
        print(node)
        dfs(node.next)

    if nodes:
        dfs(nodes[0])

c_code = """
#include <stdio.h>

void foo() {
    printf("In foo\\n");
}

int main() {
    printf("Start\\n");
    foo();
    printf("In main\\n");
    printf("End\\n");
    return 0;
}
"""

functions = parse_functions(c_code)
nodes = parse_main_function(functions)
print_nodes(nodes)