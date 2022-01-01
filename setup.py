from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in runo_crm/__init__.py
from runo_crm import __version__ as version

setup(
	name="runo_crm",
	version=version,
	description="Runo CRM Integration",
	author="ERPNext",
	author_email="venku31@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
