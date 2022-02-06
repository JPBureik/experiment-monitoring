from setuptools import setup
import site
import sys

if __name__ == "__main__":
    # workaround https://github.com/pypa/pip/issues/7953
    site.ENABLE_USER_SITE = "--user" in sys.argv[1:]
    setup(
    )