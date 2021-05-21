import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import spot
from ltl_sat_check import sat_check
import io
from GORE import GoreCase

gore_cases = []

case_file = io.open('GORE_case.txt', 'r', encoding='utf-8')
temp_case = {}
in_bc = False
for line in case_file.readlines():
  line = line.rstrip('\n')
  if len(line) > 0:
    if line.startswith('CASE:'):
      in_bc = False
      line = line[5:]
      temp_case = {}
      temp_case['name'] = line
      temp_case['BC'] = []
    if in_bc:
      temp_case['BC'].append(line)
    if line.startswith('BC:'):
      in_bc = True
    if line.startswith('DOM:'):
      line = line[5:-1]
      temp_case['doms'] = line.split(',') if  len(line) > 0 else []
    if line.startswith('GOALS:'):
      line = line[7:-1]
      temp_case['goals'] = line.split(',')
      gore_cases.append(temp_case)

gc_list = []
for case in gore_cases:
  gc_list.append(GoreCase(case['name'], case['doms'], case['goals'], case['BC']))


def check_nonsensebc_right():
  for gc in gc_list:
    print(gc.name)
    nonsense_bc = gc.getNonsenseBC()
    for bc in nonsense_bc:
      print(gc.isBC(bc, show_reason = True))


def is_nonsense_good():
  output_file = io.open('case_result.txt', 'w+', encoding = 'utf-8')
  for gc in gc_list:
    print(gc.name)
    output_file.write('case: ' + gc.name + '-----------------------------\n')
    nonsense_bc = gc.getNonsenseBC()
    excluded_bc = set()
    for n_bc in nonsense_bc:
      for bc in gc.gen_t_bc:
        if gc.isGeneral(n_bc, bc):
          excluded_bc.add(bc)
          output_file.write('bc: ' + bc.to_str() +'\n be generaled by n_bc: ' + n_bc.to_str() + '\n')
        elif gc.isWitness(n_bc, bc):
          excluded_bc.add(bc)
          output_file.write('bc: ' + bc.to_str() +'\n be witnessed by n_bc: ' + n_bc.to_str() + '\n')
    if len(excluded_bc) < len(gc.gen_t_bc):
      for bc in gc.gen_t_bc:
        if bc not in excluded_bc:
          print('!!!!\n' + bc.to_str())

if __name__ == '__main__':
  # check_nonsensebc_right()
  is_nonsense_good()
# f = spot.formula('[](l -> <>!l) && [](!p -> (!m && X l)) && []((!l && p) -> m) && X X (!m && []!l)')
# a = f.translate('ba')
# print(a.is_empty())
