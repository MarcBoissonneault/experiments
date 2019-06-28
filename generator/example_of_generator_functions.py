# example_of_generator_functions.py
# Marc Boissonneault, 2019-05-31
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations


def echo(value=None):
    print("Execution starts when 'next()' is called for the first time.")
    try:
        while True:
            try:
                value = (yield value)
            except Exception as e:
                value = e
    finally:
        print("Don't forget to clean up when 'close()' is called.")


