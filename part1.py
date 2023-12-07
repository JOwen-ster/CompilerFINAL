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

if __name__ == "__main__":
    input_file = 'Finalv1.txt'  # Replace with the actual file name
    output_file = 'Final23.txt'  # Replace with the desired output file name

    format_code(input_file, output_file)

    print(f"Code formatted and saved to {output_file}")