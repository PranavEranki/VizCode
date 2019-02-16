import subprocess

def write_file(code):
  with open('output.py', 'w') as fp:
    fp.writelines(line + '\n' for line in code)

def write_file_str(code):
  with open('output.py', 'w') as fp:
    fp.write(code)

def execute(code):
  if isinstance(code, str):
    write_file_str(code)
  else:
    write_file(code)
  try:
    out = subprocess.check_output(['python', 'output.py'], stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    out = e.output
  return str(out)