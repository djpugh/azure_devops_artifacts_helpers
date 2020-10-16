import glob
from pathlib import Path

from pkg_resources import resource_filename
from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.embed.pip_invoke import PipInvoke
from virtualenv.seed.embed.via_app_data.via_app_data import FromAppData
from virtualenv.seed.wheels import bundle, embed, Version, Wheel, get_wheel, pip_wheel_env_run


EXT_DIR = Path(resource_filename('azure_devops_artifacts_helpers.wheels', ''))


for py_ver, pkgs in embed.BUNDLE_SUPPORT.items():
    for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
        pkgs[pkg.name.split('-')[0]] = pkg.name


def get_embed_wheel(distribution, for_py_version):
    wheel = (embed.BUNDLE_SUPPORT.get(for_py_version, {}) or embed.BUNDLE_SUPPORT[MAX]).get(distribution)
    if wheel is not None:
        path = embed.BUNDLE_FOLDER / wheel
        if not path.exists():
            path = EXT_DIR/wheel
        wheel = Wheel.from_path(path)
    return wheel


bundle.get_embed_wheel = get_embed_wheel


class AzureDevopsArtifactsMixin(BaseEmbed):

    def __init__(self, options):
        for dist in self.distributions().keys():
            setattr(self, f'no_{dist}', getattr(options, f'no_{dist}'))
            setattr(self, f'{dist}_version', getattr(options, dist))
        super(AzureDevopsArtifactsMixin, self).__init__(options)
        self.extra_search_dir.append(EXT_DIR)

    @classmethod
    def distributions(cls):
        base = super().distributions()
        for pkg in EXT_DIR.glob('artifacts_keyring*.whl'):
            base[pkg.name.split('-')[0]] = Version.embed
        return base


class AzureDevopsArtifactsPipInvoke(AzureDevopsArtifactsMixin, PipInvoke):
    pass


class AzureDevopsArtifactsFromAppData(AzureDevopsArtifactsMixin, FromAppData):
    pass
