import ipdb

fileout = None


def write_line(line):
    fileout.write(line+ '\n')


def is_start_of_obj(line):
    return line == '  {\n'


def is_end_of_obj(line):
    return line == '  },\n' or line == '  }\n'


def remove_carriage_return(line):
    return line.replace('\\r\\n', ' ')


def json_parser(filein):
    json_string = []
    for line in filein:
        is_start = False
        is_end = False
        if is_start_of_obj(line):
            is_start = True
            json_string = ''
        elif is_end_of_obj(line):
            is_end = True

        line = line.strip()
        line = remove_carriage_return(line)
        if is_start:
            json_string += '' + line
        elif is_end:
            json_string += ' }'
        else:
            json_string += ' ' + line

        if is_end:
            write_line(json_string)
            json_string = ''


def parse_file(file_name):
    with open(file_name) as fp:
        json_parser(fp)


def main():
    input_file = 'hard.json'
    output_file = 'hard_parsed.json'
    fileout = open(output_file, 'w')
    parse_file(input_file)
    fileout.close()


if __name__ == "__main__":
    main()