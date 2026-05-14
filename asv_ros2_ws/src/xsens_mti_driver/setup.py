from setuptools import find_packages, setup

package_name = 'xsens_mti_driver'

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
    maintainer='StrikePS',
    maintainer_email='pranjal.sinha024@gmail.com',
    description='ROS2 driver for XSENS MTi-630R IMU',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'xsens_imu_node = xsens_mti_driver.xsens_imu_node:main',
            'xsens_imu_node_tester = xsens_mti_driver.xsens_imu_node_tester:main',
        ],
    },
)
