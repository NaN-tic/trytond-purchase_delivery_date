# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval, If
from trytond.transaction import Transaction

__all__ = ['PurchaseLine']


class PurchaseLine:
    __name__ = 'purchase.line'
    __metaclass__ = PoolMeta

    requested_delivery_date = fields.Date(
        'Requested Delivery Date',
        states={
            'invisible': (
                (Eval('type') != 'line') |
                (If(Bool(Eval('quantity')), Eval('quantity', 0), 0) <= 0)
            ),
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
        move_delivery_dates = (
            not table.column_exist('requested_delivery_date') and
            table.column_exist('delivery_date')
        )

        # Because of the change of the field's name manual_delivery_date to
        # requested_delivery_date
        if (table.column_exist('manual_delivery_date') and
                not table.column_exist('requested_delivery_date')):
            table.column_rename('manual_delivery_date',
                                'requested_delivery_date')

        super(PurchaseLine, cls).__register__(module_name)

        if move_delivery_dates:
            cursor.execute(*sql_table.update(
                columns=[sql_table.requested_delivery_date],
                values=[sql_table.delivery_date]))
            table.drop_column('delivery_date')

    @fields.depends('requested_delivery_date', methods=['delivery_date'])
    def on_change_with_requested_delivery_date(self):
        if self.requested_delivery_date:
            return self.requested_delivery_date
        return super(PurchaseLine,
            self).on_change_with_delivery_date(name='delivery_date')

    @fields.depends('requested_delivery_date')
    def on_change_with_delivery_date(self, name=None):
        return self.requested_delivery_date or super(PurchaseLine,
            self).on_change_with_delivery_date()
