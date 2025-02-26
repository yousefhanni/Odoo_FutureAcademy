from odoo import models, fields, api

class ItiSkill(models.Model):
    _name="iti.skill"   
    
    name= fields.Char()