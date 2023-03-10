from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from generate.models import Schema
from django.views import View
from faker import Faker
from io import StringIO
import csv
from django.shortcuts import render, redirect
from django.contrib.auth import login


class GenerateCSVView(View):
    def post(self, request):
        fake = Faker()
        data = StringIO()
        writer = csv.writer(data)

        # Get all existing schemas and add their fields to the CSV header row
        schemas = Schema.objects.all()
        header_row = ['First Name', 'Last Name', 'Job', 'Email', 'Domain', 'Phone Number', 'Company Name', 'Text', 'Integer', 'Address', 'Date']
        for schema in schemas:
            for field in schema.fields:
                header_row.append(field['name'])

        writer.writerow(header_row)

        num_records = int(request.POST.get('num-records', 1))
        for i in range(num_records):
            row = [
                fake.first_name(),
                fake.last_name(),
                fake.job(),
                fake.email(),
                fake.domain_name(),
                fake.phone_number(),
                fake.company(),
                fake.text(),
                fake.random_int(min=0, max=100),
                fake.address(),
                fake.date(),
            ]

            # Generate data for fields from each schema
            for schema in schemas:
                for field in schema.fields:
                    if field['type'] == 'text':
                        row.append(fake.text())
                    elif field['type'] == 'integer':
                        row.append(fake.random_int(min=0, max=100))
                    elif field['type'] == 'address':
                        row.append(fake.address())
                    elif field['type'] == 'date':
                        row.append(fake.date())

            writer.writerow(row)

        status = 'ready'
        data.seek(0)
        filename = 'fake_data.csv'
        fs = FileSystemStorage(location='media')
        file = fs.save(filename, data)
        url = fs.url(file)
        return JsonResponse({'url': url, 'num-records': num_records, 'status': status})

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        status = 'ready'
        return render(request, 'generate_csv.html', {'status': status})
    

class CreateSchemaView(View):
    def post(self, request):
        name = request.POST.get('name')
        fields = []
        for i in range(len(request.POST.getlist('fields[][name]'))):
            field_name = request.POST.getlist('fields[][name]')[i]
            field_type = request.POST.getlist('fields[][type]')[i]
            fields.append({'name': field_name, 'type': field_type})
        schema = Schema(name=name, fields=fields)
        schema.save()
        return JsonResponse({'status': 'ready', 'schema_id': schema.id})


    def get(self, request):
        return render(request, 'create_schema.html', {})
    

class AddFieldView(View):
    def post(self, request):
        schema_id = request.POST.get('schema_id')
        field_data = request.POST.get('field')
        if field_data:
            schema = Schema.objects.get(id=schema_id)
            fields = schema.fields
            fields.append(field_data)
            schema.fields = fields
            schema.save()
        return JsonResponse({'status': 'ready', 'schema_data': request.POST})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form})
    