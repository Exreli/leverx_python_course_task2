"""
Module provides Version class affording
semantic compare.
"""


import re
from collections import OrderedDict
from functools import total_ordering


class VersionChecker:
    """
    Descriptor for Version class, checks if version number is valid.
    More details on https://semver.org/
    """
    def __get__(self, instance: object, owner=None):
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: str):
        if re.fullmatch(r'(\d+\.){,2}\d+(-?(\d+|a|b|alpha|beta|rc)[.-]?)*(\+(\w+[.-]?)+)?', value)\
                and value not in ('0.0.0', '0.0', '0'):
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

    def comparable_version(self) -> list:
        """
        Converts string representation of version number
        to its comparable form.
        """
        replacements = OrderedDict(
            {'alpha': 'a', 'beta': 'b', 'a': '.a', 'b': '.b', '-': '.', r'\+.+': ''}
        )
        comparable_version = self.version
        for key, value in replacements.items():
            comparable_version = re.sub(key, value, comparable_version)
        comparable_version = re.split(r'\.+', comparable_version)
        while len(comparable_version) < 3:
            comparable_version.append('0')
        comparable_version = list(
            map(lambda x: int(x) if x.isdigit() else x.lower(), comparable_version)
        )
        return comparable_version

    @staticmethod
    def is_version(other: object):
        """
        Raises ValueError if given instance doesn't belong to Version class.
        """
        if not isinstance(other, Version):
            raise TypeError('Instance of Version class expected')

    def __eq__(self, other: 'Version') -> bool:
        """
        Check if current version is equal to other.
        """
        Version.is_version(other)
        version_1, version_2 = self.comparable_version(), other.comparable_version()
        return version_1 == version_2

    def __lt__(self, other: 'Version') -> bool:
        """
        Check if current version is less than other.
        """
        Version.is_version(other)
        version_1, version_2 = self.comparable_version(), other.comparable_version()
        for i, (x, y) in enumerate(zip(version_1, version_2)):
            try:
                if x != y:
                    return x < y
            except TypeError:
                if i <= 3:
                    return isinstance(x, str)
                return isinstance(x, int)
        if 3 in (len(version_1), len(version_2)):
            return len(version_1) > 3
        return len(version_1) < len(version_2)


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
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
