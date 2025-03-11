#!/usr/bin/env python3
"""
Test runner for poker game.
Run this script to execute all unit tests.
"""
import unittest

if __name__ == "__main__":
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('tests')
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)
    print("All tests completed.") 