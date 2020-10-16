"""Extensions for virtualenv Seeders to pre-install artifacts-keyring and deps."""
from pathlib import Path

from pkg_resources import resource_filename

from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.embed.pip_invoke import PipInvoke
from virtualenv.seed.wheels import Version, Wheel, bundle, embed


EXT_DIR = Path(resource_filename('azure_devops_artifacts_helpers.wheels', ''))


for py_ver, pkgs in embed.BUNDLE_SUPPORT.items():
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        pkgs[pkg.name.split('-')[0]] = pkg.name


def get_embed_wheel(distribution, for_py_version):
    """Get the embed wheel from the normal virtualenv embed dir or this one."""
    wheel = (embed.BUNDLE_SUPPORT.get(for_py_version, {}) or embed.BUNDLE_SUPPORT[embed.MAX]).get(distribution)
    if wheel is not None:
        path = embed.BUNDLE_FOLDER / wheel
        if not path.exists():
            path = EXT_DIR/wheel
        wheel = Wheel.from_path(path)
    return wheel


bundle.get_embed_wheel = get_embed_wheel


class AzureDevopsArtifactsMixin(BaseEmbed):
    """Mixin to add/configure the devops artifacts dependencies."""
    def __init__(self, options):
        """Add the extra attributes for the extensions."""
        for dist in self.distributions().keys():
            setattr(self, f'no_{dist}', getattr(options, f'no_{dist}'))
            setattr(self, f'{dist}_version', getattr(options, dist))
        super(AzureDevopsArtifactsMixin, self).__init__(options)
        self.extra_search_dir.append(EXT_DIR)

    @classmethod
    def distributions(cls):
        """Return the dictionary of distributions."""
        base = super().distributions()
        for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
            base[pkg.name.split('-')[0]] = Version.bundle
        return base


class AzureDevopsArtifactsPipInvoke(AzureDevopsArtifactsMixin, PipInvoke):
    """Mixed in Azure Devops artifacts-keyring into seed packages for pip seeder."""
