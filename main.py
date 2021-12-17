"""
Module provides Version class affording
semantic compare.
"""


from functools import total_ordering
from itertools import zip_longest
from utils import VersionDescriptor


@total_ordering
class Version:
    """
    Class for working with Version data (its semantic compare).
    """
    version = VersionDescriptor()
    comparable_version = VersionDescriptor(comparable_version=True)

    def __init__(self, version: str):
        """
        Creates a new instance of Version class.
        """
        self.version = version

    @staticmethod
    def get_comparable_version(obj: any) -> list:
        """
        Returns version's comparable form.
        Raises ValueError if non-comparable object given.
        """
        if isinstance(obj, Version):
            return obj.comparable_version
        if isinstance(obj, str) and VersionDescriptor.is_valid(obj):
            return VersionDescriptor.create_comparable_version(obj)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """
        Checks if current version is equal to other.
        """
        version_to_compare = Version.get_comparable_version(other)
        for x, y in zip_longest(self.comparable_version, version_to_compare, fillvalue=0):
            try:
                if x != y:
                    return False
            except TypeError:
                return False
        return True

    def __lt__(self, other: object) -> bool:
        """
        Checks if current version is less than other.
        """
        version_to_compare = Version.get_comparable_version(other)
        for x, y in zip_longest(self.comparable_version, version_to_compare, fillvalue=0):
            try:
                if x != y:
                    return x < y
            except TypeError:
                return isinstance(x, str)


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
