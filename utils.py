"""
Module provides functions for creating version's comparable form
and Version class descriptor.
"""

import re
from collections import OrderedDict

VERSION_PATTERN = re.compile(r'(\d+\.){,2}\d+(-?(\d+|a|b|alpha|beta|rc)[.-]?)*(\+(\w+[.-]?)+)?')
NOT_IMPLEMENTED_INVALID_VERSIONS = ['0.0.0', '0.0', '0']


class VersionDescriptor:
    """
    Descriptor for Version class, checks if version number is valid
    and creates its comparable form.
    """
    def __init__(self, comparable_version=False):
        self.flag = comparable_version

    def __get__(self, instance: object, owner=None):
        return getattr(instance, self.name)

    def __set__(self, instance: object, version: str):
        if self.flag:
            raise AttributeError("Can't set version's comparable form.")
        if VersionDescriptor.is_valid(version):
            setattr(instance, self.name, version)
            setattr(instance, '_comparable_version', VersionDescriptor.create_comparable_version(version))

    def __set_name__(self, owner: object, name: str):
        self.name = f'_{name}'

    @staticmethod
    def is_valid(version: str) -> bool:
        """
        Checks if version number is valid and
        raises ValueError if it's not.
        More details on https://semver.org/
        """
        if re.fullmatch(VERSION_PATTERN, version) and version not in NOT_IMPLEMENTED_INVALID_VERSIONS:
            return True
        raise ValueError(
            """
            Incorrect version number. 
            Common pattern is X.Y.Z-'pre-release version'+'metadata'. 
            At least X expected.
            """
        )

    @staticmethod
    def create_comparable_version(version: str) -> list:
        """
        Converts string representation of version number
        to its comparable form.
        """
        replacements = OrderedDict(
            {'alpha': 'a', 'beta': 'b', 'a': '.a', 'b': '.b', '-': '.', '..': '.'}
        )
        comparable_version = version if '+' not in version else version[:version.find('+')]
        for key, value in replacements.items():
            comparable_version = comparable_version.replace(key, value)
        comparable_version = comparable_version.split('.')
        comparable_version = list(
            map(lambda x: int(x) if x.isdigit() else x.lower(), comparable_version)
        )
        return comparable_version
