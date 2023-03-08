from django.views.generic import View
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import csv
from faker import Faker
from io import StringIO


class GenerateCSVView(View):
    def post(self, request):
        fake = Faker()
        data = StringIO()
        writer = csv.writer(data)
        writer.writerow([
            'First Name',
            'Last Name', 
            'Job', 
            'Email', 
            'Domain', 
            'Phone Number', 
            'Company Name', 
            'Text', 
            'Integer', 
            'Address', 
            'Date'
        ])
        num_records = int(request.POST.get('num-records', 1))
        for i in range(num_records):
            writer.writerow([
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
            ])
        data.seek(0)
        filename = 'fake_data.csv'
        fs = FileSystemStorage(location='media')
        file = fs.save(filename, data)
        url = fs.url(file)
        return JsonResponse({'url': url, 'num_records': num_records})

    def get(self, request):
        return render(request, 'generate_csv.html', {})
