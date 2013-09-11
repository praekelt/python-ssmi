from setuptools import setup, find_packages

setup(
    name="python-ssmi",
    version="0.0.7",
    url='http://github.com/praekelt/python-ssmi',
    license='BSD',
    description="Python module implementing SSMI for USSD and SMS.",
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    install_requires=[
        'Twisted',
    ],
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
