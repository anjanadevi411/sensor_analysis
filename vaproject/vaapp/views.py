import csv
from io import StringIO
from django.http import HttpResponse
from datetime import datetime as dt
from django.shortcuts import render
from django.contrib import messages
from matplotlib import pyplot as plt
# from matplotlib import style
# style.use("fivethirtyeight")
from matplotlib.backends.backend_agg import FigureCanvasAgg

from .models import Batch, Phsensor, Temp

def home(request):
    template = 'home.html'
    batches = Batch.objects.all()
    time_diff = []
    for item in batches:
        time_diff.append((item.end_date - item.start_date).total_seconds())
    return render(request,template, {'batches': batches, 'time_diff' : time_diff})

def display(request, id):
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

    #print('temp_sensor1',temp_sensor1)
    #print('length of next temp sensor',len(temp_sensor1))
    # print(len(ph_sensor1))
    # print(len(ph_sensor2))
    ret_tbl = []    

    # print(ph_sensor1)
    #time_list = []
    time_plot = []
    temp_plot = []
    ph_plot = []
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
            time_plot.append(disc['time'])
            temp_plot.append(disc['temp_diff'])
            ph_plot.append(disc['ph_diff'])
    # print(ret_tbl)
    # print(len(ret_tbl))

    context = {
        'batch' : batch.batch_id,
        'value_tbl' : ret_tbl,
    }

    #####
    # fig, ax = plt.subplots()
    # ax.plot(time_plot,ph_plot)
    # ax.set(xlabel='time_plot (s)', ylabel='temp_plot', title='Analysis of temperature and PH sensor with batch ID')
    # ax.grid()

    # response = HttpResponse(content_type = 'image/png')
    # canvas = FigureCanvasAgg(fig)
    # canvas.print_png(response)
    # return response
   
    # print(ret_data)
    return render(request, template, context)

def upload_csv(request):
    # declaring template
    template = "upload_csv.html"
    
    prompt = {
        'order': 'Order of the CSV should be Date Time, data',
              }
    
    # GET request
    if request.method == "GET":
        return render(request, template, prompt)
    
    #POST
    if request.method == "POST":
        csv_file = request.FILES['file']
    
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
        return render(request, template)

    data_set = csv_file.read().decode('UTF-8')
    
    if("PH" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = StringIO(data_set)
        
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
        messages.info(request, 'File has been uploaded')
    
    if("Temp" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = StringIO(data_set)
        
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
        messages.info(request, 'File has been uploaded')

    if("batch" in csv_file.name):
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = StringIO(data_set)
        
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
        messages.info(request, 'File has been uploaded')

    return render(request, template)
    


    