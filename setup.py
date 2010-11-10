from setuptools import setup, find_packages
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
import jqhelpers
setup(
    name="django-jqhelpers",
    version=jqhelpers.__version__,
    author="Owen Nelson",
    author_email="onelson@gmail.com",
    license="MIT",
    description="structured django template tags for jquery",
    keywords="jquery django",
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['setuptools'],
#    test_suite = 'nose.collector',
#    tests_require = ['nose'],
)
