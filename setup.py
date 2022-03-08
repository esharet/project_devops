
from setuptools import setup, find_packages


setup(
    name='project_devops',
    version='2022.03.08',
    packages=['project_devops'],
    install_requires=['gitpython',
                     'prettytable',
                     'argparse'],
    zip_safe=True,
    maintainer='es',
    maintainer_email='es@int.com',
    description='git python utilities for every project',
    license='TODO: License declaration',
    include_package_data=True,
    data_files=[
        ('project_devops', ['project_devops/git_command_config.json']),
    ],
    entry_points={
    'console_scripts': [
        'git_command=project_devops.__main__:main',
    ],
},
 
)
