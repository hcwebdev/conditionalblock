from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


MAJOR = 0
MINOR = 1
PATCH = 2


name = 'conditionalblock'
version = '%s.%s.%s' % (MAJOR, MINOR, PATCH)
long_description = '\n'.join([
    read('docs', 'README.txt'),
    '',
    'Changelog',
    '*********',
    '',
    read('docs', 'CHANGES.txt'),
])


setup(name=name,
      version=version,
      description="django templatetag to display block iff child block exists",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        'Framework :: Django',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='django templatetags',
      author='Jacob Radford',
      author_email='webmaster@hunter.cuny.edu',
      url='http://github.com/hcwebdev/conditionalblock/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
