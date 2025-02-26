from odoo import models, fields, api

class ItiTrack(models.Model):
    _name="iti.track"   
    #_rec_name="capacity" if want to change default and show capacity of tracks not names 
     
    name=fields.Char()
    is_open=fields.Boolean()    
    capacity=fields.Integer()   
    student_ids=fields.One2many("iti.student","track_id") #Show all students linked to a track 
    #When you access a specific track (ID=5) in Odoo, the ORM automatically fetches all related students by querying the iti.student table.
    # It looks for records where track_id = 5 (the foreign key pointing to the track). The ORM generates and executes the following SQL query in the background:
    #SELECT * FROM iti_student WHERE track_id = 5; =>This fetches all students associated with the specified track, using the One2many relationship.
    ##field(student_ids) One2many must To make it is there field Many2one(track_id) to relies on it 
   
   





