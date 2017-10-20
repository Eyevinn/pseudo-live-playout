from os.path import dirname, abspath, join
from setuptools import setup

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
	name = "User",
	version = "0.0.1",
	author = "Eyevinn Technology",
	author_email = "info@eyevinn.se",
	description = "User",
	license = "MIT",
	install_requires = install_reqs,
	packages = ['User']
)