# storage for (previously) useful database generating bits
# mostly not functional - they are use-once functions kept for reference

def genIPSSDatabase8(request):
	fregMap = shapeMap(3, 20)
	
	out = ""
	count = 0

	fregs = Parish.objects.all()

	for f in fregs:
		f.delete()

	for area in fregMap.areas:
		try:
			freg = Parish.objects.create(
				concelho=Council.objects.get(distrito__denominacao=area.dist,denominacao=area.conc),
				denominacao=area.freg,
				poly=area.getLongestPoly())
			
			out += str(freg) + "<br>"
			out += str(freg.poly) + "<br>"

		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		if count > 100:
			#break
			pass

	count = 0


	return HttpResponse(out)




def genIPSSDatabase7(request):
	distMap = shapeMap(1, 70)
	
	out = ""
	count = 0

	for area in distMap.areas:
		try:
			dist = District.objects.get(denominacao=area.dist)
			dist.poly = area.getLongestPoly()

			#dist.save() # only run once! this populates the db

			out += str(dist) + "<br>"
			out += str(dist.poly) + "<br>"

		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		if count > 10:
			#break
			pass

	count = 0


	concMap = shapeMap(2, 40)

	for area in concMap.areas:
		try:
			conc = Council.objects.get(distrito__denominacao=area.dist, denominacao=area.conc)
			conc.poly = area.getLongestPoly()

			#conc.save() # only run once! this populates the db

			out += str(conc) + "<br>"
			out += str(conc.poly) + "<br>"

		except Exception as e:
			out += str(e) + " - " + str(area) + "<br>"


		count += 1
		if count > 10:
			#break
			pass

	count = 0

	return HttpResponse(out)




def genIPSSDatabase6(request):
	locations = [join(BASE_DIR, 'main', 'csv', 'freguesias-metadata.csv'),]
	

	out = ""
	count = 0

	location = locations[0]
	with open(location, encoding='utf-8') as file:
		rdr = reader(file)

		for row in rdr:
			dist = Parish(concelho=Council.objects.get(distrito__denominacao=row[1], denominacao=row[2]), denominacao=row[3], dicofre=row[4])

			#dist.save() # only run once! this populates the db

			out += str(dist) + "<br>"
			out += str(dist.concelho) + "<br>"
			out += str(dist.concelho.distrito) + "<br>"
			out += str(row) + "<br><br>"

			count += 1
			if count > 10:
				#break
				pass

	count = 0

	return HttpResponse(out)


def genIPSSDatabase5(request):
	outAll = ""
	out = ""
	count = 0
	errCount = 0

	for equip in Equipment.objects.all():
		inst = equip.instituicao
		inst.sede = equip
		#inst.save()



		out = str(equip) + "<br>"

		outAll += out
		out = ""

		count += 1
		if count > 5:
			break
			pass



	return HttpResponse(outAll)



def genIPSSDatabase4(request):
	outAll = ""
	out = ""
	count = 0
	errCount = 0

	for equip in Equipment.objects.all():
		dist = District.objects.get(denominacao=equip.distrito)
		preCoun = equip.concelho.replace("- ", "-")
		preCoun = preCoun.replace("Azemeis", "Azem??is")
		preCoun = preCoun.replace("Nova Famal", "Nova de Famal")
		preCoun = preCoun.replace("Freix.Espada ... Cinta", "Freixo de Espada ?? Cinta")
		preCoun = preCoun.replace("Rod??o", "R??d??o")
		preCoun = preCoun.replace("Reguengos Monsaraz", "Reguengos de Monsaraz")
		preCoun = preCoun.replace("V. Real Sto Ant??nio", "Vila Real de Santo Ant??nio")
		preCoun = preCoun.replace("Fig. Castelo Rodrigo", "Figueira de Castelo Rodrigo")
		preCoun = preCoun.replace("Meda", "M??da")
		preCoun = preCoun.replace("Vila Nova de Foz Coa", "Vila Nova de Foz C??a")
		preCoun = preCoun.replace("Castanheira de Pera", "Castanheira de P??ra")
		preCoun = preCoun.replace("Sobral Monte Agra??o", "Sobral de Monte Agra??o")
		preCoun = preCoun.replace("Vila Nova Barquinha", "Vila Nova da Barquinha")
		preCoun = preCoun.replace("Vila Nova Cerveira", "Vila Nova de Cerveira")
		preCoun = preCoun.replace("Sta Marta Penagui??o", "Santa Marta de Penagui??o")
		preCoun = preCoun.replace("S??o Jo??o Pesqueira", "S??o Jo??o da Pesqueira")

		try:
			coun = Council.objects.get(distrito=dist, denominacao=preCoun)

		except Exception as e:
			coun = e
			errCount += 1


		out = str(equip) + "<br>"
		out += str(equip.distrito) + "<br>"
		out += str(dist) + "<br>"
		out += str(equip.concelho) + "<br>"
		out += str(preCoun) + "<br>"
		out += str(coun) + "<br>"
		out += str(count) + "<br><br>"

		equip.distrito_fk = dist
		equip.concelho_fk = coun
		#equip.save()


		outAll += out
		out = ""

		count += 1
		if count > 5:
			break
			pass


	outAll = str(errCount) + "<br><br>" + outAll


	return HttpResponse(outAll)



def genIPSSDatabase(request):
	locations = [join(BASE_DIR, 'main', 'csv', 'distritos-metadata.csv'),
				join(BASE_DIR, 'main', 'csv', 'concelhos-metadata.csv'),]
	

	out = ""
	count = 0

	location = locations[0]
	with open(location) as file:
		rdr = reader(file)

		for row in rdr:
			dist = District(denominacao=row[2], dicofre=row[1])

			#dist.save() # only run once! this populates the db

			out += str(dist) + "<br>"
			out += str(row) + "<br><br>"

			count += 1
			if count > 0:
				break
				pass

	count = 0

	location = locations[1]
	with open(location) as file:
		rdr = reader(file)

		for row in rdr:
			dist = District.objects.get(dicofre=row[1][:2])
			coun = Council(distrito=dist, denominacao=row[2], dicofre=row[1])

			#coun.save() # only run once! this populates the db

			out += str(dist) + "<br>"
			out += str(coun) + "<br>"
			out += str(row) + "<br><br>"

			count += 1
			if count > 4:
				break
				pass

	count = 0


	#for e in Council.objects.all():
		#s = "d = District.objects.get(dicofre='{}')<br>".format(e.dicofre[:2])
		#s += "r = Council(distrito=d, denominacao='{}', dicofre='{}')<br>r.save()".format(e.denominacao, e.dicofre)
		#out += s + "<br>"


	return HttpResponse(out)



def genIPSSDatabase2(request):
	locations = [join(BASE_DIR, 'main', 'csv', 'tabula-Listagem_ipss.csv'),
				join(BASE_DIR, 'main', 'csv', 'tabula-Listagem_cooperativas.PDF.csv'),
				join(BASE_DIR, 'main', 'csv', 'tabula-Listagem_casas_do_povo.PDF.csv')]
	

	out = ""
	count = 0

	for location in locations:
		with open(location, encoding='utf-8') as file:
			rdr = reader(file)

			for preRow in rdr:
				row = [item.replace('\n', ' ') for item in preRow] # remove newline characters

				inst = Institution(denominacao=row[0], morada=row[1],
					concelho=row[2], distrito=row[3],
					juridica=row[4], ano=row[5],
					nipc=row[6])

				#inst.save() # only run once! this populates the db

				#out += str(inst) + "<br>"
				#out += str(preRow) + "<br>"
				#out += str(row) + "<br><br>"

				count += 1
				if count > 6:
					break
					pass

		count = 0


	# hacks for populating db and fixing problems caused by said hacks

	#for e in Video.objects.order_by('data'):
		#r = Video(titulo=e.titulo, texto=e.texto, link=e.link)
		#out += str(r) + "<br>"
		#r.save()
		#e.delete()

	#for e in Video.objects.order_by('data'):
		#s = "r = Video(titulo='{}', texto='{}', link='{}')<br>r.save()".format(e.titulo, e.texto, e.link)
		#out += s + "<br>"
		#e.save()

	#for e in Event.objects.order_by('data'):
		#s = "r = Event(titulo='{}', texto='{}')<br>r.save()".format(e.titulo, e.texto)
		#out += s + "<br>"
		#e.save()

	#for e in NewsReport.objects.order_by('data'):
		#s = "r = NewsReport(titulo='{}', texto='{}')<br>r.save()".format(e.titulo, e.texto)
		#out += s + "<br>"
		#e.save()

	#for e in Content.objects.all():
		#s = "r = Content(pagina='{}', tag='{}', conteudo='{}')<br>r.save()".format(e.pagina, e.tag, e.conteudo)
		#out += s + "<br>"
		#e.save()

	#r = Content(pagina='index', tag='evtsTitle', conteudo='EVENTOS EM DESTAQUE')
	#r.save()
	#r = Content(pagina='index', tag='evtsDesc', conteudo='Neste espa??o pode encontrar eventos concebidos pelas variadas institui????es do nosso pa??s. Registe a sua institui????o para poder apresentar os seus eventos.')
	#r.save()
	#r = Content(pagina='index', tag='newsTitle', conteudo='NOT??CIAS EM DESTAQUE')
	#r.save()
	#r = Content(pagina='index', tag='newsDesc', conteudo='Neste espa??o pode encontrar not??cias relevantes a IPSSs.')
	#r.save()
	#r = Content(pagina='index', tag='vidsTitle', conteudo='VIDEOS EM DESTAQUE')
	#r.save()
	#r = Content(pagina='index', tag='vidsDesc', conteudo='Os melhores v??deos da nossa plataforma IPSS TV.')
	#r.save()
	#r = Content(pagina='about', tag='subtitle', conteudo='A nossa miss??o')
	#r.save()


	#r = Video(titulo='UNITATE Presentation', texto='UNITATE Presentation (English)', link='https://www.youtube.com/watch?v=sXZls5rdMkk')
	#r.save()
	#r = Video(titulo='Natal 2021 | UNITATE', texto='Natal 2021 | UNITATE', link='https://www.youtube.com/watch?v=Il0KMPqemoU')
	#r.save()
	#r = Video(titulo='Servi??o de Apoio Domicili??rio para Pessoas com Defici??ncia | UNITATE', texto='Servi??o de Apoio Domicili??rio para Pessoas com Defici??ncia | UNITATE', link='https://www.youtube.com/watch?v=rJOVkCV6sKA')
	#r.save()
	#r = Video(titulo='O nosso Natal 2020 | Unidade de A????o Social da Vendinha', texto='V??deo de Natal da Unidade de A????o Social da Vendinha da UNITATE "O nosso Natal 2020"', link='https://www.youtube.com/watch?v=ibMhMNqkXDs')
	#r.save()

	#r = Event(titulo='Concerto Comemorativo do 25 de abril ??? Lu??s Trigacheiro', texto='No ??mbito das comemora????es do 25 de abril, Lu??s Trigacheiro, jovem e consagrado artista alentejano, com uma cria????o musical dedicada ?? m??sica tradicional portuguesa, subir?? ao palco para realizar um concerto em Vila Vi??osa. O evento, ter?? lugar no dia 25 de abril de 2022, na Pra??a da Rep??blica, com in??cio ??s 17h. Trata-se de um espet??culo musical promovido pela C??mara Municipal de Vila Vi??osa que permitir?? ao artista, que venceu o ???The Voice Portugal???, apresentar alguns dos principais t??tulos originais do seu repert??rio, j?? plenamente consagrados no panorama da m??sica portuguesa e conhecidos do grande p??blico.')
	#r.save()
	#r = Event(titulo='Festival Descobre O Teu Interior ??? 8 e 9 de Abril (Vila Vi??osa) ??? O primeiro Festival Itinerante pelo Interior de Portugal', texto='Vila Vi??osa ??? 8 e 9 de abril Viva experi??ncias culturais ??nicas e intimamente ligadas ?? identidade de Vila Vi??osa. Pode assistir ao festival presencialmente ou online! Adquire o teu Bilhetes online (gerador.eu) Escolhe o bilhete que melhor se adequa ?? experi??ncia que queres viver! 4 Op????es Dispon??veis! Partilhamos o programa definido para Vila Vi??osa aqui A N??o Perder!')
	#r.save()
	#r = Event(titulo='Festival Gastron??mico ???Vila Vi??osa ?? Mesa??? ??? Semana do Borrego ??? 11 a 17 de Abril', texto='Entre os dias 11 e 17 de abril, decorrer?? a Semana Gastron??mica do Borrego, na qual os pratos tradicionais elaborados ?? base de carne de borrego, s??o um dos s??mbolos da gastronomia alentejana e da ??poca de P??scoa. Visite-nos nessas datas e encontre nos estabelecimentos de restaura????o do concelho aderentes uma oferta gastron??mica especial, dedicada ao Borrego, e que evidencia o que de melhor h?? para degustar em Vila Vi??osa.')
	#r.save()
	#r = Event(titulo='Variante Bencatel/VilaVi??osa- Pr??-Apresenta????o ??? Dia 31 Mar??o ??? 10h00', texto='A C??mara Municipal de Vila Vi??osa, no pr??ximo dia 31 de mar??o (quinta-feira), ir?? efetuar uma pr??-apresenta????o onde ser?? disponibilizado o levantamento topogr??fico da Variante, que ligar?? Bencatel a Vila Vi??osa e que se constitui como um dos principais projetos municipais do atual executivo. Esta introdu????o ir?? decorrer no Sal??o Nobre dos Pa??os do Concelho, em Vila Vi??osa, ??s 10h00 e espera contar tamb??m com a presen??a da popula????o local. Com transmiss??o direta via facebook do Munic??pio de Vila Vi??osa!')
	#r.save()

	#r = NewsReport(titulo='Feira Renascentista em Vila Vi??osa: Munic??pio abre inscri????es para o espa??o das tasquinhas e das bancas!', texto='O Munic??pio de Vila Vi??osa informa que, no ??mbito da ???Feira de Inspira????o Renascentista???, est??o abertas as inscri????es, at?? ao dia 15 de maio de 2022, para o espa??o das ???Tasquinhas???, num total de 8 (oito) e para o espa??o das ???Bancas???, num total de 14 (catorze). A autarquia informa que, no caso das Tasquinhas, ser?? dada prioridade ??s associa????es do Concelho e, no caso das Bancas, aos empres??rios cuja atividade se enquadre no ??mbito da feira. A C??mara Municipal de Vila Vi??osa relembra que o espa??o das ???Tasquinhas??? ser?? destinado ?? comercializa????o de bebidas e comida e o espa??o das ???Bancas??? estar?? vocacionado para a venda de artesanato, do??aria, produtos diversos, entre outros, ambos com regulamento pr??prio. Este evento ir?? decorrer nos dias 10, 11 e 12 de junho. As inscri????es est??o dispon??veis atrav??s do Balc??o ??nico (localizado no edif??cio da CMVV e no hor??rio: 9h00/12h30 e 14h00/16h30) ou atrav??s dos emails: geral@cm-vilavicosa.pt e luis.lourinho.silva@cm-vilavicosa.pt.')
	#r.save()
	#r = NewsReport(titulo='Festas dos Capuchos regressa este ano a Vila Vi??osa e j?? t??m data marcada!', texto='Depois de dpois anos de interregno devido ?? Pandemia de Covid 19, as seculares e tradicionais Festas dos Capuchos est??o de regresso a Vila Vi??osa. De acordo com o despacho n??14/2022, divulgado na p??gina do Munic??pio de Vila Vi??osa, as Festas dos Capuchos v??o realizar-se a 09,10,11 e 12 de setembro de 2022, no Largo dos Capuchos. Segundo a mesma informa????o, a abertura do arraial realizar-se-?? dia 09 de setembro, pelas 20h30. H?? mais de 150 anos que se celebra a Festa dos Capuchos, sob a invoca????o de Nossa Senhora da Piedade dos Capuchos; com tonalidades diferentes e com ideias diversas de acordo com o esp??rito do tempo. Mas o que se celebra ?? sempre o concelho e o refor??o dos v??nculos e da identidade dos calipolenses. Fonte: Munic??pio de Vila Vi??osa')
	#r.save()
	#r = NewsReport(titulo='Tr??s toneladas de Carne de bovino apreendidas em Vila Vi??osa n??o cumpriam condi????es de refrigera????o!', texto='A ASAE ??? Autoridade de Seguran??a Alimentar e Econ??mica desenvolveu ontem e hoje uma opera????o a n??vel nacional, incluindo a Regi??o Alentejo, que incidiu sobretudo na fiscaliza????o do transporte de bens alimentares e n??o alimentares. Tal como a R??dio Campan??rio noticiou esta manh??, em Vila Vi??osa, no ??mbito desta opera????o, foram apreendidas tr??s toneladas de carne de bovino. A carne era transportada num cami??o que vinha da zona do Montijo e destinava-se ao abastecimento do concelho de Vila Vi??osa e concelhos lim??trofes. Segundo a R??dio Campan??rio conseguiu apurar ao final do dia, as tr??s toneladas de carne de bovino foram apreendidas porque eram transportadas num cami??o que n??o cumpria as condi????es obrigat??rias de refrigera????o. Tal como a RC noticiou os bens alimentares apreendidos s??o agora sujeitos a per??cia veterin??ria.')
	#r.save()
	#r = NewsReport(titulo='Vila Vi??osa: Dezenas de pessoas acompanharam a recria????o da Via Sacra (c/fotos)', texto='Vila Vi??osa celebrou esta noite a Via Sacra em tempo de Quaresma, tendo o cortejo religioso dado in??cio no Pa??o junto ao mercado municipal. Dezenas de pessoas, percorreram o trajeto seguido por Jesus carregando a cruz, do Pret??rio at?? o Calv??rio, com passagem pelas 14 esta????es desde a primeira esta????o onde Jesus ?? condenado ?? morte at?? ?? ??ltima, a d??cima quarta, onde Jesus ?? sepultado e ressuscita ao terceiro dia A Via Sacra ?? um exerc??cio espiritual em que os fi??is revivem a paix??o e morte de Jesus, acompanhando o percurso da sua Divina miss??o Redentora. A R??dio Campan??rio acompanhou esta celebra????o e deixa-lhe algumas imagens:')
	#r.save()


	#for e in Institution.objects.all():
		#s = Equipment(institution=e, denominacao=e.denominacao+" - Sede", morada=e.morada, concelho=e.concelho, distrito=e.distrito)
		#out += str(e) + "<br>"
		#out += str(s) + "<br>"
		#s.save()


	return HttpResponse(out)
