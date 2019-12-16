import setuptools

with open('README.md', 'r') as f:
	long_description = f.read()

setuptools.setup(
	name='EPAM graduation work',
	version='0.0.1',
	author='Frolkin Volodimir',
	author_email='frolkin2801@gmail.com',
	description='Package with rest crud service and web application',
	packges=setuptools.find_packages(),
	python_requires='>=3.6'
)
