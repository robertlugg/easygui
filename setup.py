import distutils.core
from setuptools import setup, find_packages
import easygui

version = "0.97.2"
release = '0.97.2 (2014-12-24)'

desc = list()
desc.append('EasyGUI is a module for very simple, very easy GUI programming in Python.  ')
desc.append('EasyGUI is different from other GUI generators in that EasyGUI is NOT event-driven.  ')
desc.append('Instead, all GUI interactions are invoked by simple function calls.')

distutils.core.setup(
    name='easygui',
    version=version,
    url='http://easygui.sourceforge.net/',
    description=''.join(desc),
    long_description=easygui.__doc__,
    author='Stephen Ferg and Robert Lugg (active)',
    author_email='robert.lugg@gmail.com',
    license='BSD',
    keywords='gui windows graphical user interface',
    packages=['easygui'],
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
        'Topic :: Software Development :: User Interfaces',
        ]
    )
