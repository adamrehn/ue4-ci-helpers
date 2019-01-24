UE4 Continuous Integration helper functionality
===============================================

The ue4-ci-helpers Python package builds on the [ue4cli](https://github.com/adamrehn/ue4cli) and [conan-ue4cli](https://github.com/adamrehn/conan-ue4cli) packages to provide infrastructure for Continuous Integration (CI) use cases for Unreal projects and plugins. It aims to simplify the process of writing platform-agnostic build scripts that can then be run as part of a CI pipeline. Although the package works best inside the [ue4-full](https://adamrehn.com/docs/ue4-docker/building-images/available-container-images#ue4-full) Docker image produced by the [ue4-docker](https://github.com/adamrehn/ue4-docker) project, the core functionality will work on any system where ue4cli has been correctly configured.

A simple build script for packaging a nightly build of an Unreal project might look like so:

```python
#!/usr/bin/env python3
from ue4helpers import ProjectPackager, VersionHelpers
from os.path import abspath, dirname

# Create our project packager
packager = ProjectPackager(
	
	# The root directory for the project
	# (This example assumes this script is in a subdirectory)
	root = dirname(dirname(abspath(__file__))),
	
	# Use the date of the most recent git commit as our version string
	version = VersionHelpers.from_git_commit(),
	
	# The filename template for our generated .zip file
	archive = '{name}-Nightly-{version}-{platform}',
	
	# Don't strip debug symbols from the packaged build
	strip_debug = False,
	
	# Don't strip manifest files from the packaged build
	strip_manifests = False
)

# Clean any previous build artifacts
packager.clean()

# Package the project
packager.package()

# Compress the packaged distribution
# (The CI system can then tag the generated .zip file as a build artifact)
packager.archive()
```

Check out the docstring for the constructor of the [PackagerBase](https://github.com/adamrehn/ue4-ci-helpers/blob/master/ue4helpers/PackagerBase.py) class to see the full list of supported parameters and their uses.


## Legal

Copyright &copy; 2019, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/ue4-ci-helpers/blob/master/LICENSE) for details.

Development of this package was funded by [Deepdrive, Inc](https://deepdrive.io/).
