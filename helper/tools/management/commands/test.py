# -*- coding: utf8 -*-
# Python
from datetime import datetime
import sys
# Django
from django.core.management.base import BaseCommand, CommandError
# Custom
from tools.utils.discoverer import DomainDiscover
# Settings
reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    
    def __init__(self):
        super(Command, self).__init__()


    def add_arguments(self, parser):
        # Named (optional) arguments

        parser.add_argument(
            '-t',
            '--test',
            type=int,
            help='python manage.py XXXX --test XXXX',
        )


    def handle(self, *args, **options):
        print
        print
        start_date = datetime.now()
        print "----------------------------------------------"
        print "[%s] Iniciando" % start_date.strftime("%Y-%m-%d %H:%M:%S")
        print "----------------------------------------------"

        DD = DomainDiscover()
        a = DD.discover(domain="email.towebs.com")
        print(a)

        finish_date = datetime.now()
        print "**********************************************"
        print "[%s] Terminando" % finish_date.strftime("%Y-%m-%d %H:%M:%S")
        print "----------------------------------------------"
        self.stdout.write(
            self.style.SUCCESS('[ %s ] tardo el script en ejecutarse' % (finish_date - start_date))
        )
        print "**********************************************\n\n"
