import subprocess
from setuptools import setup, find_packages


def get_version():
    """
    Get the latest version from Git tags.
    Fallback to '0.0.0' if no tags are found or Git is unavailable.
    """
    try:
        # Use 'git describe' to get the latest tag
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            universal_newlines=True
        ).strip()
    except Exception:
        # Fallback if no tags are found or Git is unavailable
        version = "0.0.0"
    return version


setup(
    name='balanced-spiking-network',
    version=get_version(),  # Dynamically fetch version
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'bsn = balanced_spiking_network.cli:main'
        ]
    },
    author='Farhad Razi',
    author_email='farhad.razi.1988@gmail.com',
    description='A balanced spiking neural network simulation package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fraziphy/balanced-spiking-network',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
