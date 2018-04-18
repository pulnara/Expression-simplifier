from unittest import TestCase
from app import *

class TestProcess(TestCase):
    def test_process(self):
        self.assertEqual(process("~a&(a|b)|(b|a&a)&(a|~b)"), process("a|b"))
        self.assertEqual(process("a|0"), "a")
        self.assertEqual(process("a&a"), "a")
        self.assertEqual(process("~(a&b)&(~a|b)&(~b|b)"), "~a")
        self.assertEqual(process(" ~(a & 1) & (~a | 1) & (~1 | 1)"), "~a")
        self.assertEqual(process(" (a | c) & (a & d | a & ~d) | a & c | c"), process("a|c"))
        self.assertEqual(process("a&(a|~a)|b"), process("a|b"))
        self.assertEqual(process("~(x & y) & (~x | y) & (~x | x)"), "~x")
        self.assertEqual(process("~(a&b)"), "~a|~b")
        self.assertEqual(process("~(a|b)"), "~a&~b")
        self.assertEqual(process("x|x&y"), "x")
        self.assertEqual(process("(a | b) & (a | c)"), "a|b&c")
        self.assertEqual(process("a|~a&b"), process("a|b"))
        self.assertEqual(process("(a & b) | (a & ~b) & ~(~a & ~c)"), "a")
        self.assertEqual(process("(x & y) | (x & y & z) | (x & y & ~z) | (~x & y & z)"), "y&z|x&y") #y(x|z)
        # (a & b) | ~(a & c) | (a & ~b & c) & (a & b | c) - always true












