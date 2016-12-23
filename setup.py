from distutils.core import setup

config = {
    'name':        'suijin',
    'description': 'Suijin: A Hydroanalysis tool with flow direction and flow accumulation support',
    'author':      'Renato M. Costa',
    'url':         'https://github.com/rmascarenhas/suijin',
    'version':     '0.1',
    'packages':    ['suijin'],
    'scripts':     []
}

setup(**config)
