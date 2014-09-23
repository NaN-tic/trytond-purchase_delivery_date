# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_depends


class PurchaseDeliveryDateTestCase(unittest.TestCase):
    'Test purchase_delivery_date module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('purchase_delivery_date')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseDeliveryDateTestCase))
    return suite
