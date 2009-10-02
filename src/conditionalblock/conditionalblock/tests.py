import unittest
import testsuites.basic_tests

def suite():
    alltests = unittest.TestSuite()
    alltests.addTest( unittest.TestLoader().loadTestsFromModule( testsuites.basic_tests ) )
    return alltests
