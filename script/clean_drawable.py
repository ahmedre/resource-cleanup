import sys
import os
import subprocess

# point to a res folder
ROOT = sys.argv[1] 

def files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

for path in files(ROOT):
    if not path.startswith(ROOT + 'drawable'):
        continue
    if path[-4:] not in ('.png', '.xml', '.webp'): continue
    name = path.split('/')[-1][:-4]
    if name[-2:] == '.9':
        name = name[:-2]
    check1 = subprocess.getoutput('rg -l -g \'!line-baseline.xml\' "@drawable/' + name + '" | wc -l')
    check2 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "R.drawable.' + name + '" | wc -l')
    if check1.strip() == '0' and check2.strip() == '0':
        print("removing: " + name)
        os.remove(path)
