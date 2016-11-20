import os
import sys
import glob

class BetterParser:
    def __init__(self):
        self.env_vars = {"$HOME": os.path.expanduser('~')}
    def parse(self, instr):
        instr = instr.rstrip('\r\n\t ')
        # Handle all three steps of parsing:
        # 1: Quoting
        # 2: Expansion (vars, ~, and glob.glob)
        # 3: Splitting
        if (not instr):
            return []
        parse_array = [[],[]]
        parse_state = 0
        # Stage 1: Process quotes
        last_block = []
        for i,c in enumerate(instr):
            if (parse_state == 0):
                # Base state, look for quotes that haven't been escaped
                if (c == '\\'):
                    # Switch to special mode to escape the next character
                    last_block.append(i)
                    parse_state += 3
                elif (c == '"'):
                    # Start double quoting
                    last_block.append(i)
                    parse_state = 1
                elif (c == "'"):
                    # Start single quoting
                    last_block.append(i)
                    parse_state = 2
                else:
                    parse_array[0].append(c)
                    parse_array[1].append(0)
            elif (parse_state == 1):
                if (c not in '$\\"'):
                    parse_array[0].append(c)
                    parse_array[1].append(1)
                elif (c == '$'):
                    parse_array[0].append(c)
                    parse_array[1].append(0)
                elif (c == '\\'):
                    last_block.append(i)
                    parse_state += 3
                else:
                    last_block.pop()
                    parse_state = 0
            elif (parse_state == 2):
                if (c != "'"):
                    parse_array[0].append(c)
                    parse_array[1].append(1)
                else:
                    last_block.pop()
                    parse_state = 0
            elif (3 <= parse_state <= 4):
                last_block.pop()
                parse_array[0].append(c)
                parse_array[1].append(parse_state + 0)
                parse_state -= 3
        if (1 <= parse_state <= 2):
            raise SyntaxError("Unbalanced quotes at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        elif (parse_state == 3):
            raise SyntaxError("Unfinished backslash escape at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        elif (parse_state == 4):
            raise SyntaxError("Unfinished backslash escape within double quotes at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        # State 1.5: Rebuild the parse array, evaluating escaped characters
        temp_array = [[],[]]
        escapes = {'t': '\t', 'r': '\r', 'n': '\n'}
        for i,c in enumerate(parse_array[0]):
            if (3 <= parse_array[1][i] <= 4):
                temp_array[0].append(escapes.get(c,c))
                temp_array[1].append(1)
            else:
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 2: Perform expansions
        for i,c in enumerate(parse_array[0]):
            if ((c == '$') and (parse_array[1][i] == 0)):
                # Unquoted $ detected
                remainder = ''.join(parse_array[0][i:])
                for var_name in self.env_vars.keys():
                    if remainder.startswith(var_name):
                        # Found a variable that needs to be replaced
                        # Blow out the variable name
                        for j in range(i,len(var_name)+i):
                            parse_array[0][j] = ''
                            parse_array[1][j] = -1
                        # Insert the new value
                        parse_array[0][i] = self.env_vars[var_name]
                        parse_array[1][i] = 2
            elif ((c == '~') and (parse_array[1][i] == 0)):
                # Unquoted ~ detected, make sure it's dir-ish
                if ((i == 0) and (len(parse_array[0]) == 1)):
                    # Tilde by itself
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif ((i == 0) and ((parse_array[0][i+1] == '/') or ((parse_array[0][i+1] == ' ') and (parse_array[1][i+1] == 0)))):
                    # Tilde at start, followed by slash or non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif ((len(parse_array[0]) == (i+1)) and ((parse_array[0][i-1] == ' ') and (parse_array[1][i-1] == 0))):
                    # Tilde at end, preceded by a non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif (((parse_array[0][i-1] == ' ') and (parse_array[1][i-1] == 0)) and ((parse_array[0][i+1] == '/') or ((parse_array[0][i+1] == ' ') and (parse_array[1][i+1] == 0)))):
                    # Tilde not at start or end, preceded by a non-escaped space and followed by slash or non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
        # Stage 2.5: Rebuild the parse array, finalizing expansions
        temp_array = [[],[]]
        for i,c in enumerate(parse_array[0]):
            if (parse_array[1][i] == 2):
                for d in c:
                    temp_array[0].append(d)
                    temp_array[1].append(1)
            elif (parse_array[1][i] >= 0):
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 2.7: Wildcard globbing
        temp_groups = [[],[]]
        split_mode = 0
        for i,c in enumerate(parse_array[0]):
            # Pre-split into words based on non-escaped whitespace
            if (not ((c in ' \t\n\r') and (parse_array[1][i] == 0))):
                if (split_mode == 0):
                    split_mode = 1
                    temp_groups[0].append([c])
                    temp_groups[1].append([0 + parse_array[1][i]])
                else:
                    temp_groups[0][-1].append(c)
                    temp_groups[1][-1].append(parse_array[1][i])
            else:
                split_mode = 0
                temp_groups[0].append([c])
                temp_groups[1].append([0 + parse_array[1][i]])
        temp_array = [[],[]]
        seen_first = False
        not_whitespace = False
        for i,chunk in enumerate(temp_groups[0]):
            # Iterate through words looking for unescaped glob characters
            glob_chunk = False
            for j,c in enumerate(chunk):
                if ((c in '*[]?') and (temp_groups[1][i][j] == 0)):
                    # Found a chunk with unescaped glob character, but it's not the first chunk
                    if (seen_first):
                        glob_chunk = True
                if (not seen_first):
                    if (not ((c in ' \t\n\r') and (temp_groups[1][i][j] == 0))):
                        not_whitespace = True
            if (not_whitespace):
                seen_first = True
                not_whitespace = False
            if (glob_chunk):
                # Found a glob containing chunk
                glob_str = ''.join(chunk)
                matches = glob.glob(glob_str)
                if (matches):
                    for match in matches:
                        for c in match:
                            temp_array[0].append(c)
                            temp_array[1].append(1)
                        temp_array[0].append(' ')
                        temp_array[1].append(0)
                    _ = temp_array[0].pop()
                    _ = temp_array[1].pop()
                else:
                    for j,c in enumerate(chunk):
                        temp_array[0].append(c)
                        temp_array[1].append(temp_groups[1][i][j])
            else:
                for j,c in enumerate(chunk):
                    temp_array[0].append(c)
                    temp_array[1].append(temp_groups[1][i][j])
        parse_array = temp_array
        # Stage 2.9: Rebuild the parse array, escaping remaining non-whitespace
        temp_array = [[],[]]
        for i,c in enumerate(parse_array[0]):
            if ((c not in ' \t\n\r') and (parse_array[1][i] == 0)):
                temp_array[0].append(c)
                temp_array[1].append(1)
            else:
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 3: Splitting
        split_mode = 0
        final_value = []
        for i,c in enumerate(parse_array[0]):
            if (parse_array[1][i] == 1):
                if (split_mode == 0):
                    split_mode = 1
                    final_value.append('' + c)
                else:
                    final_value[-1] += c
            else:
                split_mode = 0
        return final_value
