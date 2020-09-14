import unittest

from unittest import TestCase
from unittest.mock import patch

from io import StringIO

import sys
from xyes import xyes


class TestB(unittest.TestCase):
	def test_limit_no_arg(self):
		# Append limit arg
		sys.argv = [sys.argv[0], '-limit']

		# Mock stdout
		with patch('sys.stdout', new = StringIO()) as mocked_stdout:
			# Run test
			xyes()
			# Make assertions
			self.assertEqual(mocked_stdout.getvalue(), "".join(['hello world\n'] * 20))

	def test_limit_with_arg(self):
		# Append limit arg
		sys.argv = [sys.argv[0], '-limit', 'cat', 'apple']

		# Mock stdout
		with patch('sys.stdout', new = StringIO()) as mocked_stdout:
			# Run test
			xyes()
			# Make assertions
			self.assertEqual(mocked_stdout.getvalue(), "".join(['cat apple\n'] * 20))

	def test_nolimit_with_arg(self):
		sys.argv = [sys.argv[0], 'cat', 'apple']

		# Mock stdout
		with patch('sys.stdout', new = StringIO()) as mocked_stdout:
			# Run test
			xyes(120)
			# Make assertions
			self.assertEqual(mocked_stdout.getvalue(), "".join(['cat apple\n'] * 120))

	def test_nolimit_no_arg(self):
		sys.argv = [sys.argv[0]]

		# Mock stdout
		with patch('sys.stdout', new = StringIO()) as mocked_stdout:
			# Run test
			xyes(99)
			# Make assertions
			self.assertEqual(mocked_stdout.getvalue(), "".join(['hello world\n'] * 99))

if __name__ == '__main__':
	unittest.main()