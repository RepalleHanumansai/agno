from odoo import models, fields


class VpnChurn(models.Model):
    _name = "vpn.churn"
    _description = "VPN Churn Dataset"
    _rec_name = "customer_id"

    customer_id = fields.Char(string="Customer ID", required=True)
    gender = fields.Selection([("Male", "Male"), ("Female", "Female")])
    marital_status = fields.Char(string="Marital Status")
    seniorcitizen = fields.Boolean(string="Senior Citizen")
    tenure = fields.Integer(string="Tenure")
    auto_renewal = fields.Boolean(string="Auto Renewal")
    subscription_type = fields.Char(string="Subscription Type")
    devices_connected = fields.Integer(string="Devices Connected")
    tickets_raised = fields.Integer(string="Tickets Raised")
    feedback_sentiment = fields.Char(string="Feedback Sentiment")
    payment_method = fields.Char(string="Payment Method")
    subscription_status = fields.Char(string="Subscription Status")
    country = fields.Char(string="Country")
    language = fields.Char(string="Language")
    failed_login_attempts = fields.Integer(string="Failed Login Attempts")
    login_frequency = fields.Integer(string="Login Frequency")
    monthly_usage_hours = fields.Float(string="Monthly Usage Hours")
    server_switch_frequency = fields.Integer(string="Server Switch Frequency")
    streaming_access = fields.Boolean(string="Streaming Access")
    average_speed_mbps = fields.Float(string="Average Speed (Mbps)")
    connection_success_rate = fields.Float(string="Connection Success Rate")
    plan_upgrade_attempts = fields.Integer(string="Plan Upgrade Attempts")
    last_login = fields.Datetime(string="Last Login")
    unresolved_tickets = fields.Integer(string="Unresolved Tickets")
    discount_used = fields.Boolean(string="Discount Used")
    churn = fields.Boolean(string="Churn")


class VpnChurnTest(models.Model):
    _name = "vpn.churn.test"
    _description = "VPN Churn Test Dataset"
    _rec_name = "customer_id"

    customer_id = fields.Char(string="Customer ID", required=True)
    gender = fields.Selection([("Male", "Male"), ("Female", "Female")])
    marital_status = fields.Char(string="Marital Status")
    seniorcitizen = fields.Boolean(string="Senior Citizen")
    tenure = fields.Integer(string="Tenure")
    auto_renewal = fields.Boolean(string="Auto Renewal")
    subscription_type = fields.Char(string="Subscription Type")
    devices_connected = fields.Integer(string="Devices Connected")
    tickets_raised = fields.Integer(string="Tickets Raised")
    feedback_sentiment = fields.Char(string="Feedback Sentiment")
    payment_method = fields.Char(string="Payment Method")
    subscription_status = fields.Char(string="Subscription Status")
    country = fields.Char(string="Country")
    language = fields.Char(string="Language")
    failed_login_attempts = fields.Integer(string="Failed Login Attempts")
    login_frequency = fields.Integer(string="Login Frequency")
    monthly_usage_hours = fields.Float(string="Monthly Usage Hours")
    server_switch_frequency = fields.Integer(string="Server Switch Frequency")
    streaming_access = fields.Boolean(string="Streaming Access")
    average_speed_mbps = fields.Float(string="Average Speed (Mbps)")
    connection_success_rate = fields.Float(string="Connection Success Rate")
    plan_upgrade_attempts = fields.Integer(string="Plan Upgrade Attempts")
    last_login = fields.Datetime(string="Last Login")
    unresolved_tickets = fields.Integer(string="Unresolved Tickets")
    discount_used = fields.Boolean(string="Discount Used")
    churn = fields.Boolean(string="Churn")
