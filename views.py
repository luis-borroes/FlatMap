from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from luis.settings import BASE_DIR
from os.path import join
from csv import reader
from ast import literal_eval
from math import ceil
from time import sleep
from shapely.geometry import Point as shapelyPoint
from shapely.geometry.polygon import Polygon as shapelyPolygon
from .utils import getCont, xRender
from .map.parser import ShapeMap, Poly
from .map.address import AddressRegex
import geocoder

from .models import *


def index(request):
	evts = Event.objects.order_by('data')[:4]
	news = NewsReport.objects.order_by('data')[:4]
	vids = Video.objects.order_by('data')[:4]

	context = {
		'cont': getCont("index"),
		'evts': evts,
		'news': news,
		'vids': vids
	}

	return xRender(request, 'flatmap/base/index.html', context)



def about(request):
	context = {\
		'cont': getCont("about"),
	}

	return xRender(request, 'flatmap/base/content/about.html', context, "about")



def evtsList(request):
	evts = Event.objects.order_by('data')[:4]

	context = {
		'evts': evts,
	}

	return xRender(request, 'flatmap/base/contList/events.html', context, "events")



def newsList(request):
	news = NewsReport.objects.order_by('data')[:4]

	context = {
		'news': news,
	}

	return xRender(request, 'flatmap/base/contList/newsreports.html', context, "news")



def evtsDisp(request, slug):
	evt = Event.objects.get(slug=slug)

	context = {
		'evt': evt,
	}

	return xRender(request, 'flatmap/base/content/event.html', context, "events")



def newsDisp(request, slug):
	newRep = NewsReport.objects.get(slug=slug)

	context = {
		'newRep': newRep,
	}

	return xRender(request, 'flatmap/base/content/newsreport.html', context, "news")




def listIPSS(request):
	dists = District.objects.all()
	couns = {}
	fregs = {}

	perPage = 18

	insts = Institution.objects.order_by('denominacao')

	gDist = request.GET.get('d', '')
	gConc = request.GET.get('c', '')
	gFreg = request.GET.get('f', '0')
	gQuery = request.GET.get('q', '')

	if request.method == 'GET':

		if gDist != '':
			dist = District.objects.get(slug=gDist)
			insts = Institution.objects.filter(sede__distrito=dist).order_by('denominacao')

			if gConc != '':
				coun = Council.objects.get(slug=gConc)

				# only display intersection if concelho is part of distrito
				if coun.distrito == dist:
					insts = Institution.objects.filter(sede__distrito=dist, sede__concelho=coun).order_by('denominacao')


					if gFreg != '0':
						freg = Parish.objects.get(id=gFreg)

						# only display intersection if freguesia is part of concelho
						if freg.concelho == coun:
							insts = Institution.objects.filter(sede__distrito=dist, sede__concelho=coun, sede__freguesia=freg).order_by('denominacao')


				fregs = Parish.objects.filter(concelho__distrito=dist, concelho=coun)
			
			couns = Council.objects.filter(distrito=dist)


		if gQuery != '':
			q = gQuery.replace('.', ' ')
			q = q.replace(',', ' ')
			q = q.replace(':', ' ')
			q = q.replace(';', ' ')

			for word in slugify(q).split('-'):
				try:
					tag = Tag.objects.get(name=word)
					insts = insts.filter(tags=tag)

				except Tag.DoesNotExist:
					insts = Institution.objects.none()
				


	numInsts = len(insts)
	numPages = ceil(numInsts / perPage)
	pageList = range(1, numPages + 1)


	page = int(request.GET.get('p', 1))

	if page not in pageList:
		page = 1

	prevPage = page - 1 if page > 1 else 1
	nextPage = page + 1 if page < numPages else numPages

	first = perPage * (page - 1) # if page is 1, start from 0, if page is 2, start from "perPage" etc
	last = perPage * page # finish 1 * perPage items later


	context = {
		'insts': insts[first:last],
		'dists': dists,
		'couns': couns,
		'fregs': fregs,
		'first': first + 1,
		'last': min(last, numInsts),
		'numInsts': numInsts,
		'page': page,
		'prevPage': prevPage,
		'nextPage': nextPage,
		'numPages': numPages,
		'pageList': pageList,
		'pageType': 'filtros',
		'post': request.GET
	}

	return xRender(request, 'flatmap/base/search/list.html', context, "search")



def mapsIPSS(request):
	areas = District.objects.all()
	urlType = 'flatmap:mapsIPSSDist'
	crumbs = []


	context = {
		'pageType': 'mapa',
		'crumbs': crumbs,
		'areas': areas,
		'viewBox': "-9.6 -50.7 3.5 6.4",
		'clickable': True,
		'urlType': urlType,
		'showInstsPane': False
	}

	return xRender(request, 'flatmap/base/search/map.html', context, "search")



def mapsIPSSDist(request, dist):
	district = District.objects.get(id=dist)
	areas = Council.objects.filter(distrito=district)
	urlType = 'flatmap:mapsIPSSConc'
	crumbs = [[district.denominacao, 'flatmap:mapsIPSSDist', district.id]]

	equips = Equipment.objects.filter(distrito = district).exclude(latitude='')
	points = equips


	context = {
		'pageType': 'mapa',
		'crumbs': crumbs,
		'areas': areas,
		'points': equips,
		'equips': equips,
		'viewBox': district.viewBox,
		'clickable': True,
		'urlType': urlType,
		'showInstsPane': True
	}

	return xRender(request, 'flatmap/base/search/map.html', context, "search")



def mapsIPSSConc(request, conc):
	council = Council.objects.get(id=conc)
	areas = Parish.objects.filter(concelho=council)
	urlType = 'flatmap:mapsIPSSFreg'
	crumbs = [[council.distrito.denominacao, 'flatmap:mapsIPSSDist', council.distrito.id],
			[council.denominacao, 'flatmap:mapsIPSSConc', council.id]]

	equips = Equipment.objects.filter(distrito = council.distrito, concelho = council).exclude(latitude='')
	points = equips


	context = {
		'pageType': 'mapa',
		'crumbs': crumbs,
		'areas': areas,
		'points': points,
		'equips': equips,
		'viewBox': council.viewBox,
		'clickable': True,
		'urlType': urlType,
		'showInstsPane': True
	}

	return xRender(request, 'flatmap/base/search/map.html', context, "search")



def mapsIPSSFreg(request, freg):
	parish = Parish.objects.get(id=freg)
	areas = [parish]
	crumbs = [[parish.concelho.distrito.denominacao, 'flatmap:mapsIPSSDist', parish.concelho.distrito.id],
			[parish.concelho.denominacao, 'flatmap:mapsIPSSConc', parish.concelho.id],
			[parish.denominacao, 'flatmap:mapsIPSSConc', parish.id]]

	equips = Equipment.objects.filter(distrito = parish.concelho.distrito, concelho = parish.concelho, freguesia = parish).exclude(latitude='')
	points = equips


	context = {
		'pageType': 'mapa',
		'crumbs': crumbs,
		'areas': areas,
		'points': points,
		'equips': equips,
		'viewBox': parish.viewBox,
		'clickable': False,
		'showInstsPane': True
	}

	return xRender(request, 'flatmap/base/search/map.html', context, "search")





def dispIPSS(request, inst):
	inst = Institution.objects.get(id=inst)
	sede = inst.sede

	if sede.freguesia is not None:
		parish = sede.freguesia
		areas = [parish]
		crumbs = [[parish.concelho.distrito.denominacao, 'flatmap:mapsIPSSDist', parish.concelho.distrito.id],
				[parish.concelho.denominacao, 'flatmap:mapsIPSSConc', parish.concelho.id],
				[parish.denominacao, 'flatmap:mapsIPSSConc', parish.id]]

	else:
		council = sede.concelho
		areas = [council]
		crumbs = [[council.distrito.denominacao, 'flatmap:mapsIPSSDist', council.distrito.id],
				[council.denominacao, 'flatmap:mapsIPSSConc', council.id]]

	points = [sede]


	context = {
		'inst': inst,
		'pageType': 'mapa',
		'crumbs': crumbs,
		'areas': areas,
		'points': points,
		'viewBox': areas[0].viewBox,
		'clickable': False,
		'showInstsPane': True
	}


	return xRender(request, 'flatmap/base/search/ipss.html', context, "search")






# Hacky code to manipulate database below
# There's definitely better ways of doing this...





def genIPSSDatabase(request):
	#return genMaps(request)
	#return genMapBoxes(request)
	
	#return geocode(request)
	#return parseGeoCoords(request)
	
	#return geocode2(request)
	#return geoTest(request)
	#return parseGeoCoords2(request)

	#return addFregToEquips(request)
	#return fregTest(request)
	#return parseGeoCoords3(request)
	#return addMissingFregToEquips(request)

	#return genInstSlugs(request)
	#return genDivSlugs(request)

	#return renameFregs(request)
	#return renameInsts(request)

	#return populateAddressModel(request)
	#return listAddresses(request)

	pass



def listAddresses(request):
	addresses = Address.objects.all()
	addresses = addresses.filter(arteria='').filter(porta='').filter(alojamento='').filter(localidade='').exclude(original='')

	addReg = AddressRegex()
	out = addReg.parse(addresses)

	return HttpResponse(out)



def populateAddressModel(request):
	out = ""
	count = 0

	for equip in Equipment.objects.all():
		if equip.morada_fk is None:
			address = Address(original = equip.morada)
			address.save()

			equip.morada_fk = address
			equip.save()

		
		count += 1
		print(count)

		if count > 5:
			#break
			pass

	return HttpResponse(out)



def renameInsts(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		name = inst.denominacao

		if name[0] == '"' and name[-1] == '"':
			inst.denominacao = name[1:-1]
			#inst.save()
			out += str(count) + inst.denominacao + "<br>"

		count += 1
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def renameFregs(request):
	out = ""
	count = 0

	for parish in Parish.objects.all():
		if "freguesias" in parish.denominacao:
			parish.denominacao = parish.denominacao.replace("freguesias", "Freguesias")
			#parish.save()
			out += str(count) + parish.denominacao + "<br>"

		count += 1
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def genDivSlugs(request):
	out = ""
	count = 0

	for inst in District.objects.all():
		inst.save()
		count += 1

		out += str(count) + inst.slug + "<br>"
		print(count)

		if count > 10:
			#break
			pass

	for inst in Council.objects.all():
		inst.save()
		count += 1

		out += str(count) + inst.slug + "<br>"
		print(count)

		if count > 10:
			#break
			pass

	for inst in Parish.objects.all():
		inst.save()
		count += 1

		out += str(count) + inst.slug + "<br>"
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def genInstSlugs(request):
	out = ""
	count = 0

	for t in Tag.objects.all():
		t.delete()


	for inst in Institution.objects.all():
		inst.save()
		count += 1

		out += str(count) + inst.denominacao + "<br>"
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def geoTest(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		sede = inst.sede
		addr = sede.morada
		city = sede.concelho.denominacao

		count += 1

		if sede.geocode2 != '':

			data = literal_eval(sede.geocode2) # replace single quote with double
			
			try:
				print(data['status'])
				out += str(count) + " - " + data['status'] + " - " + sede.denominacao + "<br>"

			except Exception as e:
				print(str(e))
				out += str(count) + " - " + str(e) + " - " + sede.denominacao + "<br>"

			#sede.save()


		else:
			out += str(count) + " - fail - " + sede.denominacao + "<br>"


		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def fregTest(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		sede = inst.sede

		if sede.freguesia == None:
			count += 1
			out += str(count) + " - " + sede.denominacao + " - " + sede.distrito.denominacao + " - " + sede.concelho.denominacao + "<br>"
			out += str(count) + " - " + str(sede.morada) + "<br><br>"

			#query = "{}, {}, PT".format(sede.morada.split(",")[0], sede.concelho.denominacao).lower()
			#query = query.replace("n.o", "")
			#query = query.replace("no.", "")

			#g = geocoder.bing(query, key='AkhOmRDTPjff-SzS682xqnmlO67Cq7U6Ee6VFYH-pi_MEA8LI-8-KkApHdvYcEI0')
			#inst.sede.geocode3 = g.json if g.json is not None else ''
			#inst.sede.save()

			#print(query)
			#print(g.json)
			#sleep(1)



		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def addMissingFregToEquips(request):
	out = ""
	count = 0


	polyCache = {}

	for inst in Institution.objects.exclude(sede__geocode3=''):
		sede = inst.sede

		council = sede.concelho
		parishes = council.parish_set.all()

		for parish in parishes:
			#out += str(parish.poly) + "<br>"

			# cache polygon maps
			if parish.id not in polyCache:
				polyPoints = []

				for polyPoint in parish.poly.split():
					coordsList = polyPoint.split(',')

					polyPoints.append((float(coordsList[0]), float(coordsList[1])))
					
				poly = shapelyPolygon(polyPoints)

				polyCache[parish.id] = poly

			else:
				poly = polyCache.get(parish.id)


			equip = sede
			#out += str(equip.latitude) + "," + str(equip.longitude) + "<br>"


			p = shapelyPoint(float(equip.longitude), float(equip.latitude))


			if poly.contains(p):
				out += str(parish) + " - " + str(equip) + "<br>"

				if equip.freguesia == None:
					equip.freguesia = parish
					equip.save()

				else:
					out += str(parish) + " IS NOT NONE " + str(equip) + "<br>"




			else:
				out += str(parish) + " NOT " + str(equip) + "<br>"




		count += 1
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def addFregToEquips(request):
	out = ""
	count = 0

	for council in Council.objects.all():
		parishes = council.parish_set.all()

		for parish in parishes:
			#out += str(parish.poly) + "<br>"

			polyPoints = []

			for polyPoint in parish.poly.split():
				coordsList = polyPoint.split(',')

				polyPoints.append((float(coordsList[0]), float(coordsList[1])))
				
			poly = shapelyPolygon(polyPoints)


			equips = Equipment.objects.filter(distrito=council.distrito, concelho=council)
			for equip in equips:
				#out += str(equip.latitude) + "," + str(equip.longitude) + "<br>"


				p = shapelyPoint(float(equip.longitude), float(equip.latitude))


				if poly.contains(p):
					out += str(parish) + " - " + str(equip) + "<br>"

					if equip.freguesia == None:
						equip.freguesia = parish
						#equip.save()

					else:
						out += str(parish) + " IS NONE " + str(equip) + "<br>"




				else:
					out += str(parish) + " NOT " + str(equip) + "<br>"




		count += 1
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def parseGeoCoords3(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		sede = inst.sede
		addr = sede.morada
		city = sede.concelho.denominacao

		if sede.geocode3 != '':
			count += 1

			print(sede)

			data = literal_eval(sede.geocode3) # replace single quote with double
			print(data['lng'])
			print(data['lat'])

			sede.longitude = data['lng']
			sede.latitude = str(float(data['lat']) * -1.2)

			sede.save()


		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def parseGeoCoords2(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		sede = inst.sede
		addr = sede.morada
		city = sede.concelho.denominacao

		if sede.geocode2 != '':
			count += 1

			print(sede)

			data = literal_eval(sede.geocode2) # replace single quote with double
			print(data['lng'])
			print(data['lat'])

			sede.longitude = data['lng']
			sede.latitude = str(float(data['lat']) * -1.2)

			sede.save()


		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def parseGeoCoords(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		sede = inst.sede
		addr = sede.morada
		city = sede.concelho.denominacao

		if sede.geocode != '':
			count += 1

			print(sede)

			data = literal_eval(sede.geocode) # replace single quote with double
			print(data['lng'])
			print(data['lat'])

			sede.longitude = data['lng']
			sede.latitude = str(float(data['lat']) * -1.2)

			sede.save()


		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def geocode2(request):
	out = ""
	count = 0

	for inst in Institution.objects.all()[4344:]:
		addr = inst.sede.morada
		council = inst.sede.concelho.denominacao

		query = "{}, {}, PT".format(addr.split(",")[0], council).lower()
		query = query.replace("n.o", "")
		query = query.replace("no.", "")

		g = geocoder.arcgis(query)
		inst.sede.geocode2 = g.json if g.json is not None else ''
		inst.sede.save()

		print(query)
		print(g.json)
		sleep(1)

		count += 1
		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def geocode(request):
	out = ""
	count = 0

	for inst in Institution.objects.all():
		addr = inst.sede.morada
		city = inst.sede.concelho.denominacao

		if inst.sede.geocode != '':
			count += 1

		#query = "{}, {}, PT".format(addr.split(",")[0], city).lower()
		#query = query.replace("n.o", "")
		#query = query.replace("no.", "")

		#g = geocoder.osm(query)
		#inst.sede.geocode = g.json if g.json is not None else ''
		#inst.sede.save()

		#print(query)
		#print(g.json)
		#sleep(1.5)

		print(count)

		if count > 10:
			#break
			pass

	return HttpResponse(out)



def genMapBoxes(request):
	out = ""
	count = 0


	for dist in District.objects.all():
		poly = Poly(dist.poly, 1, False, False)
		box = poly.getBox()

		dist.viewBox = box
		dist.save()

		out += box + "<br>"
		out += str(dist.poly) + "<br><br>"


		count += 1
		print(count)

		if count > 10:
			#break
			pass



	for conc in Council.objects.all():
		poly = Poly(conc.poly, 1, False, False)
		box = poly.getBox()

		conc.viewBox = box
		conc.save()

		out += box + "<br>"
		out += str(conc.poly) + "<br><br>"


		count += 1
		print(count)

		if count > 10:
			#break
			pass



	for freg in Parish.objects.all():
		poly = Poly(freg.poly, 1, False, False)
		box = poly.getBox()

		freg.viewBox = box
		freg.save()

		out += box + "<br>"
		out += str(freg.poly) + "<br><br>"


		count += 1
		print(count)

		if count > 10:
			#break
			pass




	return HttpResponse(out)



def genMaps(request):	
	distMap = ShapeMap(1, 60)
	
	out = ""
	count = 0

	for area in distMap.areas:
		try:
			dist = District.objects.get(dicofre=area.dicofre)
				
			dist.poly = area.getLongestPoly()

			dist.save()

			out += str(dist) + "<br>"
			out += str(dist.poly) + "<br>"

		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		print(str(count))

		if count > 100:
			#break
			pass



	concMap = ShapeMap(2, 40)

	for area in concMap.areas:
		try:
			conc = Council.objects.get(distrito__denominacao=area.dist, denominacao=area.conc)
			conc.poly = area.getLongestPoly()

			conc.save() # only run once! this populates the db

			out += str(conc) + "<br>"
			out += str(conc.poly) + "<br>"

		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		print(str(count))

		if count > 10:
			#break
			pass



	fregMap = ShapeMap(3, 30)

	for area in fregMap.areas:
		try:
			freg = Parish.objects.get(dicofre=area.dicofre)
				
			freg.poly = area.getLongestPoly()

			freg.save()

			out += str(freg) + "<br>"
			out += str(freg.poly) + "<br>"


		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		print(str(count))

		if count > 100:
			#break
			pass



	return HttpResponse(out)
