from .spmpackage import SPMPackage


class Project(object):

    def __init__(self, package: SPMPackage):
        self.spm_package = package
