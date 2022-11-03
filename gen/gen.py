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
		preCoun = preCoun.replace("Azemeis", "Azeméis")
		preCoun = preCoun.replace("Nova Famal", "Nova de Famal")
		preCoun = preCoun.replace("Freix.Espada ... Cinta", "Freixo de Espada à Cinta")
		preCoun = preCoun.replace("Rodão", "Ródão")
		preCoun = preCoun.replace("Reguengos Monsaraz", "Reguengos de Monsaraz")
		preCoun = preCoun.replace("V. Real Sto António", "Vila Real de Santo António")
		preCoun = preCoun.replace("Fig. Castelo Rodrigo", "Figueira de Castelo Rodrigo")
		preCoun = preCoun.replace("Meda", "Mêda")
		preCoun = preCoun.replace("Vila Nova de Foz Coa", "Vila Nova de Foz Côa")
		preCoun = preCoun.replace("Castanheira de Pera", "Castanheira de Pêra")
		preCoun = preCoun.replace("Sobral Monte Agraço", "Sobral de Monte Agraço")
		preCoun = preCoun.replace("Vila Nova Barquinha", "Vila Nova da Barquinha")
		preCoun = preCoun.replace("Vila Nova Cerveira", "Vila Nova de Cerveira")
		preCoun = preCoun.replace("Sta Marta Penaguião", "Santa Marta de Penaguião")
		preCoun = preCoun.replace("São João Pesqueira", "São João da Pesqueira")

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
	#r = Content(pagina='index', tag='evtsDesc', conteudo='Neste espaço pode encontrar eventos concebidos pelas variadas instituições do nosso país. Registe a sua instituição para poder apresentar os seus eventos.')
	#r.save()
	#r = Content(pagina='index', tag='newsTitle', conteudo='NOTÍCIAS EM DESTAQUE')
	#r.save()
	#r = Content(pagina='index', tag='newsDesc', conteudo='Neste espaço pode encontrar notícias relevantes a IPSSs.')
	#r.save()
	#r = Content(pagina='index', tag='vidsTitle', conteudo='VIDEOS EM DESTAQUE')
	#r.save()
	#r = Content(pagina='index', tag='vidsDesc', conteudo='Os melhores vídeos da nossa plataforma IPSS TV.')
	#r.save()
	#r = Content(pagina='about', tag='subtitle', conteudo='A nossa missão')
	#r.save()


	#r = Video(titulo='UNITATE Presentation', texto='UNITATE Presentation (English)', link='https://www.youtube.com/watch?v=sXZls5rdMkk')
	#r.save()
	#r = Video(titulo='Natal 2021 | UNITATE', texto='Natal 2021 | UNITATE', link='https://www.youtube.com/watch?v=Il0KMPqemoU')
	#r.save()
	#r = Video(titulo='Serviço de Apoio Domiciliário para Pessoas com Deficiência | UNITATE', texto='Serviço de Apoio Domiciliário para Pessoas com Deficiência | UNITATE', link='https://www.youtube.com/watch?v=rJOVkCV6sKA')
	#r.save()
	#r = Video(titulo='O nosso Natal 2020 | Unidade de Ação Social da Vendinha', texto='Vídeo de Natal da Unidade de Ação Social da Vendinha da UNITATE "O nosso Natal 2020"', link='https://www.youtube.com/watch?v=ibMhMNqkXDs')
	#r.save()

	#r = Event(titulo='Concerto Comemorativo do 25 de abril – Luís Trigacheiro', texto='No âmbito das comemorações do 25 de abril, Luís Trigacheiro, jovem e consagrado artista alentejano, com uma criação musical dedicada à música tradicional portuguesa, subirá ao palco para realizar um concerto em Vila Viçosa. O evento, terá lugar no dia 25 de abril de 2022, na Praça da República, com início às 17h. Trata-se de um espetáculo musical promovido pela Câmara Municipal de Vila Viçosa que permitirá ao artista, que venceu o “The Voice Portugal”, apresentar alguns dos principais títulos originais do seu repertório, já plenamente consagrados no panorama da música portuguesa e conhecidos do grande público.')
	#r.save()
	#r = Event(titulo='Festival Descobre O Teu Interior – 8 e 9 de Abril (Vila Viçosa) – O primeiro Festival Itinerante pelo Interior de Portugal', texto='Vila Viçosa – 8 e 9 de abril Viva experiências culturais únicas e intimamente ligadas à identidade de Vila Viçosa. Pode assistir ao festival presencialmente ou online! Adquire o teu Bilhetes online (gerador.eu) Escolhe o bilhete que melhor se adequa à experiência que queres viver! 4 Opções Disponíveis! Partilhamos o programa definido para Vila Viçosa aqui A Não Perder!')
	#r.save()
	#r = Event(titulo='Festival Gastronómico “Vila Viçosa à Mesa” – Semana do Borrego – 11 a 17 de Abril', texto='Entre os dias 11 e 17 de abril, decorrerá a Semana Gastronómica do Borrego, na qual os pratos tradicionais elaborados à base de carne de borrego, são um dos símbolos da gastronomia alentejana e da época de Páscoa. Visite-nos nessas datas e encontre nos estabelecimentos de restauração do concelho aderentes uma oferta gastronómica especial, dedicada ao Borrego, e que evidencia o que de melhor há para degustar em Vila Viçosa.')
	#r.save()
	#r = Event(titulo='Variante Bencatel/VilaViçosa- Pré-Apresentação – Dia 31 Março – 10h00', texto='A Câmara Municipal de Vila Viçosa, no próximo dia 31 de março (quinta-feira), irá efetuar uma pré-apresentação onde será disponibilizado o levantamento topográfico da Variante, que ligará Bencatel a Vila Viçosa e que se constitui como um dos principais projetos municipais do atual executivo. Esta introdução irá decorrer no Salão Nobre dos Paços do Concelho, em Vila Viçosa, às 10h00 e espera contar também com a presença da população local. Com transmissão direta via facebook do Município de Vila Viçosa!')
	#r.save()

	#r = NewsReport(titulo='Feira Renascentista em Vila Viçosa: Município abre inscrições para o espaço das tasquinhas e das bancas!', texto='O Município de Vila Viçosa informa que, no âmbito da “Feira de Inspiração Renascentista”, estão abertas as inscrições, até ao dia 15 de maio de 2022, para o espaço das “Tasquinhas”, num total de 8 (oito) e para o espaço das “Bancas”, num total de 14 (catorze). A autarquia informa que, no caso das Tasquinhas, será dada prioridade às associações do Concelho e, no caso das Bancas, aos empresários cuja atividade se enquadre no âmbito da feira. A Câmara Municipal de Vila Viçosa relembra que o espaço das “Tasquinhas” será destinado à comercialização de bebidas e comida e o espaço das “Bancas” estará vocacionado para a venda de artesanato, doçaria, produtos diversos, entre outros, ambos com regulamento próprio. Este evento irá decorrer nos dias 10, 11 e 12 de junho. As inscrições estão disponíveis através do Balcão Único (localizado no edifício da CMVV e no horário: 9h00/12h30 e 14h00/16h30) ou através dos emails: geral@cm-vilavicosa.pt e luis.lourinho.silva@cm-vilavicosa.pt.')
	#r.save()
	#r = NewsReport(titulo='Festas dos Capuchos regressa este ano a Vila Viçosa e já têm data marcada!', texto='Depois de dpois anos de interregno devido á Pandemia de Covid 19, as seculares e tradicionais Festas dos Capuchos estão de regresso a Vila Viçosa. De acordo com o despacho nº14/2022, divulgado na página do Município de Vila Viçosa, as Festas dos Capuchos vão realizar-se a 09,10,11 e 12 de setembro de 2022, no Largo dos Capuchos. Segundo a mesma informação, a abertura do arraial realizar-se-á dia 09 de setembro, pelas 20h30. Há mais de 150 anos que se celebra a Festa dos Capuchos, sob a invocação de Nossa Senhora da Piedade dos Capuchos; com tonalidades diferentes e com ideias diversas de acordo com o espírito do tempo. Mas o que se celebra é sempre o concelho e o reforço dos vínculos e da identidade dos calipolenses. Fonte: Município de Vila Viçosa')
	#r.save()
	#r = NewsReport(titulo='Três toneladas de Carne de bovino apreendidas em Vila Viçosa não cumpriam condições de refrigeração!', texto='A ASAE – Autoridade de Segurança Alimentar e Económica desenvolveu ontem e hoje uma operação a nível nacional, incluindo a Região Alentejo, que incidiu sobretudo na fiscalização do transporte de bens alimentares e não alimentares. Tal como a Rádio Campanário noticiou esta manhã, em Vila Viçosa, no âmbito desta operação, foram apreendidas três toneladas de carne de bovino. A carne era transportada num camião que vinha da zona do Montijo e destinava-se ao abastecimento do concelho de Vila Viçosa e concelhos limítrofes. Segundo a Rádio Campanário conseguiu apurar ao final do dia, as três toneladas de carne de bovino foram apreendidas porque eram transportadas num camião que não cumpria as condições obrigatórias de refrigeração. Tal como a RC noticiou os bens alimentares apreendidos são agora sujeitos a perícia veterinária.')
	#r.save()
	#r = NewsReport(titulo='Vila Viçosa: Dezenas de pessoas acompanharam a recriação da Via Sacra (c/fotos)', texto='Vila Viçosa celebrou esta noite a Via Sacra em tempo de Quaresma, tendo o cortejo religioso dado início no Paço junto ao mercado municipal. Dezenas de pessoas, percorreram o trajeto seguido por Jesus carregando a cruz, do Pretório até o Calvário, com passagem pelas 14 estações desde a primeira estação onde Jesus é condenado à morte atá à última, a décima quarta, onde Jesus é sepultado e ressuscita ao terceiro dia A Via Sacra é um exercício espiritual em que os fiéis revivem a paixão e morte de Jesus, acompanhando o percurso da sua Divina missão Redentora. A Rádio Campanário acompanhou esta celebração e deixa-lhe algumas imagens:')
	#r.save()


	#for e in Institution.objects.all():
		#s = Equipment(institution=e, denominacao=e.denominacao+" - Sede", morada=e.morada, concelho=e.concelho, distrito=e.distrito)
		#out += str(e) + "<br>"
		#out += str(s) + "<br>"
		#s.save()


	return HttpResponse(out)
