# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval, If
from trytond.transaction import Transaction

__all__ = ['PurchaseLine']
__metaclass__ = PoolMeta


class PurchaseLine:
    __name__ = 'purchase.line'
    manual_delivery_date = fields.Date('Delivery Date',
            states={
                'invisible': ((Eval('type') != 'line')
                    | (If(Bool(Eval('quantity')), Eval('quantity', 0), 0)
                        <= 0)),
                },
            depends=['type', 'quantity'])

    @classmethod
    def __setup__(cls):
        super(PurchaseLine, cls).__setup__()
        cls.delivery_date.states['invisible'] = True

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().connection.cursor()
        sql_table = cls.__table__()

        # Migration from 3.2
        table = TableHandler(cls, module_name)
        move_delivery_dates = (not table.column_exist('manual_delivery_date')
            and table.column_exist('delivery_date'))

        super(PurchaseLine, cls).__register__(module_name)

        if move_delivery_dates:
            cursor.execute(*sql_table.update(
                    columns=[sql_table.manual_delivery_date],
                    values=[sql_table.delivery_date]))
            table.drop_column('delivery_date')

    @fields.depends('manual_delivery_date', methods=['delivery_date'])
    def on_change_with_manual_delivery_date(self):
        if self.manual_delivery_date:
            return self.manual_delivery_date
        return super(PurchaseLine,
            self).on_change_with_delivery_date(name='delivery_date')

    @fields.depends('manual_delivery_date')
    def on_change_with_delivery_date(self, name=None):
        return self.manual_delivery_date

