"""
A central repo for choices for various fields of forms
"""


PROGRAM_LEVEL_CHOICES = (
    ("be", "Bachelors"),
    ("msc", "Masters"),
    ("phd", "PhD")
)


BE_PROGRAM_CHOICES = (
    ("BCT", "BE Computer (BCT)"),
    ("BEX", "BE Electronics (BEX)"),
    ("BEI", "BEI"),
)

MSC_PROGRAM_CHOICES = (
    ("MSICE", "MSc in Information & Communications Engineering (MScICE)"),
    ("MSCSK", "MSc in Computer Systems and Knowledge engineering (MScCKSE)"),
)


GROUPED_PROGRAM_CHOICES = (
    ('Bachelors', BE_PROGRAM_CHOICES),
    ('Masters', MSC_PROGRAM_CHOICES),
    ('PhD', (
        ('PhD', 'PhD'),
    )),
)

BE_STUDENT_GROUP_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

TITLE_CHOICES = (
    ("Dr.", "Dr."),
    ("Er.", "Er."),
    ("Mr.", "Mr."),
    ("Ms.", "Ms."),
    ("Mrs.", "Mrs."),
)

BE_PROGRAM_TYPE_CHOICES = (
    ('Regular', 'Regular'),
    ('Full Fee', 'Full Fee'),
)

MSC_PROGRAM_TYPE_CHOICES = (
    ('Regular', 'Regular'),
    ('Full Fee', 'Full Fee'),
    ('Sponsorship', 'Sponsorship'),
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

ADDRESS_TYPE_CHOICES = (
    ("Current", "Current"),
    ("Permanent", "Permanent"),
)

ACADEMIC_LEVEL_CHOICES = (
    ("Masters", "Masters"),
    ("PhD", "PhD"),
    ("Post Doc.", "Post Doc."),
)

ACADEMIC_STATUS_CHOICES = (
    ("Ongoing", "Ongoing"),
    ("Completed", "Completed"),
)

EMPLOYMENT_STATUS_CHOICES = (
    ("Employed", "Employed"),
    ("Unemployed", "Unemployed"),
)

