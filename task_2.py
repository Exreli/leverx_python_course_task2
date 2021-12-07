"""
Module provides Version class affording
semantic compare.
"""


import re
from collections import OrderedDict
from functools import total_ordering


class VersionChecker:
    def __get__(self, instance, owner=None):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if re.fullmatch(r'(\d+\.){,2}\d+(-?(\d+|a|b|alpha|beta|rc|sr)[.-]?)*(\+(\w+[.-]?)+)?', value) and \
                value != '0.0.0':
            setattr(instance, self.name, value)
        else:
            raise ValueError("""
                        Incorrect version number. 
                        Common pattern is X.Y.Z-'pre-release version'+'metadata'. 
                        At least X expected.
                        """)

    def __set_name__(self, owner, name):
        self.name = f'_{name}'


@total_ordering
class Version:
    """
    Class for working with Version data (its semantic compare).
    """
    version = VersionChecker()

    def __init__(self, version: str):
        """
        Creates a new instance of Version class.
        """
        self.version = version
        self.comparable_version = Version.convert_version(version)

    @staticmethod
    def convert_version(version: str) -> list:
        """
        Converts string representation of version number
        to its comparable form.
        """
        replacements = OrderedDict(
            {'alpha': 'a', 'beta': 'b', 'a': '.a', 'b': '.b', r'\-': '.', r'\+.+': ''}
        )
        for key, value in replacements.items():
            version = re.sub(key, value, version)
        version = re.split(r'\.+', version)
        while len(version) < 3:
            version.append('0')
        version = list(map(lambda x: int(x) if x.isdigit() else x.lower(), version))
        return version

    @staticmethod
    def is_version(other):
        """
        Raises ValueError if given instance doesn't belong to Version class.
        """
        if not isinstance(other, Version):
            raise TypeError('Instance of Version class expected')

    def __eq__(self, other) -> bool:
        """
        Check if current version is equal to other.
        :type other: Version
        """
        Version.is_version(other)
        return self.comparable_version == other.comparable_version

    def __lt__(self, other) -> bool:
        """
        Check if current version is less than other.
        :type other: Version
        """
        Version.is_version(other)
        for i, (x, y) in enumerate(zip(self.comparable_version, other.comparable_version)):
            try:
                if x == y:
                    continue
                return x < y
            except TypeError:
                if i <= 3:
                    return isinstance(x, str)
                return isinstance(x, int)
        if 3 in (len(self.comparable_version), len(other.comparable_version)):
            return len(self.comparable_version) > 3
        return len(self.comparable_version) < len(other.comparable_version)


def main():
    """
    Tests of Version's semantic compare.
    """
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0-alpha+001", "1.0.0-beta+exp.sha.5114f85"),
        ("1.0.0-alpha+001", "1.0.0+20130313144700"),
        ("1.0.0-beta+exp.sha.5114f85", "1.0.0+20130313144700"),
        ("1.0.0-alpha", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.2"),
        ("1.0.0-beta.2", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1"),
        ("1.10", "1.10.1"),
        ("6.42b", "6.42"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
