# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .purchase import *

def register():
    Pool.register(
        PurchaseLine,
        module='purchase_delivery_date', type_='model')
