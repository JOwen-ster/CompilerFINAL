rows = {0:'E', 1:'Q', 2:'T', 3:'R', 4:'F'}
cols = {0:'i', 1:'+', 2:'-', 3:'*', 4:'/', 5:'(', 6:')', 7:'$'}
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
      
      
#          a           b          c          d             w          f           0          1           2          3            4           5           6          7          8          9          SEMICOLON          COLON          LAMBDA          program          var          integer          write          begin        end.          +          -          *          /          (          )          id          num          ,          :=          ;          :          lambda          program          var          integer          write          begin          end.          +          -          *          /          (          )          =         "value=",         COMMA  
data = [
        ['blank',   'blank',   'blank',   'blank',     'blank',    'TQ',       'blank',   'blank'], # 0 S
        ['blank',   '+TQ',     '-TQ',     'blank',     'blank',    'blank',    'L',       'L'], # 1 A
        ['FR',      'blank',   'blank',   'blank',     'blank',    'FR',       'blank',   'blank'], # 2 Q
        ['blank',   'L',       'L',       '*FR',       '/FR',      'blank',    'L',       'L'  ], # 3 B
        ['i',       'blank',   'blank',   'blank',     'blank',    '(E)',      'blank',   'blank'], # 4 C
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'L',       'L'  ], # 5 D
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 6 E
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 7 F
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 8 G
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 9 H
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 10 I
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 11 J
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 12 T
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 13 K
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 14 R
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 15 L
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 16 M
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 17 U
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 18 N
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank'], # 19 O
        ['blank',   'blank',   'blank',   'blank',     'blank',    'blank',    'blank',   'blank']  # 20 P
        ]

def compiler():
  expression = input("Input a string with '$' at the end: ") # (a+a)*a$
  if len(expression) == 0 or expression[-1] != '$': # last char but this wont work if the string is empty so we use another case to short circut
    raise CompilerError(rejected)
  
  parsedExpression = expression # (a+a)*a$
  stack = list()
  stack.append('$')
  stack.append('E') # [$, E]
  print(stack)

  popped = stack.pop() # Pop E
  print(stack)
  read = parsedExpression[0] # READ (
  parsedExpression = parsedExpression[1:] # cursor:

# loopstart
  while popped != '$' and read != '$':
    print("Beginning of loop")
    print(popped)
    if popped.isupper(): # checking if its a nonterminal, if its a terminal we need to match popped with read
      goto = data[r(popped)][c(read)] 
      if goto == 'blank':
        print("shoot, goto hit a blank")
        raise CompilerError(rejected)
    
      if goto == 'L':
        print("Lambda found, popping stack") 
        print(stack)
        popped = stack.pop()
        print(stack)
        continue
  
      for element in goto[::-1]: # reverse string and then append
        stack.append(element)
      print("nonterminal found, popping stack, adding elements")
      print(stack)
      popped = stack.pop()
      print(stack)
      
    else: #this is a terminal # append in this else
      if popped != read:
        print("shoot, the terminal we found isn't the one we're looking for")
        raise CompilerError(rejected)
      else:
        print("terminal found, popping stuff and resetting")
        print(stack) #$QR)E
        popped = stack.pop() # E gets popped
        print(stack) #$QR)
        print(read) # read = (
        read = parsedExpression[0] # Switch to next terminal we need to look for
        parsedExpression = parsedExpression[1:]
        print(read) # read = a (!!!!)
    
    
  return accepted
  
print(compiler())