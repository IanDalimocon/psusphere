from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, Student, College
from studentorg.forms import OrganizationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.db.models import Q

# College
class CollegeList(ListView):
    model = College
    template_name = 'college_list.html'
    paginate_by = 10

# Student
class StudentCreateView(CreateView):
    model = Student
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentList(ListView):
    model = Student
    template_name = 'student_list.html'
    paginate_by = 10

def forms_view(request):
    return render(request, 'forms.html', {})

# Organization
class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

@method_decorator([login_required], name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = 'org_list.html'
    paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return qs
    
def PieCountbySeverity(request):
    query = '''
    SELECT severity_level, COUNT(*) as count
    FROM fire_incident
    GROUP BY severity_level
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}

    return JsonResponse(data)
