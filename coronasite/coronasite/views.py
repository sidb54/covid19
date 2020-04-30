#Created by Me!!
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,render_to_response
import requests
import json
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
import datetime
from datetime import datetime as date
# from graphos.sources.simple import SimpleDataSource
# from graphos.renderers.yui import LineChart

states = []
totconfirm = []
totdeaths = []
totrecovery = []
totactive = []
newconfirm = []
newdeaths = []
newrecovery = []
state_dist ={}
state_names = []
context = {}

inddate = []
indcon = []
indact = []
inddeath = []
indrec = []
indtoday = []

countryname = []
slugname = []
cnewconf = []
ctotconf = []
cnewdeath = []
ctotdeath = []
cnewreco = []
ctotreco = []

earthdata = []
countrydata = []

def homepage(request):
    global states
    global totconfirm
    global totdeaths
    global totrecovery
    global totactive
    global newconfirm
    global newdeaths
    global newrecovery
    global state_names
    global state_dist
    global context
    global inddate
    global indcon
    global indact
    global inddeath
    global indrec
    global indtoday
    global countryname
    global slugname
    global cnewconf
    global ctotconf
    global cnewdeath
    global ctotdeath
    global cnewreco
    global ctotreco
    global earthdata
    global countrydata

    response = requests.get("https://api.covid19india.org/data.json")
    response_json = response.json()

    response1 = requests.get("https://api.covid19india.org/state_district_wise.json")
    response1_json = response1.json()

    response2 = requests.get("https://api.covid19api.com/dayone/country/india")
    response2_json = response2.json()

    #print(response2_json)
    #state_dist = {}
    if(len(states)!=0):
        return render(request, 'home.html',context)

    #ctr = 0
    for dic in response2_json:
        dt = dic['Date'].split('T')
        inddate.append(dt[0])
        indcon.append(dic['Confirmed'])
        indrec.append(dic['Recovered'])
        inddeath.append(dic['Deaths'])
        indact.append(str(int(dic['Confirmed'])-int(dic['Recovered'])-int(dic['Deaths'])))

    #print(indtoday)

    for key in response1_json:
	    state = response1_json[key]
	    dist_data = response1_json[key]
	    dist_data = dist_data["districtData"]
	    dist_list = []
	    for dist in dist_data:
		    district = dist
		    values = dist_data[dist]
		    active = values["active"]
		    confirmed = values["confirmed"]
		    deceased = values["deceased"]
		    recovered = values["recovered"]
		    delconfirm = values["delta"]["confirmed"]
		    deldeceased = values["delta"]["deceased"]
		    delrecovered = values["delta"]["recovered"]
		    #print(district)
		    dist_list1 = []
		    dist_list1.append(district)
		    dist_list1.append(confirmed)
		    dist_list1.append(active)
		    dist_list1.append(delconfirm)
		    dist_list1.append(recovered)
		    dist_list1.append(delrecovered)
		    dist_list1.append(deceased)
		    dist_list1.append(deldeceased)
		    dist_list.append(dist_list1)
	    statename = key
	    state_dist[statename] = dist_list

    #print(state_dist)

    #print(dictionary)
    sd = response_json['statewise']

    for i in sd:
	    states.append(i["state"])
	    totconfirm.append(i["confirmed"])
	    totactive.append(i["active"])
	    totdeaths.append(i["deaths"])
	    totrecovery.append(i["recovered"])
	    newconfirm.append(i["deltaconfirmed"])
	    newdeaths.append(i["deltadeaths"])
	    newrecovery.append(i["deltarecovered"])

    for i in sd:
        indtoday.append(i["confirmed"])
        indtoday.append(i["active"])
        indtoday.append(i["recovered"])
        indtoday.append(i["deaths"])
        indtoday.append(i["deltaconfirmed"])
        indtoday.append(i["deltadeaths"])
        indtoday.append(i["deltarecovered"])
        break
    
    response3 = requests.get("https://api.covid19api.com/summary")
    response3_json = response3.json()
    countries = response3_json['Countries']
    globe = response3_json['Global']
    earthdata = globe
    countries = sorted(countries, key = lambda i: i['TotalConfirmed'],reverse=True)
    #print(countries)

    for key in countries:
        clist = []
        countryname.append(key['Country'])
        slugname.append(key['Slug'])
        cnewconf.append(key['NewConfirmed'])
        ctotconf.append(key['TotalConfirmed'])
        cnewdeath.append(key['NewDeaths'])
        ctotdeath.append(key['TotalDeaths'])
        cnewreco.append(key['NewRecovered'])
        ctotreco.append(key['TotalRecovered'])  
        clist.append(key['Country']) 
        clist.append(key['Slug'])
        clist.append(key['NewConfirmed']) 
        clist.append(key['TotalConfirmed'])
        clist.append(key['NewDeaths'])
        clist.append(key['TotalDeaths'])
        clist.append(key['NewRecovered'])
        clist.append(key['TotalRecovered'])
        clist.append(str(int(key['TotalConfirmed'])-int(key['TotalDeaths'])-int(key['TotalRecovered'])))
        countrydata.append(clist)

    state_names = states[1:]
    #print(state_names)
    statelist=""
    for i in state_names:
        statelist = statelist+i+":"
    #print(statelist)
    context = {"states" : state_names,"counties": slugname, "ll":[1], "ed" :earthdata}
    return render(request, 'home.html',context)

countrylist = []
sluglist = []
cnewconf = []
ctotconf = []
cnewd = []
 

def statsum(request):
    #print(states)
    statlist = []
    for i in range(0,len(states)-1):
        curr = []
        curr.append(state_names[i])
        curr.append(totconfirm[i+1])
        curr.append(totactive[i+1])
        curr.append(newconfirm[i+1])
        curr.append(totrecovery[i+1])
        curr.append(newrecovery[i+1])
        curr.append(totdeaths[i+1])
        curr.append(newdeaths[i+1])
        statlist.append(curr)
    #print(statlist)
    context1 = {'data':statlist,"states" : state_names,"counties": slugname, "ll":[]}
    return render(request,'statesummary.html',context1)


def statedata(request):
    return render_to_response('stdata.html', {'script' : script, 'div' : div})

def chartjsview(request):
    #print(indact)
    data={
        "labels": inddate,
        "confirm": indcon,
        "active": indact,
        "recovered": indrec,
        "deaths": inddeath,
        "indtoday": indtoday
    }
    return render(request,'test.html',data)


def index(request):
    stateclicked = request.GET.get('drop')
    ind = 0
    #print(stateclicked)
    #print(states)

    if(stateclicked not in state_dist):
        return render(request, 'home.html',context)

    for i in range(0,len(states)):
        if(states[i]==stateclicked):
            ind = i
            break
    #print(str(ind))
    now = datetime.datetime.now()
    dt = now.strftime("%d-%m-%Y")
    da = date.today().strftime("%A")
    #print(state_dist)
    distdata = state_dist[stateclicked]
    context2 = {"ll":[],'stname': stateclicked, 'districts': distdata,'dt':dt, 'day':da, 'totc': totconfirm[ind], 'tota':totactive[ind], 'totd': totdeaths[ind], 'totr': totrecovery[ind], 'nc': newconfirm[ind], 'nd': newdeaths[ind], 'nr': newrecovery[ind], "states" : state_names,"counties": slugname}
    return render(request, 'stdata.html', context2)
   
def globaldata(request):
    c = {'cdata':countrydata, "states" : state_names,"counties": slugname, "ll":[]}
    return render(request, 'worldsummary.html', c)
    
def countrywise(request):

    response4 = requests.get("https://api.covid19api.com/dayone/country/"+request.GET.get('drop2'))
    response4_json = response4.json()
    print(response4_json)
    ind = 0
    for i in range(0,len(countrydata)):
        if(countrydata[i][1] == request.GET.get('drop2')):
            ind = i
            break
    


    cdate = []
    ccon = []
    crec = []
    cdeath = []
    cact = []
    for dic in response4_json:
        dt = dic['Date'].split('T')
        cdate.append(dt[0])
        ccon.append(dic['Confirmed'])
        crec.append(dic['Recovered'])
        cdeath.append(dic['Deaths'])
        cact.append(str(int(dic['Confirmed'])-int(dic['Recovered'])-int(dic['Deaths'])))

    data2={
        "labels": cdate,
        "confirm": ccon,
        "active": cact,
        "recovered": crec,
        "deaths": cdeath,
        "indtoday": cact,
        "cname": countrydata[i][0],
        "cnewconf": countrydata[i][2],
        "ctotconf": countrydata[i][3],
        "cnewdeath": countrydata[i][4],
        "ctotdeath": countrydata[i][5],
        "cnewreco": countrydata[i][6],
        "ctotreco": countrydata[i][7],
        "ctotact": str(int(countrydata[i][3])-int(countrydata[i][7])-int(countrydata[i][5])),
        "states" : state_names,
        "counties": slugname,
        "ll":[]

    }

    return render(request,'test.html', data2)    