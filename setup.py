from setuptools import setup
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(name='pyazuread',
    version='0.1',
    install_requires=install_requires,
    description='This package for verify Azure SSO JWT token to rest API.',
    author='Suman Dey',
    author_email='email.sumandey@gmail.com',
    url='https://github.com/deysuman/pyazuread',
    license='MIT',
    packages=['pyazuread'],
    zip_safe=False)