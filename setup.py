import setuptools

with open('README.md', 'r') as f:
	long_description = f.read()

setuptools.setup(
	name='EPAM graduation work',
	version='0.0.1',
	author='Frolkin Volodimir',
	author_email='frolkin2801@gmail.com',
	long_description=long_description,
	description='Package with rest api and web application',
	url='https://github.com/frolkin28/epam_gw',
	packges=setuptools.find_packages(),
	python_requires='>=3.6'
)
