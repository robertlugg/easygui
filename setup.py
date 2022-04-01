import distutils.core
## WARNING: Although the following import appears to do nothing, it is required for bdist_wheel to be recognized
from setuptools import setup, find_packages

version = "0.98.3"
release = "0.98.3"

desc = list()
desc.append('EasyGUI is a module for very simple, very easy GUI programming in Python.  ')
desc.append('EasyGUI is different from other GUI generators in that EasyGUI is NOT event-driven.  ')
desc.append('Instead, all GUI interactions are invoked by simple function calls.')

with open('README.md', "r", encoding='utf-8') as f:
    long_description = f.read()

distutils.core.setup(
    name='easygui',
    version=version,
    url='https://github.com/robertlugg/easygui',
    description=''.join(desc),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='easygui developers and Stephen Ferg',
    author_email='robert.lugg@gmail.com',
    license='BSD',
    keywords='gui linux windows graphical user interface',
    packages=['easygui', 'easygui.boxes'],
    package_data={
        'easygui': ['python_and_check_logo.*', 'zzzzz.gif']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: User Interfaces',
        ]
    )

