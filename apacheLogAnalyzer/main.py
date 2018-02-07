import os
from datetime import datetime



# path = os.path.dirname(__file__)+'/log_file'

for filename in os.listdir('log_file'):
    i = 0
    prev = datetime.strptime('[Sat Jan 01 01:01:01.000000 2000]', '[%a %b %d %H:%M:%S.%f %Y]')
    with open('log_file/'+filename) as fp:
        for line in fp:
            #print line[:33]
            i += 1
            if (i % 100000) == 0:
                print '[{0}] row number {1}'.format(filename, i)
            current = datetime.strptime(line[:33], '[%a %b %d %H:%M:%S.%f %Y]')

            if current < prev:
                print
                print '[{0}] row number {1} back in time. Delta: {2}'.format(filename, i, prev-current)
                print prevline
                print line
                print

            prev = current
            prevline = line




#datetime_object = datetime.strptime('Fri Feb 02 15:44:33.930165 2018', '%a %b %d %H:%M:%S.%f %Y')
#print datetime_object

