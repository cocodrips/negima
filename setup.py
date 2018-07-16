from setuptools import setup

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''
    
setup(
    name='negima',
    version='0.1.0',
    author='cocodrips',
    install_requires=[
        "mecab-python3>=0.7",
        "pandas>=0.19",
        "xlrd>=1.1.0"
    ],
    extras_require={
        'dev': [
            'pytest>=3',
        ],
    },
    long_description=readme,
    license="MIT",
    packages=['negima'],
)
