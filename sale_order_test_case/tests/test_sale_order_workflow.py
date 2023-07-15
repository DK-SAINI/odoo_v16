import logging

from odoo.tests.common import TransactionCase

# Create a logger instance
logger = logging.getLogger(__name__)


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "testpartner@example.com",
            }
        )

    def test_create_sale_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "date_order": "2023-07-15",
            }
        )
        self.assertEqual(sale_order.state, "draft")
        print("+++++++++++++++++++++Sale order created+++++++++++++++++++++")

    def test_confirm_sale_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "date_order": "2023-07-15",
            }
        )
        sale_order.action_confirm()
        self.assertEqual(sale_order.state, "sale")
        print("+++++++++++++++++++++Sale order confirm+++++++++++++++++++++")

    def test_cancel_sale_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "date_order": "2023-07-15",
            }
        )
        sale_order.action_cancel()
        self.assertEqual(sale_order.state, "cancel")
        print("+++++++++++++++++++++Sale order created+++++++++++++++++++++")
