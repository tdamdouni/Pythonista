# word-domains: A fun tool for finding domain names that spell words.

import collections
import os

import requests


GH_BASE = "https://raw.githubusercontent.com/"
TLD_URL = os.path.join(
    GH_BASE,
    "publicsuffix/list/master/public_suffix_list.dat"
)


def get_tlds():
    """Get a list of registerable TLDs."""

    print("Downloading TLD list...")

    return [
        tld.lower() for tld in
        requests.get(TLD_URL).text.splitlines()
        if not tld.startswith("//") and tld
    ]


def get_words():
    """Get a list of english words from /usr/share/dict/words (UNIX only)."""

    with open("/usr/share/dict/words") as f:
        return f.read().split("\n")


class DomainFinder(collections.Mapping):
    _tlds = get_tlds()
    _words = get_words()

    def __getitem__(self, ext):
        if ext not in self._tlds:
            raise KeyError(ext)
        else:
            simple_ext = ext.replace(".", "")

            return [w[:-len(simple_ext)] + "." + ext for w in
                    self._words
                    if w.endswith(simple_ext) and w != simple_ext]

    def __iter__(self):
        return iter(self._tlds)

    def __len__(self):
        return len(self._tlds)

    def __repr__(self):
        """Not for the faint of heart."""
        return repr(dict(self))

    def keys(self):
        return self._tlds

domains = DomainFinder()
