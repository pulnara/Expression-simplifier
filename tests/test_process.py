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
        self.assertEqual(process("(a & b) | ~(a & c) | (a & ~b & c) & (a & b | c) "), "Always true")
        self.assertEqual(process("0|1"), "Always true")
        self.assertEqual(process("0&1"), "Always false")
        self.assertEqual(process("0>abcdefg"), "Always true")
        self.assertEqual(process("c | ~(b & c)"), "Always true")
        self.assertEqual(process("(a&b&~c&~d)|(~b&c&~d)|(a&~c&d)|(a&~b&~c)|(b&c&~d)"), "c&~d|a&~c")
        self.assertEqual(process("p|q>r"), "~p&~q|r")














