from setuptools import setup, find_packages
from pathlib import Path
  
with open('requirements.txt') as f:
    requirements = f.readlines()
 
root_dir = Path(__file__).parent
long_description = (root_dir / "README.md").read_text()
  
setup(
        name ='DataSika',
        version ='1.0.3',
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
        packages=find_packages(),
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
