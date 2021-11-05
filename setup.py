import os

from setuptools import find_packages, setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()


def requirements():
    dependencies = ["setuptools~=58.0.4"]
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8") as f:
        dependencies.extend([line.strip() for line in f.readlines() if line.strip()])
    return dependencies


setup(
    name="markov-solver",
    version="1.0.0",
    author="Giacomo Marciani",
    description="Utility to solve Markov chains.",
    url="https://github.com/gmarciani/markov-solver",
    license="MIT License",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    install_requires=requirements(),
    entry_points={
        "console_scripts": [
            "markov-solver = markov_solver.cli:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Changelog": "https://github.com/gmarciani/markov-solver/CHANGELOG.md",
        "Issue Tracker": "https://github.com/gmarciani/markov-solver/issues",
        "Documentation": "https://github.com/gmarciani/markov-solver",
    },
)
