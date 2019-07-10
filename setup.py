# -*- coding: utf-8 -*-
"""

"""

import os
import subprocess
from setuptools import setup, find_packages


# Change version number here, not in neurotic/version.py, which is generated
# by this script. Try to follow recommended versioning guidelines at semver.org.
MAJOR       = 0     # increment for backwards-incompatible changes
MINOR       = 6     # increment for backwards-compatible feature additions
MICRO       = 0     # increment for backwards-compatible bug fixes
IS_RELEASED = True  # determines whether version will be marked as development
VERSION     = f'{MAJOR}.{MINOR}.{MICRO}'

# Try to fetch the git revision number from the .git directory if it exists,
# as well as whether the working directory is dirty or not.
if os.path.exists('.git'):
    try:
        out = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                               stdout=subprocess.PIPE).communicate()[0]
        GIT_REVISION = out.strip().decode('ascii')

        out = subprocess.Popen(['git', 'diff', '--stat'],
                               stdout=subprocess.PIPE).communicate()[0]
        if out.strip().decode('ascii'):
            GIT_DIRTY = True
        else:
            GIT_DIRTY = False
    except OSError:
        GIT_REVISION = 'unknown'
        GIT_DIRTY = None
# If the .git directory is absent (perhaps because this is a source distro), or
# if git is not available, try to fetch the rev number and dirty state from
# neurotic/version.py where it may have been stored during packaging.
elif os.path.exists('neurotic/version.py'):
    try:
        v = {}
        with open('neurotic/version.py', 'r') as f:
            exec(f.read(), v)
        GIT_REVISION = v['git_revision']
        GIT_DIRTY = v['git_dirty']
    except ImportError:
        raise ImportError('Unable to import git_revision. Try removing ' \
                          'neurotic/version.py and the build directory ' \
                          'before building.')
else:
    GIT_REVISION = 'unknown'
    GIT_DIRTY = None

# If this is not a release version, mark it as a development build/distro and
# tag it with the git revision number and dirty state.
if not IS_RELEASED:
    VERSION += '.dev+git.' + GIT_REVISION[:7]
    if GIT_DIRTY:
        VERSION += '.dirty'

# Write the version string to a file that will be included with the
# build/distro. This makes the string accessible to the package via
# neurotic.__version__. The git revision and dirty state are also written in
# case a source distro is being built, so that they can be fetched later during
# installation.
with open('neurotic/version.py', 'w') as f:
    try:
        f.write('"""THIS FILE WAS GENERATED BY SETUP.PY DURING BUILDING/PACKAGING"""\n')
        f.write(f'version = \'{VERSION}\'\n')
        f.write(f'git_revision = \'{GIT_REVISION}\'\n')
        f.write(f'git_dirty = {GIT_DIRTY}\n')
    finally:
        f.close()

# Read in the README to serve as the long_description, which will be presented
# on pypi.org as the project description.
with open('README.rst', 'r') as f:
    README = f.read()

# Unreleased versions of ephyviewer and neo are needed by this package, and the
# dev version of neo conflicts with the overly restrictive requirements of
# elephant. The only way around the latter complication is for the user to
# manually install dependencies using `pip install -r requirements.txt`, which
# warns about the incompatibility of neo and elephant but doesn't halt.
# Someday this package may be able to use the specification below, but not
# before neo releases AxographRawIO in a form compatible with elephant.
install_requires = [
    # 'av',
    # 'elephant>=0.6.2',
    # 'ephyviewer @ https://github.com/NeuralEnsemble/ephyviewer/archive/master.tar.gz', # latest version
    # 'ipywidgets',
    # 'neo @ https://github.com/NeuralEnsemble/python-neo/archive/master.tar.gz', # TODO require >0.7.1 for AxographRawIO
    # 'numpy',
    # 'pandas',
    # 'pylttb',
    # 'pyqt5',
    # 'pyyaml',
    # 'quantities',
    # 'tqdm',
]

# Can't use this method of reading requirements.txt into install_requires until
# this package depends only on released packages and not development versions.
# This is because git commands ("git+https://github...") in requirements.txt
# cannot be understood by setuptools. The "@" notation for specifying urls used
# above could be placed in an external file like requirements.txt in lieu of
# git commands, but then `pip install -r requirements.txt` cannot read it. So,
# to get `pip install neurotic` to install the development version of
# ephyviewer, it will be necessary to use the "@" notation, and it probably
# shouldn't be put in an external file with the name requirements.txt because
# it won't be usable in the normal way with `pip install -r requirements.txt`.
# with open('requirements.txt', 'r') as f:
#     install_requires = f.read()

extras_require = {}
with open('requirements-notebook.txt', 'r') as f:
    extras_require['notebook'] = f.read()
with open('requirements-tests.txt', 'r') as f:
    extras_require['tests'] = f.read()

setup(
    name = 'neurotic',
    version = VERSION,
    description = 'Curate, visualize, and annotate your behavioral ephys data using Python',
    packages = find_packages(),
    package_data = {'neurotic': ['example/metadata.yml'], 'neurotic.tests': ['metadata-for-tests.yml']},
    install_requires = install_requires,
    extras_require = extras_require,
    entry_points = {'console_scripts': ['neurotic=neurotic.scripts:main']},
    long_description = README,
    keywords = ['neuroscience', 'electrophysiology', 'visualization',
        'video-sync', 'data-management', 'data-sharing', 'download-manager',
        'annotation-tool', 'open-science', 'python-neo'],
    author = 'Jeffrey Gill',
    author_email = 'jeffrey.p.gill@gmail.com',
    license = 'MIT',
    url = 'https://github.com/jpgill86/neurotic',
    project_urls={
        # 'Documentation': 'https://github.com/jpgill86/neurotic',
        'Source code': 'https://github.com/jpgill86/neurotic',
        'Bug tracker': 'https://github.com/jpgill86/neurotic/issues',
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
