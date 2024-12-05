from setuptools import setup, find_packages

# Read requirements files
def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read regular requirements
requirements = read_requirements('requirements.txt')

# Read Mac M1/M2 specific requirements if available
try:
    mac_requirements = read_requirements('requirements_mac_arm64.txt')
except FileNotFoundError:
    mac_requirements = []

setup(
    name="asl_classifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'mac_arm64': mac_requirements
    },
    scripts=[
        'scripts/download_dataset.py',
    ],
    py_modules=[
        'asl_cnn',
        'camera',
        'data_collection'
    ],
    author="Ashley Liu, Alex Xie, Veronica Zhao",
    description="ASL Classifier with Real-time Camera Detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/asl-classifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
    entry_points={
        'console_scripts': [
            'download-asl-dataset=scripts.download_dataset:main',
        ],
    }
)
