def decrement_values(filename):
    # Read the original file
    with open(filename, "r") as file:
        lines = file.readlines()

    # Prepare to collect modified lines
    new_lines = []

    for line in lines:
        if "=" in line:
            # Split the line into the part before and after the '='
            parts = line.split("=")
            # Attempt to decrement the integer value
            try:
                # Strip spaces and convert the right part to an integer, then decrement
                modified_value = int(parts[1].strip()) - 1
                # Create the new line with the decremented value
                new_line = f"{parts[0].strip()} = {modified_value}\n"
                new_lines.append(new_line)
            except ValueError:
                # In case there's something that's not an integer, keep the line unchanged
                new_lines.append(line)
        else:
            # If the line does not contain '=', keep it unchanged
            new_lines.append(line)

    # Write the modified lines back to the file
    with open(filename, "w") as file:
        file.writelines(new_lines)


# Specify the path to your file
file_path = "mapping_2023.py"
decrement_values(file_path)
