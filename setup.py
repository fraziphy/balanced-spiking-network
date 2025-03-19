import subprocess
import os
from setuptools import setup, find_packages

def get_version():
    """
    Get the latest version from Git tags.
    Fallback to '0.0.0' if no tags are found or Git is unavailable.
    """
    try:
        # Ensure we're in the project root directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Use 'git describe' to get the latest tag
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            universal_newlines=True,
            stderr=subprocess.DEVNULL  # Suppress stderr output
        ).strip()

        # Validate version format
        if not version.startswith('v'):
            raise ValueError(f"Invalid version format: {version}")

        # Remove 'v' prefix
        version = version[1:]

        print(f"Detected version: {version}")
        return version
    except subprocess.CalledProcessError:
        print("Git command failed. Falling back to default version.")
    except Exception as e:
        print(f"Error in get_version: {str(e)}")

    print("Using fallback version 0.0.0")
    return "0.0.0"

setup(
    name='balanced-spiking-network',
    version=get_version(),
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
