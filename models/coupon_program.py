from odoo import api, fields, models, _
from datetime import datetime, timedelta



class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    is_meal_program = fields.Boolean(string='Is Meal Program?', default=False)

    def cron_reset_discount_period(self):
        self.reset_discount_period()
    def reset_discount_period(self):
        current_date = fields.Datetime.now()
        start_of_today = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_tomorrow = start_of_today + timedelta(days=1)

        programs = self.env['coupon.program']
        programs = self.env['coupon.program'].search([('is_meal_program', '=', True), ('active', '=', True)])
        for program in programs:
            program.write(
                {
                    'rule_date_from': fields.Datetime.to_string(start_of_today),
                    'rule_date_to': fields.Datetime.to_string(start_of_tomorrow),
                    'maximum_use_number': program.pos_order_count+program.order_count+1,
                }
            )
        
