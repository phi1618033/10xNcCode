import re
import argparse

# Regex to match lines starting with G00, G01, G02, G03 (possibly with leading spaces)
GCODE_LINE_RE = re.compile(r"^\s*(G0[0-3])\b")
# Regex to find X, Y, Z, I, J tokens with floating-point numbers
TOKEN_RE = re.compile(r"([XYZIJ])(-?\d+\.\d+)")


def scale_token(match):
    axis = match.group(1)
    num_str = match.group(2)
    # Determine number of decimal places
    decimals = len(num_str.split('.')[-1])
    # Scale by factor of 10
    scaled = float(num_str) * 10
    # Format with same decimal places
    return f"{axis}{scaled:.{decimals}f}"


def process_line(line):
    # Only scale lines with G00, G01, G02, G03
    if GCODE_LINE_RE.match(line):
        # Substitute all matching tokens
        return TOKEN_RE.sub(scale_token, line)
    else:
        return line


def scale_gcode_file(input_path, output_path):
    """
    Reads G-code from input_path, scales X, Y, Z, I, J coordinates by 10 on G00-G03 moves,
    and writes result to output_path.
    """
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            outfile.write(process_line(line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scale G-code coordinates by factor 10.')
    parser.add_argument('input_file', help='Path to input G-code file')
    parser.add_argument('output_file', help='Path to output scaled G-code file')
    args = parser.parse_args()

    scale_gcode_file(args.input_file, args.output_file)
    print(f"Scaled G-code written to {args.output_file}")
