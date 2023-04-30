"""Package containing virtualenv helpers for installing artifacts-keyring."""
__version__ = "0.0.0"  # Default blank Version
try:
    # Look here for setuptools scm to update the version - for development environments only
    from setuptools_scm import get_version
    try:
        __version__ = get_version(root='../../', version_scheme='no-guess-dev', relative_to=__file__)
    except LookupError:
        pass
except ImportError:
    pass
if __version__ == '0.0.0':
    # Otherwise we try loading from file or metadata
    try:
        from azure_devops_artifacts_helpers._version import __version__  # noqa: F401
    except ImportError:
        pass
if __version__ == '0.0.0':
    # Use the metadata
    import sys
    if sys.version_info.major >= 3 and sys.version_info.minor >=8:
        from importlib.metadata import version, PackageNotFoundError
    else:
        from importlib_metadata import version, PackageNotFoundError
    try:
        __version__ = version("azure_devops_artifacts_helpers")
    except PackageNotFoundError:
        # package is not installed
        pass
