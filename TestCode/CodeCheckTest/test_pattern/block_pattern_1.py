def extract_blocks(code):
    depth = 0
    start = None
    blocks = []

    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if '{' in stripped_line:
            if depth == 0:
                # Capture the block's title from the previous line
                title_line = lines[i - 1].strip() if i > 0 else ''
                start = i
            depth += stripped_line.count('{')

        if '}' in stripped_line:
            depth -= stripped_line.count('}')
            if depth == 0 and start is not None:
                end = i
                blocks.append((title_line, '\n'.join(lines[start:end + 1])))
                start = None

    return blocks


def print_blocks(blocks):
    for title, block in blocks:
        print(f"{title} 제목으로 블록 코드 부분:")
        print(block)
        print()


# Example usage
code = """if(true)
{
   for(int i = 1 ; i <= 10 ; i ++)
   {
   }
}"""

blocks = extract_blocks(code)
print_blocks(blocks)
