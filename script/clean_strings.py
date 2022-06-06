import sys
import subprocess
import xml.etree.ElementTree as ET

TARGET = sys.argv[1].replace('/strings.xml', '')
tree = ET.parse(TARGET + '/strings.xml')
root = tree.getroot()

for child in root:
    # only look for strings explicitly (ignore plurals, etc)
    if child.tag != 'string':
        continue

    name = child.attrib['name']
    check1 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "@string/' + name + '" | wc -l')
    check2 = subprocess.getoutput('rg -l -g \'!lint-baseline.xml\' "R.string.' + name + '" | wc -l')
    if check1.strip() == '0' and check2.strip() == '0':
        print("removing: " + name)
        fn = TARGET + '/strings.xml'
        subprocess.getoutput('xmlstarlet ed -P -L -d "/resources/string[@name=\'' + name + '\']" ' + fn)

        # remove from other translations
        subprocess.getoutput('xmlstarlet ed -P -L -d "/resources/string[@name=\'' + name + '\']" ' + TARGET + '-*/strings.xml')
