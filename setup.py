from setuptools import setup, find_packages

setup(
        name = "python-ssmi",
        version = "0.0.4",
        url = 'http://github.com/praekelt/python-ssmi',
        license = 'proprietary',
        description = "Python module implementing SSMI for USSD and SMS.",
        author = 'Morgan Collett',
        author_email = 'morgan@praekelt.com',
        packages = find_packages('src'),
        package_dir = {'': 'src'},
        install_requires = ['setuptools'],
)
