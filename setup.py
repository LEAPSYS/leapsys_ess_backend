from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="leapsys_ess_backend",
	version="0.0.1",
	description="Employee Self Service and Service App for LEAPSYS",
	author="LEAPSYS",
	author_email="info@leapsys.net",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
