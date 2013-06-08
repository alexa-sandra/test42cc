from django.core.management.base import AppCommand
from optparse import make_option

class Command( AppCommand ):
    option_list = AppCommand.option_list + (make_option('--err-stderr',
            action='store_true',
            dest='err',
            default=False,
            help='duplicate output to stderr'),)

    requires_model_validation = True
    help = 'Prints model names for given application and objects count'
    args = '[appname ...]'


    def handle_app(self, app, **options):
        from django.db.models import get_models

        lines = []

        for model in get_models( app ):
            err = options.get('err')
            val = model.__name__ + " - %s objects" % model._default_manager.count()
            if err:
                self.stderr.write('error:%s'%val)
            else:
                lines.append( val )

        return "\n".join( lines )