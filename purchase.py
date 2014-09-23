#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool, If

__all__ = ['PurchaseLine']
__metaclass__ = PoolMeta


class PurchaseLine:
    __name__ = 'purchase.line'
    delivery_date = fields.Date('Delivery Date',
            states={
                'invisible': ((Eval('type') != 'line')
                    | (If(Bool(Eval('quantity')), Eval('quantity', 0), 0)
                        <= 0)),
                },
            depends=['type', 'quantity'])

    @fields.depends('product', 'quantity', 'delivery_date',
        '_parent_purchase.purchase_date', '_parent_purchase.party')
    def on_change_with_delivery_date(self):
        if self.delivery_date:
            return self.delivery_date
        if not self.product or not self.quantity:
            return
        return super(PurchaseLine, self).on_change_with_delivery_date()
