from distutils.core import setup

setup(
    name             = 'nosehtml',
    version          = '0.1.0',
    author           = 'Lionel Barret',
    author_email     = 'lionel.barret@gmail.com',
    packages         = ['nosehtml', 'nosehtml.tests'],
    scripts          = [],
    #url              = 'http://pypi.python.org/pypi/Reactive/',
    license          = 'LICENSE.txt',
    description      = 'a nose plugin that create a report in html (based on a jinja template).',
    long_description = open('README.md').read(),
    install_requires = [ ],
    entry_points = { 'nose.plugins': [ 'nosehtml = nosehtml:HTMLReport' ]
        },
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Topic :: Communications :: Email',
    'Topic :: Office/Business',
    'Topic :: Software Development :: Testing',
    ],
    )
