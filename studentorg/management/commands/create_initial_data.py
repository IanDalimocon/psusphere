from typing import Any
from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_organization(10)
        self.create_students(50) 
        self.create_membership(10)
            
    def create_organization(self, count):
        fake = Faker()
            
        for _ in range(count):
            college = College.objects.create(name=fake.university(), address=fake.address())
            program = Program.objects.create(name=fake.job(), college=college)
            organization = Organization.objects.create(name=fake.company(), program=program)

        self.stdout.write(self.style.SUCCESS('Initial data for organizations created successfully.'))
                
    def create_students(self, count):
        fake = Faker()
        colleges = College.objects.all()
        programs = Program.objects.all()

        for _ in range(count):
            college = fake.random_element(colleges)
            program = fake.random_element(programs)
            Student.objects.create(
                name=f"{fake.first_name()} {fake.last_name()}",
                college=college,
                program=program
            )

        self.stdout.write(self.style.SUCCESS('Initial data for students created successfully.'))
                
    def create_membership(self, count):
        fake = Faker()
        students = Student.objects.all()
        organizations = Organization.objects.all()

        for _ in range(count):
            student = fake.random_element(students)
            organization = fake.random_element(organizations)
            OrgMember.objects.create(
                student=student,
                organization=organization,
                role=fake.job(),
                start_date=fake.date_between(start_date='-2y', end_date='-1y')
            )

        self.stdout.write(self.style.SUCCESS('Initial data for membership created successfully.'))
