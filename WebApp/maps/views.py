
from django.shortcuts import render
from django.views.generic import TemplateView
from maps.inputform import InputForm
from urllib.parse import quote
import googlemaps
import json
import urllib.request
from datetime import datetime
import time
from maps.models import Model_DataTable



class HomeView(TemplateView):

    template_name = 'maps/index.html'

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form' : form, 'flag': -1})

    def post(self, request):

        form = InputForm(request.POST)

        #creating google maps client object
        gmaps = googlemaps.Client(key='YOUR_KEY')

        if form.is_valid():
            #form.save()
            start = form.cleaned_data['Start']
            destination = form.cleaned_data['End']
            #return HttpResponseRedirect('/search/')

        args = {'form': form, 'start': start, 'end': destination}

        starttime = time.time()

        #Fetch Table data from database
        data_table = Model_DataTable.objects.all()

        #data_object stores record from data_table if record is found
        data_object = None

        #Iteration over the records found in the data_table
        for data in data_table:
            #if start, destination and date of the record matched with the one we entered in the form, we store the record in data_object and break from loop
            if data.Start == start and data.End == destination and str(data.date) == datetime.today().strftime('%Y-%m-%d'):
                data_object = data
                break

        #if data_object is not null, we fetch the google api and weather api responses from the object and store those in respective variables
        #we also fetch weather responses for start and destination

        if data_object is not None :

            #setting the parameters by extracting them from data_object like google response, weather response
            direction = data_object.google_response
            weather_dict = data_object.weather_response


            x_param = quote(str(request.POST['Start']))
            y_param = quote(str(request.POST['End']))


            endtime_db= time.time()

            #printing database access time
            print(endtime_db- starttime)

            #Send google api, weather api responses to index.html
            return render(request, self.template_name,
                          {'form': form, 'response': json.dumps(direction), 'flag': 1, 'start': start,
                           'end': destination,  'weather_dict': json.dumps(weather_dict)})

        #else, we call APIs to get the responses (google maps and weather) and save them to database
        else:

            #creating google maps client object
            gmaps = googlemaps.Client(key='YOUR_KEY')


            x = str(request.POST['Start'])
            y= str(request.POST['End'])

            x_param = quote(x)
            y_param = quote(y)

            #sending request to google maps api for route
            request1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + x_param + "&destination=" + y_param + "&key=AIzaSyBQThVIW-tNgV4Yth_Evk_vbLS4cVQgjgU"
            response = urllib.request.urlopen(request1).read()
            direction = json.loads(response)

            if str(direction['status']) != 'ZERO_RESULTS':

                weather_list=[]

                weather_dict= dict()
                i =1

                for x in direction['routes'][0]['legs'][0]['steps']:
                    lat = str(x['start_location']['lat'])
                    lon = str(x['start_location']['lng'])
                    lat_param = quote(lat)
                    lon_param = quote(lon)
                    req = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat_param + "&lon=" + lon_param + "&appid=66b64cfa937f31bbd5cb328cdad938a0"
                    weather_response = urllib.request.urlopen(req).read()
                    weather_res = json.loads(weather_response)
                    weather_list.append(weather_res['weather'][0]['main'])
                    temp = dict()

                    #Everything is in try catch because sometimes, we dont some information for the particular waypoint like pressure etc
                    try:
                        temp['Name'] = str(weather_res['name'])
                    except:
                        temp['Name'] = "Not Defined"
                    try:
                        temp['Description']= str(weather_res['weather'][0]['description'])
                    except:
                        temp['Description'] = "Not Defined"
                    try:
                        temp['Temp_Min'] = str(round((weather_res['main']['temp_min'] -273.15)*1.8 +32, 2))
                    except:
                        temp['Temp_Min'] = "Not Defined"
                    try:
                        temp['Temp_Max'] = str(round((weather_res['main']['temp_max'] -273.15)*1.8 +32 , 2))
                    except:
                        temp['Temp_Max'] = "Not Defined"
                    try:
                        temp['Pressure'] = str(weather_res['main']['pressure'])
                    except:
                        temp['Pressure'] = "Not Defined"
                    try:
                        temp['Humidity'] = str(weather_res['main']['humidity'])
                    except:
                        temp['Humidity'] = "Not Defined"
                    try:
                        temp['Wind_Speed'] = str(weather_res['wind']['speed'])
                    except:
                        temp['Wind_Speed'] = "Not Defined"
                    try:
                        temp['Wind_Degree'] = str(weather_res['wind']['deg'])
                    except:
                        temp['Wind_Degree'] = "Not Defined"

                    weather_dict[str(i)]=temp
                    i=i+1


                #appending direction object with request
                destination={}
                origin={}
                destination['query'] = y
                origin['query'] =x
                direction['request'] = {'destination': destination, 'origin': origin, 'travelMode': str(request.POST['Mode'])}


                #Saving data to database table
                object_datatable = Model_DataTable()
                object_datatable.Start = start
                object_datatable.End = form.cleaned_data['End']
                object_datatable.Mode = request.POST['Mode']
                object_datatable.google_response = direction
                object_datatable.weather_response = weather_dict
                object_datatable.save()

                endtime_api = time.time()

                #Printing time required for API access
                print( endtime_api - starttime)

                return render(request, self.template_name,
                              {'form': form, 'response': json.dumps(direction), 'flag': 1, 'start': start,
                               'end': destination,  'weather_dict': json.dumps(weather_dict)})

            else:

                form = InputForm()
                return render(request, self.template_name, {'form': form, 'flag': 0})


#fetching the latitude and longitudes for a particular location
def fetch_latlong(loc, gmaps):
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]

    lat = str(lat)
    lon = str(lon)
    lat_param = quote(lat)
    lon_param = quote(lon)

    return lat_param, lon_param
