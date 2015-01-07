
from __future__ import print_function

from os.path import dirname, exists, join
import sys, subprocess
from setuptools import setup

setup_dir = dirname(__file__)
base_package = 'netconsole'

# Automatically generate a version.py based on the git version
if exists(join(setup_dir, '.git')):
    p = subprocess.Popen(["git", "describe", "--tags", "--dirty=-dirty"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    # Make sure the git version has at least one tag
    if err:
        print("Error: You need to create a tag for this repo to use the builder")
        sys.exit(1)

    # Create the version.py file
    with open(join(setup_dir, base_package, 'version.py'), 'w') as fp:
        fp.write("# Autogenerated by setup.py\n__version__ = '{0}'".format(out.decode('utf-8').rstrip()))

with open(join(setup_dir, base_package, 'version.py'), 'r') as fp:
    exec(fp.read(), globals())

with open(join(setup_dir, 'README.rst'), 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='pynetconsole',
    version=__version__,
    description='A pure python implementation of a NetConsole listener',
    long_description=long_description,
    author='RobotPy',
    author_email='robotpy@googlegroups.com',
    url='https://github.com/robotpy/pynetconsole',
    keywords='frc first robotics wpilib networktables',
    packages=[base_package],
    license='ISC',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'License :: OSI Approved :: ISC License (ISCL)'
    ],
    entry_points = {
        'console_scripts': ['netconsole = netconsole.netconsole:run']
    }
    )
