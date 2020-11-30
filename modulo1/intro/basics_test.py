
import unittest
import basics

class MyTest(unittest.TestCase):
  def test_factorial_five(self):
    self.assertEqual(basics.factorial(5), 120)
  def test_factorial_zero(self):
    self.assertEqual(basics.factorial(0),1)
  def test_factorial_one(self):
    self.assertEqual(basics.factorial(1),1)