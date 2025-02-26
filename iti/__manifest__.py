{
    'name': 'ITI Q1 Module',
    'version': '1.0',
    'description': 'First module containing ITI students and tracks',
    'author': 'ITI Minia',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'reports/iti_student_templates.xml',
        'reports/iti_reports.xml',  
        'security/iti_security.xml',  
        'security_iti/ir.model.access.csv',     
        'views/iti_student_views.xml',
        'views/iti_track_views.xml',
    ],
}
