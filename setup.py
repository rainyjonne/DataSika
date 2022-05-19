from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = 'This is a package which allows you to create a simple data pipeline by defining a simple yaml file'
  
setup(
        name ='DataSika',
        version ='1.0.0',
        author ='rainyjonne',
        author_email ='rainyjonne@gmail.com',
        url ='https://github.com/rainyjonne/DataSika',
        project_urls={
            "Bug Tracker": "https://github.com/rainyjonne/DataSika/issues",
        },
        description ='Package for building pipeline by yaml file',
        long_description = long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=['sika', 'sika.db', 'sika.task_bypass'],
        entry_points={
            'console_scripts': [
                'sika = sika.main:main'
            ]
        },
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='sika data pipeline',
        install_requires = requirements,
        zip_safe = False
)
