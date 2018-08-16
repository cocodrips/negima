from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='negima',
    version='0.1.1',
    url='https://github.com/cocodrips/negima',
    author='cocodrips',
    author_email='cocodrips@gmail.com',
    description='Extract phases in Japanese text using rules.',
    install_requires=_requires_from_file('requirements.txt'),
    extras_require={
        'dev': [
            'pytest>=3',
        ],
    },
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
