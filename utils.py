from django.shortcuts import render
from datetime import datetime
from .models import Content


def getCont(pagina):
	"""Generates a dictionary with the page content from the DB to be used in the template"""
		
	contQuery = Content.objects.filter(pagina=pagina)
	cont = {}

	for item in contQuery:
		cont[item.tag] = item.conteudo

	return cont



def xRender(request, template, context, sideBar = ""):
	"""Hijacks the render function to highlight the current selected 
	navbar, de-cache the css file, etc"""

	context['sideBar'] = sideBar
	context['staticCache'] = datetime.now().strftime("%y%d%m%H%M")

	return render(request, template, context)
