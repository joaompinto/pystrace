from setuptools import setup
import sys
import os
import io

assert sys.version_info >= (3, 6, 0), "requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def setup_package():

    # Get readme
    readme_path = os.path.join(CURRENT_DIR, "README.md")
    with io.open(readme_path, encoding="utf8") as f:
        readme = f.read()

    # Get requiremeents
    with io.open("requirements.txt", encoding="utf8") as f:
        requirements = f.read()

    setup(
        long_description=readme,
        long_description_content_type="text/markdown",
        install_requires=[x for x in requirements.splitlines() if x],
        package_data={
            # If any package contains *.json files, include them:
            "": ["*.json"]
        },
    )


if __name__ == "__main__":
    setup_package()
