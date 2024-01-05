import setuptools
from version import get_version

VERSION = get_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="csctracker-queue-scheduler",
    version=VERSION,
    license="MIT",
    author="Carlos Eduardo",
    description="A library for handle scheduled jobs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krlsedu/CscTrackerQueueScheduler.git",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    keywords=['queue', 'scheduled', 'scheduler'],
    classifiers=[
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development",
    ],
    install_requires=required,
    python_requires='>=3',
    include_package_data=True,
)
