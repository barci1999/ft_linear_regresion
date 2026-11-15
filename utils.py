def print_box(*lines):
    str_lines = [str(line) for line in lines]

    text_lines = [l for l in str_lines if l != "---"]
    max_len = max(len(line) for line in text_lines) if text_lines else 0
    
    border = "+" + "-" * (max_len + 2) + "+"
    divider = "|" + "-" * (max_len + 2) + "|"
    
    print(border)
    for line in str_lines:
        if line == "---":
            print(divider)
        else:
            print(f"| {line.ljust(max_len)} |")
    print(border)