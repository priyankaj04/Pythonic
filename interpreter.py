import re


# split contents into tokens
def lexer(contents):
    lines = contents.split('\n')
    n_lines = []
    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []
        quote_cnt = 0
        for char in chars:
            if char == '"' or char == "'":
                quote_cnt += 1

            if quote_cnt % 2 == 0:
                in_quotes = False
            else:
                in_quotes = True

            if char == " " and in_quotes == False:
                tokens.append(temp_str)
                temp_str = ""
            else:
                temp_str += char
        tokens.append(temp_str)
        items = []
        for token in tokens:
            if token[0] == "'" or token[0] == '"':
                if token[-1] == "'" or token[-1] == '"':
                    items.append(("string", token))
                    # else: break Throw error
            elif re.match(r"[.a-zA-Z]+", token):
                items.append(("symbol", token))
            elif token in "+-/*%":
                items.append(("expression", token))
            elif re.match(r"[.0-9]+", token):
                items.append(("number", token))
        n_lines.append(items)
    return n_lines


Symbols = ["var", "fun"]

Vars = {}


def parse(file):
    contents = open(file, "r").read()
    lines = lexer(contents)
    for i in range(len(lines)):
        line = lines[i]
        inst_line = ""
        for j in range(len(line)):
            token = line[j]
            if token[0] == 'symbol':
                if token[1] in Symbols:
                    if token[1] == 'var':
                        inst_line += 'Vars["'
                        if re.match(r'[.a-zA-Z0-9_]+', line[j + 1][1]):
                            inst_line += line[j + 1][1] + '"] = '
                        # else: break Throw error
                        inst_line += line[j + 2][i]
                        exec(inst_line)
    print(Vars)
    return lines
