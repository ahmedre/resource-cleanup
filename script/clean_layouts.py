import os
import sys
import subprocess

PATH = sys.argv[1]

for fileName in os.listdir(PATH):
    name = fileName[:-4]
    binding = ''.join(map(lambda x: x[0].upper() + x[1:], name.split('_'))) + 'Binding'
    check1 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "@layout/' + name + '" | wc -l')
    check2 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "R.layout.' + name + '" | wc -l')
    check3 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\'  "' + binding + '" | wc -l')
    if check1.strip() == '0' and check2.strip() == '0' and check3.strip() == '0':
        print("removing: " + fileName)
        os.remove(PATH + fileName)
