def convert_to_python(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    python_code = []
    for line in lines:
        # Remove leading and trailing whitespaces and semicolons
        line = line.strip().rstrip(';')

        # Skip empty lines
        if not line:
            continue

        # Check if it's a variable declaration
        if line.startswith("var"):
            variables = line.split(" ")[1:]
            for var in variables:
                python_code.append(f"{var} = 0")

        # Check if it's an assignment statement
        elif line.startswith("begin"):
            continue

        elif line.startswith("end."):
            continue

        elif line.startswith("write"):
            var_name = line.split("(")[1].split(")")[0].strip()
            python_code.append(f'print({var_name})')

        elif "=" in line:
            parts = line.split("=")
            var_name = parts[0].strip()
            value = parts[1].strip()
            python_code.append(f"{var_name} = {value}")

    # Write the generated Python code to the output file
    with open(output_file, 'w') as file:
        file.write("# Program f2023\n")
        file.write("\n".join(python_code))


# Example usage:
input_file_path = 'Final23.txt'  # Replace with the actual file path
output_file_path = 'part3.py'  # Replace with the desired output file path

convert_to_python(input_file_path, output_file_path)