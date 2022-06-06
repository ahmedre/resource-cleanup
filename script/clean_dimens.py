import sys
import subprocess
import xml.etree.ElementTree as ET

TARGET = sys.argv[1]
tree = ET.parse(TARGET)
root = tree.getroot()

for child in root:
    name = child.attrib['name']
    check1 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "@dimen/' + name + '" | wc -l')
    check2 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "R.dimen.' + name + '" | wc -l')
    if check1.strip() == '0' and check2.strip() == '0':
        print("removing " + name)
        subprocess.getoutput('xmlstarlet ed -P -L -d "/resources/dimen[@name=\'' + name + '\']" ' + TARGET)
