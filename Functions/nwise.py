from typing import Sequence, Generator, Tuple, Optional, Any


def nwise(
    sequence: Sequence[Any], n: int = 3, exhaust: Optional[bool] = None
) -> Generator[Tuple[Any, ...], None, None]:
    """
    yield tuple of n values from a sequence
    see also: `itertools.batched()`

    Paramaters:
        sequence (Sequence[Any]):
            sequence from which to take elements in n-wise groups
        n (int):
            size of group to take
        exhaust (bool, optional):
            When True: pads out the return values with None for the last set.
            When False: truncates leftover data that can't fill n values.
            When None: raises exception if data does not fit shape of n.
            Defaults to None.
    Yields:
        Tuple[Any, ...]
    """

    assert int(n) > 0, "n must be an integer value greater than z"

    def n_minus_one_times() -> Generator[Any, None, None]:
        """yield from idata n-1 times times"""
        for _ in range(int(n) - 1):
            try:
                yield (next(idata))
            except StopIteration as e:
                # catch StopIteration here to pad with None
                if exhaust is True:
                    yield None
                    continue
                # or pass up to next level
                raise e

    idata = iter(sequence)
    for val in idata:
        try:
            yield (val, *n_minus_one_times())
        except (StopIteration, RuntimeError):  # https://peps.python.org/pep-0479/
            # catch here to truncate
            if exhaust is False:
                return
            # exhaust is None so raise ValueError
            raise ValueError(f"The values do not fit shape {n}")


def example() -> None:
    print(">>> list(nwise(range(6), 3))")
    print(list(nwise(range(6), 3)))
    print(">>> list(nwise(range(6), 2))")
    print(list(nwise(range(6), 2)))
    print(">>> list(nwise(range(5), 3, True))")
    print(list(nwise(range(5), 3, True)))
    print(">>> list(nwise(range(5), 3, False))")
    print(list(nwise(range(5), 3, False)))
    print(">>> list(nwise(range(5), 3, None))")
    print("ValueError")


if __name__ == "__main__":
    example()
