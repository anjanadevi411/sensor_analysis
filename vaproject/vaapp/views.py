import csv, io
from tempfile import template
from datetime import date, datetime as dt
from django.shortcuts import render
from django.contrib import messages

from vaapp.models import Batch, Phsensor, Temp

# Create your views here.
def home(request):
    # declaring template
    template = 'home.html'
    batches = Batch.objects.all()
    time_deff = []
    for item in batches:
        time_deff.append((item.end_date - item.start_date).total_seconds())
    return render(request,template, {'batches': batches, 'time_diff' : time_deff})

def display(request, id):
    # declaring template
    template = 'display.html'
    batch = Batch.objects.get(pk = id)

    def convertKeyValue(listofDist):
        dist = {}
        for index in range(len(listofDist)):
            dist[dt.strftime(listofDist[index]['time'], '%Y-%m-%d %H:%M:%S')[:-3]] = listofDist[index]['value']
        # print(dist)
        return dist

    temps = Temp.objects.filter(time__gte = batch.start_date, time__lte = batch.end_date)
    temp_sensor1 = convertKeyValue(list(temps.filter(sensorName = '400E_Temp1').values('time', 'value')))
    temp_sensor2 = convertKeyValue(list(temps.filter(sensorName = '400E_Temp2').values('time', 'value')))

    phs = Phsensor.objects.filter(time__gte = batch.start_date, time__lte = batch.end_date)
    ph_sensor1 = convertKeyValue(list(phs.filter(sensorName = '400E_PH1').values('time', 'value')))
    ph_sensor2 = convertKeyValue(list(phs.filter(sensorName = '400E_PH2').values('time', 'value')))

    # print(temp_sensor1)
    # print(len(temp_sensor2))
    # print(len(ph_sensor1))
    # print(len(ph_sensor2))
    ret_tbl = []    

    # print(ph_sensor1)
    time_list = []
    for key in temp_sensor1.keys():
        # key = dt.strftime(temp_sensor1[index]['time'], '%Y-%m-%d %H:%M:%S')
        # print(key)
        # print(ph_sensor1[key])
        if key in temp_sensor1 and key in temp_sensor2 and key in ph_sensor1 and key in ph_sensor2:
            disc = {
                'time' : key,
                'temp_diff'  : temp_sensor2[key] - temp_sensor1[key],
                'ph_diff'   : ph_sensor2[key] - ph_sensor1[key],
            }
            # print(disc)
            # time_list.append(key)
            ret_tbl.append(disc)
    # print(ret_tbl)
    # print(len(ret_tbl))

    ret_data = {
        'batch' : batch.batch_id,
        'value_tbl' : ret_tbl,
    }
    # print(ret_data)
    return render(request, template, ret_data)

# one parameter named request
def upload_csv(request):
    # declaring template
    template = "upload_csv.html"
    # data = Phsensor.objects.all()
    
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be Date Time, data',
        # 'PH': data    
              }
    
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']
    
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    
    if("PH" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        
        # delete all exsiting records
        # Phsensor.objects.all().delete()

        next(io_string)
        for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
            print(column[0], ":", column[1])
            _, created = Phsensor.objects.update_or_create(
                time=column[0],
                value=column[1],
                sensorName=csv_file.name.split(".")[0],
            )
        context = {
            'message' : 'File has been uploaded'
        }
    
    if("Temp" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        
        # delete all exsiting records
        # Temp.objects.all().delete()

        next(io_string)
        for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
            print(column[0], ":", column[1])
            created = Temp.objects.update_or_create(
                time=column[0],
                value=column[1],
                sensorName=csv_file.name.split(".")[0],
            )
        context = {}

    if("batch" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        
        # delete all exsiting records
        # Batch.objects.all().delete()

        next(io_string)
        for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
            print(column[0], ":", column[1], ":", column[2])
            created = Batch.objects.update_or_create(
                start_date=column[0],
                end_date=column[1],
                batch_id=column[2],
            )
        context = {}

    return render(request, template, context)
    


    