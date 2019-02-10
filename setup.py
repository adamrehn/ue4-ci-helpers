from os.path import abspath, dirname, join
from setuptools import setup

# Read the README markdown data from README.md
with open(abspath(join(dirname(__file__), 'README.md')), 'rb') as readmeFile:
	__readme__ = readmeFile.read().decode('utf-8')

setup(
	name='ue4-ci-helpers',
	version='0.0.1',
	description='Unreal Engine 4 Continuous Integration helper functionality',
	long_description=__readme__,
	long_description_content_type='text/markdown',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Build Tools',
		'Environment :: Console'
	],
	keywords='epic unreal engine ci',
	url='http://github.com/adamrehn/ue4-ci-helpers',
	author='Adam Rehn',
	author_email='adam@adamrehn.com',
	license='MIT',
	packages=['ue4helpers'],
	zip_safe=True,
	python_requires = '>=3.5',
	install_requires = [
		'boto3',
		'conan>=1.7.4',
		'conan-ue4cli>=0.0.10',
		'setuptools>=38.6.0',
		'twine>=1.11.0',
		'ue4cli>=0.0.24',
		'wheel>=0.31.0'
	]
)
