from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError
class ItiStudent(models.Model):
    _name="iti.student"   
   
    @api.depends("salary")
    def calc_salary(self):
        for student in self:
            student.tax_salary =student.salary*0.20
            # student.net_salary =student.salary-student.tax_salary
        
    name=fields.Char(required=True)
    email=fields.Char()
    birth_date=fields.Date()    
    salary=fields.Float()
    #field computed => calc at run time => Cal fuction named calc_tax it calc this taxes  
    tax_salary=fields.Float(compute="calc_salary", store=True)
    # net_salary=fields.Float(compute="calc_salary")
    address=fields.Text()
    gender = fields.Selection(
        [('m', "Male"), ('f', "Female")],
        string="Gender" 
    )  
    @api.onchange('gender') #lisen on change
    def _onchange_gender(self):
        if self.gender == 'm':
            self.salary = 15000 
        else:
            self.salary=5000
            
    accepted=fields.Boolean()
    level=fields.Integer()
    image = fields.Binary(string="Image")
    cv=fields.Html()
    login_time = fields.Datetime(string="Login Time", default=fields.Datetime.now)  # Automatically set to current datetime when a record is created
    gpa = fields.Float(string="GPA")    
    track_id=fields .Many2one("iti.track") #many to one field
    track_capacity=fields.Integer(related="track_id.capacity") #the related field allows you to access values from related models (like a field in a referenced model) without needing to manually write the logic to fetch the data.
    
    skills_ids=fields.Many2many("iti.skill") #Default Relation name of skill will appear only 
    
   # Create a One2many field to link students and courses with grades
    student_course_grades_ids = fields.One2many("iti.student.course.grades", "student_id")

    # At many2many field =>
    # 1. In a Many2many relationship, you define the field in one of the models (in this case, 'iti.student').
    # 2. The 'Many2many' field specifies the related model ('iti.skill') to establish the connection.
    # 3. Odoo will automatically create an intermediate table to manage this relationship.
    #    This table will contain two foreign keys:
    #    - One for the 'iti.student' model (student ID).
    #    - One for the 'iti.skill' model (skill ID).
    # 4. The intermediate table is handled by Odoo automatically, and you don't need to define it explicitly in the code.
    #=>if you want to adding custom data or attributes on relation => you need to create manual table to put it 
    #this Fields and also put two keys 
    
    state=fields.Selection([
    ('applied', 'Applied'),
    ('first', 'First Interview'),
    ('second', 'Second Interview'),
    ('passed', 'Passed'),
    ('rejected', 'Rejected'),
     ],default='applied')
    
    #we want to change behaviour of create which once that you create name will get email to this name
    #when will create search with name and get email, create=>call func named create   
     
    def change_state(self):
        if self.state=='applied':
          self.state='first'
        elif self.state=='first':
          self.state='second'  
        elif self.state in ['passed','rejected']:
         self.state='applied'  
    
    def set_passed(self):
        self.state = 'passed'
        
    def set_rejected(self):
        self.state = 'rejected'
       
     # Define SQL constraints
    _sql_constraints = [
        # Enforce uniqueness on the 'name' field
        ('unique_student_name', 'unique(name)', 'The name must be unique for each student.'),
        ('unique_email_name', 'unique(email)', 'The email must be unique for each student.')
    ]   
       
     #Api Constrain: decorator in Odoo is used to enforce a validation constraint at the business logic level
    @api.constrains("salary") 
    def _check_Salary(self):
        for record in self:
            if record.salary>10000:
                raise UserError("Salary should not be greater than 10000")
            
            
    @api.constrains("track_id")
    def check_track_id(self):
        """
        Ensures that the number of students in a track does not exceed the track's capacity.
        """
        for record in self:
            track_count = len(record.track_id.student_ids)
            track_capacity = record.track_id.capacity
            if track_count > track_capacity:
                raise UserError("Track is full")        
            
            
            

       
        
    #Create    
    @api.model
    def create(self, vals): # override on create method to change of implementation=>Generate the email based on the name 
      # Split the name into parts (assumes the name is a string with first and last name)
       name_split = vals['name'].split()  # E.g., ["ahmed", "ali"] 
        # Generate the email based on the name
       if len(name_split) >= 2:
          vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        #=>Search   
        # Check if this email already exists for any previous student
       search_students = self.search([('email', '=', vals['email'])])  
    #Use env to move to another table 
    #    track=self.env['iti.track'].browse(vals['track_id'])
    #    if track.is_open is False:
    #        raise UserError("Selected Track is false")    
       if search_students:
           raise UserError("This email is already registered for another student.")
        # Create a new student record
       new_student = super().create(vals)
       return new_student
    
    #Update
    def write(self, vals): #self tells you which records are being updated | vals tells you what fields and values to update on those records.
        # Call the super write method to update the record(s)
        result = super(ItiStudent, self).write(vals)
        
        # The for loop in the write method is used because the write method can potentially update multiple records at once in Odoo.
        # Update email if the name is being updated
        for record in self:
            if 'name' in vals and record.name: #'name' in vals: The name field is being updated (included in the vals dictionary).| record.name: The record currently being processed already has a value for its name field.
                name_split = record.name.split()  # Split name into parts
                if len(name_split) >= 2:  # Ensure the name has at least 2 parts
                    record.email = f"{name_split[0][0]}{name_split[1]}@gmail.com" 
        
        return result  # Ensure this return is properly indented inside the method
   
   #Delete
    def unlink(self): #self :self: Represents the recordset (the records to be deleted).
    # Check each record's state
     for record in self:
        if record.state in ['passed', 'rejected']:
            raise UserError("You can't delete passed/rejected students")

    # If no restricted records were found, proceed with the deletion
     return super().unlink()

               
           
        
    
class ItiCourse(models.Model):
    _name = "iti.course"
    # _description = "Course Model"   
    name = fields.Char(string="Course Name")
    
class StudentCourseGrades(models.Model):
    _name = "iti.student.course.grades"
    # _description = "Student Course Grades"

    student_id = fields.Many2one("iti.student", string="Student", required=True)
    course_id = fields.Many2one("iti.course", string="Course", required=True)
    
    # Grade as a Selection field
    grade = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ], string="Grade", required=True, help="Grade for the course")