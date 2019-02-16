import keyword
import re

def func_while(l):
  temp = l.replace(" ","")
  line = temp[0:5]+" "+temp[5:]
  if(temp[5] == '('):
    if(temp[-2:] != '):'):
      line = line[:-2] + "):"
    elif(temp[-1:] == ":" and temp[-2:-1] != ')'):
      line = line[:-2] + "):"
  elif(temp[-2:-1] == ")" and temp[5] != "("):
    line = line[:5]+"("+line[5:]
    if(line[-1:] != ":"):
      line = line + ":"
  elif(temp[5] != "(" and temp[-2:-1] != ")"):
    if(temp[-1:] != ":"):
      line = line + ":"
  return line

def func_for(l):
  temp = l.replace(" ","")
  if("inrange" in temp):
    index = temp.index("in")
    if(temp[index+7] != '('):
      temp = temp[:index+7] + "(" + temp[index+7:]
    if(temp[-1] != ":"):
      temp = temp + ":"
    if(temp[-2] != ")"):
      temp = temp[:-1] + "):"
    temp = "for "+temp[3:index] + " in range " + temp[index+7:]
  elif("in" in temp):
    index = temp.index("in")
    if(temp[-1] != ":"):
      temp = temp + ":"
    temp = "for " + temp[3:index] + " in " + temp[index+2:]
  return temp

def func_if(l):
  temp = l.replace(" ","")
  if(temp[-2:] != "):"):
    if(temp[-1] == ":" and temp[-2] != ")"):
      temp = temp[:-1] + "):"
  elif(temp[-1] != ":" and temp[-2] == ")"):
    temp = temp+":"
  else:
    temp = temp + "):"
  if(l.startswith("if")):
    if(temp[2] != '('):
      temp = temp[:2] + "("+temp[2:]
  elif(l.startswith("elif")):
    if(temp[4] != '('):
      temp = temp[:4] + "("+temp[4:]
  return temp

def func_else(l):
  temp = l.replace(" ","")
  if(temp[-1] != ":"):
    temp = temp+":"
  return temp

def func_def(l):
  first_space = l.find(" ",4)
  if(l[first_space+1] != '('):
    l.replace(" ","(",1)
  temp = l.replace(" ","")
  if(temp[0:3] == "def"):
    line = "def "+temp[3:]
  if(temp[-1] != ":"):
    if(temp[-1] != ")"):
      line = line + "):"
    elif(temp[-1] == ")"):
      line = line + ":"
  return line

def func_return(l):
  temp = l.replace(" ","")
  line = temp[0:6]+" "+temp[6:]
  line = "  "+line
  return line

def func_print(l):
  temp = l.replace(" ","")
  word = temp[0:5]
  line = word + " " + temp[5:]
  if(len(line) > 6):
    if(line[6:].isalnum()):
      return line
    elif(line[6] == "\""):
      if(line[-1] == "\'"):
        line = line[:-1] + "\""
      if(line[-1] != "\"" ):
        line = line + "\""
  return line

def error_correction(lines):
  tab_prefix = 0
  keyword_terms = ["for","while","if","else","def"]
  for i in range(len(lines)):
    lines[i] = lines[i].lower()
    a = lines[i].replace(" ","")
    tab_space = "  "
    #while loop
    if a.startswith('while'):
      lines[i] = func_while(lines[i])
      if(lines[0].startswith("def")):
        lines[i] = "  "+lines[i]
    #for loop
    elif a.startswith('for'):
      lines[i] = func_for(lines[i])
      if(lines[0].startswith("def")):
        lines[i] = "  "+lines[i]
    #if function
    elif a.startswith('if'):
      lines[i] = func_if(lines[i])
      if(lines[0].startswith("def")):
        lines[i] = "  "+lines[i]
    #elif function
    elif a.startswith('elif'):
      lines[i] = func_if(lines[i])
      tab_prefix -= 1
      if(lines[0].startswith("def")):
        lines[i] = "  "+lines[i]
    #else function
    elif a.startswith('else'):
      lines[i] = func_else(lines[i])
      tab_prefix -= 1
      if(lines[0].startswith("def")):
        lines[i] = "  "+lines[i]
    #def function
    elif a.startswith('def'):
      lines[i] = func_def(lines[i])
    #def return function
    elif a.startswith('return'):
      tab_prefix = 0
      lines[i] = func_return(lines[i])
    #print function
    elif(i != 0):
      if(a.startswith("print")):
        lines[i] = func_print(lines[i])
      if(" " in lines[i-1]):
        index = lines[i-1].index(" ")
        if(lines[i-1][:index] in keyword_terms):
          tab_prefix += 1
      tab=0
      while(tab < tab_prefix):
        lines[i] = "  "+lines[i]
        tab += 1
  return lines

def has_operator(line):
  # recognizes operator sanitizes operands, returns line (else return line)
  pass

def has_fun_call(line):
  # recognizes function call sanitizes parameters, returns line (else return line)
  pass
