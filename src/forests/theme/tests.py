import unittest

from Testing import ZopeTestCase as ztc

import forests.theme
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(forests.theme)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        # doctestunit.DocFileSuite(
        #    'README.txt', package='forests.theme',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # doctestunit.DocTestSuite(
        #    module='forests.theme.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        # ztc.ZopeDocFileSuite(
        #    'README.txt', package='forests.theme',
        #    test_class=TestCase),

        # ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='forests.theme',
        #    test_class=TestCase),

    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
