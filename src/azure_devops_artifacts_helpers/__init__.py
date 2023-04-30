"""Package containing virtualenv helpers for installing artifacts-keyring."""
try:
    from azure_devops_artifacts_helpers._version import __version__  # noqa: F401
except ImportError:
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
