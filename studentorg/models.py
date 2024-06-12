from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class College(BaseModel):
    college_name = models.CharField(max_length=150)
    
    def  __str__(self):
        return self.college_name

class Program(BaseModel):
    prog_name = models.CharField(max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def  __str__(self):
        return self.prog_name
    
class Organization(BaseModel):
    name = models.CharField(max_length=150)
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    def   __str__(self):
        return self.name
    

class Student(BaseModel):
    student_id = models.CharField(max_length=15)  # Binago mula sa max_lenght papunta sa max_length
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=25)
    middlename = models.CharField(max_length=25, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)  # Inayos ang pangalan ng field

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"

    
class OrgMember(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date_joined = models.DateField()


class Incident(models.Model):
    severity_level = models.CharField(max_length=50)
    date_time = models.DateTimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.severity_level} - {self.date_time}"
