from setuptools import find_packages
from setuptools import setup

setup(
    name='asv_localization_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('asv_localization_interfaces', 'asv_localization_interfaces.*')),
)
