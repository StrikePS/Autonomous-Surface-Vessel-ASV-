from setuptools import find_packages, setup

package_name = 'esc_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='strikeps',
    maintainer_email='pranjal.sinha024@gmail.com',
    description='ESC driver for ROS 2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'esc_driver_node = esc_driver.esc_driver_node:main'
        ],
    },
)
