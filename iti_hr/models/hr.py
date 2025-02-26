from odoo import models, fields,api

class HrEmployeeInherit(models.Model):   
    _inherit = "hr.employee"   
    
    military_certificate = fields.Binary("Military Certificate")
    
    
    #may change Functions(create , write, search ,link, .....) 
  
