from setuptools import setup


PACKAGE = "ReviewBoard-Persona"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Mozilla Persona support for Review Board",
    author="Steven MacLeod, Mike Conley",
    packages=["reviewboard_persona"],
    entry_points={
        'reviewboard.extensions':
            '%s = reviewboard_persona.extension:RBPersona' % PACKAGE,
    },
    package_data={
        'reviewboard_persona': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/reviewboard_persona/*.txt',
            'templates/reviewboard_persona/*.html',
        ],
    }
)
