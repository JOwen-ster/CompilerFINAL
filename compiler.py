import re # regex

rows = {
0:'E',
1:'F',
2:'G',
3:'H',
4:'I',
5:'J',
6:'T',
7:'K',
8:'R',
9:'L',
10:'M',
11:'U',
12:'N',
13:'O',
14:'P'
}


cols = {
0:'a',          
1:'b',         
2:'c',         
3:'d',            
4:'w',         
5:'f',          
6:'0',         
7:'1',          
8:'2',          
9:'3',          
10:'4',           
11:'5',           
12:'6',           
13:'7',           
14:'8',           
15:'9',       
16:';',          
17:':',          
18:'LAM',          
19:'program', # START STATE                     
20:'var',          
21:'integer',          
22:'write',          
23:'begin',        
24:'end.',          
25:'+',         
26:'-',          
27:'*',          
28:'/',          
29:'(',          
30:')',          
31:'=',          
32:'"value=",',         
33:','   
}


accepted = 'Accepted'
rejected = 'Rejected'
class CompilerError(Exception):
  pass

def r(row):
   for key in rows.keys():
      if rows.get(key) == row:
        return key
      
def c(col):
   for key in cols.keys():
      if cols.get(key) == col:
         return key
      
# terminals
reservedwords = ['program', 'var', 'integer', 'write', 'begin', 'end.']   
terminals = [":", ";", "=", "+", "-", "*", "/", "(", ")", ",", '"value="', "$"]
allowed_letters = ['a', 'b', 'c']
allterminals = [
    'a', 'b', 'c', 'd', 'w', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ';', ':', 'LAM', 'program', 'var', 'integer', 'write', 'begin', 'end.',
    '+', '-', '*', '/', '(', ')', '=', '"value=",', ','
]


#          a           b          c          d             w          f           0          1           2           3           4           5           6           7           8           9       SEMICOLON          COLON          LAMBDA          program                   var          integer          write          begin        end.          +          -          *          /          (          )          =          "value=",          ,   
data = [
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank','program A; var B begin E end.','blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 0 S
        ['PQ',      'PQ',      'PQ',      'PQ',        'PQ',       'PQ',       'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 1 A
        ['PQ',      'PQ',      'PQ',      'PQ',        'PQ',       'PQ',       'OQ',      'OQ',       'OQ',       'OQ',       'OQ',       'OQ',       'OQ',       'OQ',       'OQ',       'OQ',       'LAM',           'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 2 Q
        ['C:D;',    'C:D;',    'C:D;',    'C:D;',      'C:D;',     'C:D;',     'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'LAM',     'LAM',     'LAM',     'LAM',     'blank',   'LAM',      'blank',    'blank',         'blank'  ], # 3 B
        ['A',       'A',       'A',       'A',         'A',        'A',        'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 4 C
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'integer',      'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 5 D
        ['F',       'F',       'F',       'F',         'F',        'F',        'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 6 E
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'F',           'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 7 F
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'G',           'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 8 G
        ['LAM',     'LAM',     'LAM',     'LAM',       'LAM',      'LAM',      'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'write(HA);',  'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'value=',        'blank'  ], # 9 H
        ['blank',   'blank',   'blank',   'blank',     'A=J;',     'A=J;',     'A=J;',    'A=J;',     'A=J;',     'A=J;',     'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 10 I
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'KT',       'KT',       'KT',       'KT',       'KT',       'KT',       'KT',       'KT',       'KT',       'blank',         'blank',        'KT',           'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'KT',      'KT',      'KT',      'KT',      'KT',      'blank',    'blank',    'blank',         'blank'  ], # 11 J
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'LAM',           'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     '+KT',     '-KT',     'blank',   'blank',   'blank',   'LAM',      'blank',    'blank',         'blank'  ], # 12 T
        ['LR',      'LR',      'LR',      'LR',        'LR',       'LR',       'LR',      'LR',       'LR',       'LR',       'LR',       'LR',       'LR',       'LR',       'LR',       'LR',       'blank',         'blank',        'LR',           'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'LR',      'LR',      'blank',   'blank',   'LR',      'blank',    'blank',    'blank',         'blank'  ], # 13 K
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'LAM',           'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'LAM',     'LAM',     '*LR',     '/LR',     'blank',   'LAM',      'blank',    'blank',         'blank'  ], # 14 R
        ['A',       'A',       'A',       'A',         'A',        'A',        'M',       'M',        'M',        'M',        'M',        'M',        'M',        'M',        'M',        'M',        'blank',         'blank',        'M',            'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'M',         'M',     'blank',   'blank',   '(J)',     'blank',    'blank',    'blank',         'blank'  ], # 15 L
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'NU',           'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'NU',      'NU',      'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 16 M
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'OU',      'OU',       'OU',       'OU',       'OU',       'OU',       'OU',       'OU',       'OU',       'OU',       'LAM',           'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'LAM',      'blank',    'blank',         'blank'  ], # 17 U
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'LAM',     'LAM',      'LAM',      'LAM',      'LAM',      'LAM',      'LAM',      'LAM',      'LAM',      'LAM',      'LAM',           'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     '+',       '-',       'LAM',     'LAM',     'blank',   'LAM',      'blank',    'blank',         'blank'  ], # 18 N
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    '0',       '1',        '2',        '3',        '4',        '5',        '6',        '7',        '8',        '9',        'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ], # 19 O
        ['a',       'b',       'c',       'd',         'w',        'f',        'blank',   'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',    'blank',         'blank',        'blank',        'blank',                'blank',       'blank',        'blank',       'blank',    'blank',     'blank',   'blank',   'blank',   'blank',   'blank',   'blank',    'blank',    'blank',         'blank'  ]  # 20 P
        ]

def compiler(content):
    errors = []

    # Define all the terminal values
    reserved_words = ["program", "var", "begin", "end.", "integer", "write"]
    terminals = [":", ";", "=", "+", "-", "*", "/", "(", ")", ",", '"value="', "$"]
    allowed_letters = "abcdfl"

    # Check for required keywords
    required_keywords = ['program', 'var', 'begin', 'end.']
    for keyword in required_keywords:
        if keyword not in content:
            errors.append(f"{keyword} is expected (missing or spelled wrong)")

    # Check for required declarations
    required_declarations = ['integer', 'write']
    for declaration in required_declarations:
        if re.search(fr'\b{declaration}\b', content) is None:
            errors.append(f"{declaration} is expected (missing or spelled wrong)")

    # Check for missing symbols
    missing_symbols = {
        ';': 'semicolon',
        ',': 'comma',
        '.': 'period',
        '(': 'left parentheses',
        ')': 'right parentheses',
    }

    for symbol, description in missing_symbols.items():
        if symbol not in content:
            errors.append(f"{description} is missing")

    # Check for mismatched parentheses
    left_parentheses_count = content.count('(')
    right_parentheses_count = content.count(')')
    if left_parentheses_count != right_parentheses_count:
        errors.append("Mismatched left and right parentheses")
        if left_parentheses_count > right_parentheses_count:
            errors.append("Right parentheses is missing")
        else:
            errors.append("Left parentheses is missing")

    # Check for unknown identifiers
    known_identifiers = set(['program', 'var', 'begin', 'end.', 'integer', 'write', 'a1', 'b2a', 'end', 'value', 'ba', 'c', 'f2023'])
    unknown_identifiers = set(re.findall(r'\b[a-zA-Z_]\w*\b', content)) - known_identifiers
    for unknown_identifier in unknown_identifiers:
        errors.append(f"Unknown identifier: {unknown_identifier}")

    # Check for missing semicolons at the end of lines
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.endswith(';') and line not in ['var', 'begin', 'end.']:
            errors.append(f"Missing semicolon at the end of line: {line}")

    if len(errors) == 0:
        print("Accepted")
    else:
        print(errors)

# Specify the path to your text file
file_path = 'Final23.txt'

# Read the content of the file
with open(file_path, 'r') as file:
    file_content = file.read()

# Call the function to check for errors
compiler(file_content)