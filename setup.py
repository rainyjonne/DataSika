from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = 'This is a package which allows you to create a simple data pipeline by defining a simple yaml file'
  
setup(
        name ='yaml-pipeline-generator',
        version ='1.0.0',
        author ='rainyjonne',
        author_email ='rainyjonne@gmail.com',
        url ='https://github.com/rainyjonne/yaml-pipeline-generator',
        project_urls={
            "Bug Tracker": "https://github.com/rainyjonne/yaml-pipeline-generator/issues",
        },
        description ='Package for building pipeline by yaml file',
        long_description = long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=['yaml_pipeline_generator', 'yaml_pipeline_generator.db', 'yaml_pipeline_generator.task_bypass'],
        entry_points={
            'console_scripts': [
                'yml-gen = yaml_pipeline_generator.main:main'
            ]
        },
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='yaml pipeline generator',
        install_requires = requirements,
        zip_safe = False
)
