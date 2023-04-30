def get_version():
    """Get version information or return default if unable to do so."""
    # Default
    version = '0+unknown'
    # Development installation only
    try:
        # Look here for setuptools scm to update the version - for development environments only
        from setuptools_scm import get_version
        try:
            version = get_version(root='../../', version_scheme='no-guess-dev', relative_to=__file__)
        except LookupError:
            pass
    except ImportError:
        pass
    # Development installation without setuptools_scm or installed package
    # try loading from file
    if version == '0+unknown':
        try:
            from azure_devops_artifacts_helpers._version import __version__  # noqa: F401
        except ImportError:
            pass
    # Development installation without setuptools_scm
    if version == '0+unknown':
        # Use the metadata
        import sys
        if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
            from importlib.metadata import version, PackageNotFoundError
        else:
            from importlib_metadata import version, PackageNotFoundError
        try:
            version = version("azure_devops_artifacts_helpers")
        except PackageNotFoundError:
            # package is not installed
            pass
    return version
