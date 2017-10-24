"""
slf2.0 setup module.
"""

from setuptools import setup, find_packages

setup(
    name='slf',
    version='0.1.0',
    description='slf data agregator',
    url='https://github.com/bigluu/slf_2.0',
    author='Nicolas Bigler',
    author_email='bigli@bigli.ch',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages(),
    install_requires=[
        'influxdb'
        'Flask'
    ],

)
