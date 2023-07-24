# BASIC interpreter

token = ''
variables = {
  'a': '10',
  'b': '6',
  'num': 'a'
}

def execute(num, line):
  try: 
    line = [c for c in line]
    scan(line)
    if token == 'PRINT': print_statement(line)
  except: 
    print('Line ' + str(num) + ': ', end='')
    print('Execution failed!')

def print_statement(line):
  line = [c for c in ''.join(line).strip()]
  scan(line);
  args = ','.join(''.join(line).split(',')[1:])
  if type(token) == str and token[0] == '"':
    print(token[1:-1], end='')
    scan(line);
  else: 
    line = [c for c in ''.join(line).replace(' ', '')]
    print(calc(line), end='')
  if token == ',': print_statement(args)
  else: print()

def calc(line):
  try: 
    result = expression(line)
    if result is not None: return result
    else: print('Bad expression!')
  except: print('Execution failed!')

def expression(line):
  a = term(line)
  while True:
    if token == '+':
      scan(line)
      b = term(line)
      a = a + b
    elif token == '-':
      scan(line)
      b = term(line)
      a = a - b
    else: return a

def term(line):
  a = factor(line)
  while True:
    scan(line)
    if token == '*':
      scan(line)
      b = factor(line)
      a = a * b
    elif token == '/':
      scan(line)
      b = factor(line)
      a = int(a / b)
    else: return a

def factor(line):
  if type(token) == int: return token
  if token == '(':
    scan(line); a = expression(line)
    if a == None: return None
    if token == ')': return a
    else: return None
  elif token == '-':
    scan(line)
    return -factor(line)
  else: return None

def number(line):
  num = 0; tok = ''
  while len(line) and line[0].isdigit():
    tok += line[0]
    del line[0]
    num = int(tok)
  return num

def variable(line):
  name = ''
  while len(line) and line[0].islower():
    name += line[0]
    del line[0]
  if name not in variables:
    print('Variable "' + name + '" is not defined!')
  try: return int(variables[name])
  except: return int(variables[variables[name]])

def statement(line):
  keyword = ''
  while len(line) and line[0].isupper():
    keyword += line[0]
    del line[0]
  if keyword not in ['PRINT', 'LET', 'IF', 'THEN', 'GOTO']:
    print('Unknown keyword "' + keyword + '"')
    raise ValueError
  else: return keyword

def operator(line):
  op = line[0]
  del line[0]
  return op

def string(line):
  msg = ''; del line[0]
  while len(line) and line[0] != '"':
    msg += line[0]
    del line[0]
  if not len(line):
    print('Missing closing \'"\'!')
    raise ValueError
  else: del line[0]; return '"' + msg + '"'

def scan(line):
  global token
  if len(line) and line[0].isdigit(): token = number(line)
  elif len(line) and line[0].islower(): token = variable(line)
  elif len(line) and line[0].isupper(): token = statement(line)
  elif len(line) and line[0] in '+-*/()=<>,': token = operator(line)
  elif len(line) and line[0] == '"': token = string(line)

line = 'PRINT 5, " ", 2*2, " ", "Hello, world!", " ", -((12+12)/4 + a * (b-17)), " ", "hi there"'
execute(0, line)

