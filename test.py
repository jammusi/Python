import binascii
from itertools import chain, zip_longest
from typing import Iterable, Sequence

def compute_order_book_checksum(
    bids: Iterable[Sequence[float]], asks: Iterable[Sequence[float]]
) -> int:
    """
    Compute the checksum for the order book.

    Bids and asks are iterables of 2-item lists <price, quantity>.
    The algorithm to compute the checksum of the order book is described here:
    https://docs.ftx.com/#orderbooks

    :param bids: the list of bids
    :param asks: the list of asks
    :return: the CRC32 checksum of the order book
    """

    order_book_hash_iterator = zip_longest(bids, asks, fillvalue=tuple())
    check_string = ":".join(
        (
            str(token)
            for ask_level, bid_level in order_book_hash_iterator
            for token in chain(ask_level, bid_level)
        )
    )

    return binascii.crc32(check_string.encode("ascii"))