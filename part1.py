import re
def format_code(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove comments
    content = re.sub(r'\(\*.*?\*\)', '', content, flags=re.DOTALL)

    # Remove empty lines
    content = '\n'.join(line for line in content.splitlines() if line.strip())

    # Remove tabs and align code
    lines = content.split('\n')
    aligned_lines = []
    for line in lines:
        if line.startswith(('program', 'var', 'begin', 'end')):
            aligned_lines.append(line)
        else:
            aligned_lines.append(' '.join(line.split()))

    content = '\n'.join(aligned_lines).strip()

    with open(output_file, 'w') as file:
        file.write(content)

format_code('Finalv1.txt', 'Final23.txt')