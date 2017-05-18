# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PurchaseDeliveryDateTestCase(ModuleTestCase):
    'Test purchase_delivery_date module'
    module = 'purchase_delivery_date'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PurchaseDeliveryDateTestCase))
    return suite
