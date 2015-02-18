import os
import sys

#paths = [ '/home/webdev/boredshopper',
#          '/home/webdev/boredshopper/boredshopper',
#          '/usr/lib/python2.7/dist-packages',
#          '/usr/local/lib/python2.7/dist-packages',
#]
paths = [ '/home/webdev/boredshopper',
          '/home/webdev/boredshopper/boredshopper',
#          '/home/webdev/venv/lib/python2.7/site-packages',
#          '/home/webdev/venv/lib/python2.7',
          '/usr/lib/python2.7/dist-packages',
          '/usr/local/lib/python2.7/dist-packages',
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

#paths2 = ["/usr/lib/python2.7/dist-packages",
#         "/usr/local/lib/python2.7/dist-packages",]
#for path in paths2:
#    if path in sys.path:
#        sys.path.remove(path)

import site
site.addsitedir('/home/webdev/venv/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'boredshopper.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



