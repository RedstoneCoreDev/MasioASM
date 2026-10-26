# ========================================== #
# MasioASM Macro Preprocessor Source Code    #
# License: BSD 3-Clause License              #
# Copyright (c) 2026 RedstoneCoreDev         #
# ========================================== #

import argparse

# args parser setup
parser = argparse.ArgumentParser(description="Masio Preprocessor")
parser.add_argument(
    "action", choices=["transform", "compile"], help="Only transform or compile too"
)
parser.add_argument("filename", help="the .masio file to transform/compile")

args = parser.parse_args()
file_in = args.filename

# enforce .masio file extension
if not file_in.endswith(".masio"):
    print(f"cannot {args.action}: file is not a masio file")
    exit(1)

# split from the right, only once,
# take everything before the last dot
file_raw = file_in.rsplit(".", 1)[0]

# make all filenames
file_masio = file_raw + ".masio"
file_out = file_raw + ".nasm"
file_object = file_raw + ".o"


def generate_string(elements, line, indent):

    index = 0
    final = ""
    while index < len(elements):
        final += elements[index]

        index += 1

        return final


print_function = False
string_number = 0
strings_data_section = {}


def expand_macros(elements, line, indent, in_start):

    index = 0
    output = []
    while index < len(elements):
        current = elements[index]

        match current:
            case "print":
                global print_function
                global string_number
                print_function = True

                string_number += 1
                string_name = f"_print_str_{string_number}"

                start_index = line.find('"')
                end_index = line.rfind('"')

                if start_index != end_index and start_index != -1 and end_index != -1:
                    string = line[start_index + 1 : end_index]

                string_size = len(string)

                strings_data_section[string_name] = string

                output.append(f"{indent}mov rsi, {string_name}\n")
                output.append(f"{indent}mov rdx, {string_size}\n")
                output.append(f"{indent}call _print\n")
                break

            case "zero":
                next = elements[index + 1]
                output.append(f"{indent}xor {next}, {next}\n")
                index += 2

            case "Fn":
                next = elements[index + 1]
                if next == "_start":
                    in_start = True
                else:
                    in_start = False
                if not ":" in next:
                    next += ":"
                output.append(f"{next}\n")
                index += 1

            case "FSetup":
                output.append(f"{indent}push rbp\n")
                output.append(f"{indent}mov rbp, rsp\n")

            case "FDestroy":
                output.append(f"{indent}mov rsp, rbp\n")
                output.append(f"{indent}pop rbp\n")

            case "return":
                try:
                    exit_code = int(elements[index + 1])
                except Exception:
                    exit_code = ""

                if in_start:
                    if exit_code == 0 or exit_code == "":
                        output.append(f"{indent}xor rdi, rdi\n")
                    else:
                        output.append(f"{indent}mov rdi, {exit_code}\n")

                    output.append(f"{indent}mov rax, 60\n")
                    output.append(f"{indent}syscall\n")
                    index += 1

                else:
                    if exit_code != "":
                        output.append(f"{indent}mov rax, {exit_code}\n")
                        index += 1
                    else:
                        output.append(f"{indent}xor rax, rax\n")

                    output.append(f"{indent}mov rsp, rbp\n")
                    output.append(f"{indent}pop rbp\n")

            case _:
                output.append(current + "\n")
                break

        index += 1

    return in_start, output


def transform():

    with open(file_in, "r") as source, open(file_out, "w") as dest:
        in_start = False
        first_hit = 0
        for line in source:
            elements = line.split()

            indent = 4 * " "

            if len(elements) == 0:
                dest.write("\n")

            elif elements[0] in (";", "//", "#", "--"):
                elements[0] = ";"

                final = ""
                if line.startswith(" "):
                    final = indent
                final += " ".join(elements) + "\n"
                dest.write(final)

            else:
                if first_hit == 0:
                    first_hit = 1
                if first_hit == 1:
                    first_hit = -1
                    dest.write("section .text\n")
                    dest.write("global _start\n\n")
                in_start, output = expand_macros(elements, line, indent, in_start)
                dest.write("".join(output))

        if print_function:
            dest.write("\n")
            dest.write("_print:\n")
            print_function_instructions = [
                "push rbp",
                "mov rbp, rsp",
                "mov rax, 1  ; sys_write",
                "mov rdi, 1  ; stdout",
                "; rsi already holds the string pointer",
                "; rdx already holds the string length",
                "syscall",
                "mov rsp, rbp",
                "pop rbp",
                "ret",
            ]
            for item in print_function_instructions:
                dest.write(f"{indent}{item}\n")

            dest.write("\n")
            dest.write("section .data\n")
            for key, value in strings_data_section.items():
                dest.write(f'{indent}{key} db "{value}", 0')


def compile():
    import subprocess
    import platform

    os_name = platform.system()

    if os_name == "Linux":
        subprocess.run(["nasm", "-f", "elf64", file_out, "-o", file_object], check=True)
        subprocess.run(["ld", file_object, "-o", file_raw], check=True)
    elif os_name == "Darwin":
        subprocess.run(
            ["nasm", "-f", "macho64", file_out, "-o", file_object], check=True
        )
        subprocess.run(
            [
                "ld",
                "-e",
                "_start",
                "-o",
                file_raw,
                file_object,
                "-syslibroot",
                subprocess.run(
                    ["xcrun", "--show-sdk-path"],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip(),
                "-lSystem",
            ],
            check=True,
        )
    elif os_name == "Windows":
        subprocess.run(["nasm", "-f", "win64", file_out, "-o", file_object], check=True)
        subprocess.run(["gcc", file_object, "-o", file_raw, "-lkernel32"], check=True)
    else:
        print("unsupported operating system", os_name)
        print("transform file and compile manually")


if args.action == "compile":
    transform()
    compile()
elif args.action == "transform":
    transform()
