from setuptools import setup, find_packages

def listify(filename):
    return filter(None, open(filename, 'r').read().split('\n'))

setup(
    name="python-ssmi",
    version="0.0.7",
    url='http://github.com/praekelt/python-rm',
    license='BSD',
    description="Python module implementing SSMI for USSD and SMS.",
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    install_requires=listify('requirements.pip'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
