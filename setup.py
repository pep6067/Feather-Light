from setuptools import setup, find_packages

setup(
    name='featherlight',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'pywin32',
        'cryptography',
        'requests',
        'lz4'
    ],
    entry_points={
        'console_scripts': [
            'featherlight=featherlight.cli:main',
        ],
    },
)
