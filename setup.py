from setuptools import setup, find_packages
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='freezy',
    version='1.0.0',
    description='Automatic speed calculation through DLC coordinates.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Min Seok Kim',
    author_email='minseok.kim@brain.snu.ac.kr',
    url='https://github.com/minsmis/freezy.git',
    install_requires=['numpy', 'matplotlib', 'pandas'],
    packages=find_packages(exclude=[]),
    keywords=['deeplabcut', 'mouse', 'speed'],
    python_requires='>=3.11',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)
