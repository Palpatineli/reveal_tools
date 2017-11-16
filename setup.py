from setuptools import setup

setup(
    name='reveal_tools',
    version='0.1.0',
    packages=['reveal_tools'],
    url='https://github.com/Palpatineli/reveal_tools',
    download_url='https://github.com/Palpatineli/reveal_tools/archive/0.1.0.tar.gz',
    license='GPLv3',
    author='Keji Li',
    author_email='mail@keji.li',
    entry_points={'console_scripts': ['reveal_cleanfigs = reveal_tools.clean:clean']},
    description='convenience functions for manipulating revealjs presentations',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 3']
)
