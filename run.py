"""Finds large cap sets."""
import itertools
import numpy as np


def evaluate(n: int) -> int:
  """Returns the size of an `n`-dimensional cap set."""
  capset = []
  length = len(capset)
  with open('result', 'w') as f:
    f.write(str(length))


def priority(el: tuple[int, ...], n: int) -> float:
  """Returns the priority with which we want to add `element` to the cap set."""

