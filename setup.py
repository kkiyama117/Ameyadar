from setuptools import setup, find_packages

with open('README.txt') as f:
    readme = f.read()

with open('LICENSE') as f:
    MIT = f.read()

setup(
    name='Ameyader',
    version='1.0.1',
    description='SNS account auto rename tools with the weather at a point',
    long_description=readme,
    license=MIT,
    author='',
    author_email='',
    install_requires=['Mastodon.py', 'requests', 'scipy', 'python-decouple',
                      'requests', 'requests_oauthlib'],
    maintainer='kkiyama117',
    maintainer_email='kkiyama117@gmail.com',
    url='https://github.com/5ebec/Ameyadar',
    packages=find_packages(include='src'),
)
