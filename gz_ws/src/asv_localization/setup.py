from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'asv_localization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/data', glob('data/*.csv')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='strikeps',
    maintainer_email='pranjal.sinha024@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'GzSim_StateEstimate = asv_localization.GzSim_StateEstimate:main',
            'echo_state_estimate = asv_localization.echo_state_estimate:main',
        ],
    },
)
