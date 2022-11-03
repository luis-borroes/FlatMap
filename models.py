from django.db import models
from django.urls import reverse
from django.utils.text import slugify



class Division(models.Model):
	denominacao = models.CharField(max_length=400, default='', editable=False)
	dicofre = models.CharField(max_length=10, default='', editable=False)
	poly = models.TextField(default='')
	viewBox = models.CharField(max_length=80, default='')
	slug = models.SlugField(max_length=200, blank=True, null=True)


	class Meta:
		abstract = True	
	

	def __str__(self):
		return self.denominacao + ' - ' + self.dicofre


	def save(self, *args, **kwargs):
		self.slug = slugify(self.denominacao)

		super(Division, self).save(*args, **kwargs)



class District(Division):
	pass



class Council(Division):
	distrito = models.ForeignKey(District, on_delete=models.CASCADE, editable=False)



class Parish(Division):
	concelho = models.ForeignKey(Council, on_delete=models.CASCADE, editable=False)



class Institution(models.Model):
	denominacao = models.CharField(max_length=400, default='')
	sede = models.ForeignKey('Equipment', on_delete=models.CASCADE, null=True)
	juridica = models.CharField(max_length=100, default='')
	ano = models.IntegerField(default=0) # ano de registo
	nipc = models.CharField(max_length=9, default='')
	tags = models.ManyToManyField('Tag')


	def __str__(self):
		return self.denominacao + ' - ' + self.juridica


	def save(self, *args, **kwargs):
		super(Institution, self).save(*args, **kwargs)

		tagStr = self.denominacao + ' '
		tagStr += self.sede.distrito.denominacao + ' '
		tagStr += self.sede.concelho.denominacao + ' '

		if self.sede.freguesia != None:
			tagStr += self.sede.freguesia.denominacao + ' '

		tagStr = tagStr.replace('.', ' ')
		tagStr = tagStr.replace(',', ' ')
		tagStr = tagStr.replace(':', ' ')
		tagStr = tagStr.replace(';', ' ')


		for tagStr in slugify(tagStr).split('-'):
			tag = Tag.objects.get_or_create(name=tagStr)[0]
			tag.save()
			self.tags.add(tag)


	def get_absolute_url(self):
		return reverse("flatmap:dispIPSS", args=[self.id])



class Equipment(models.Model):
	instituicao = models.ForeignKey(Institution, on_delete=models.CASCADE)
	denominacao = models.CharField(max_length=400, default='')
	morada = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
	distrito = models.ForeignKey(District, on_delete=models.CASCADE)
	concelho = models.ForeignKey(Council, on_delete=models.CASCADE)
	freguesia = models.ForeignKey(Parish, on_delete=models.CASCADE, default=None, null=True)
	latitude = models.CharField(max_length=80, default='', blank=True)
	longitude = models.CharField(max_length=80, default='', blank=True)
	geocode = models.TextField(default='', blank=True)
	geocode2 = models.TextField(default='', blank=True)
	geocode3 = models.TextField(default='', blank=True)


	def __str__(self):
		return self.denominacao + ' - ' + str(self.distrito) + ' - ' + str(self.concelho)



class Address(models.Model):
	original = models.CharField(max_length=400, default='')
	arteria = models.CharField(max_length=400, default='', blank=True, null=True)
	porta = models.CharField(max_length=400, default='', blank=True, null=True)
	alojamento = models.CharField(max_length=400, default='', blank=True, null=True)
	localidade = models.CharField(max_length=400, default='', blank=True, null=True)


	def __str__(self):
		items = []

		if self.arteria:
			items.append(self.arteria)

		if self.porta:
			items.append(self.porta)

		if self.alojamento:
			items.append(self.alojamento)

		if self.localidade:
			items.append(self.localidade)


		if not items:
			items.append(self.original)

		return ', '.join(items)



class Tag(models.Model):
	name = models.CharField(max_length=80, default='')


	def __str__(self):
		return self.name



class Content(models.Model):
	pagina = models.CharField(max_length=500, default='')
	tag = models.CharField(max_length=500, default='')
	conteudo = models.TextField(default='', blank=True)


	def __str__(self):
		return self.pagina + ' - ' + self.tag



class Article(models.Model):
	titulo = models.CharField(max_length=500, default='')
	texto = models.TextField(default='', blank=True)
	data = models.DateTimeField(auto_now_add=True)
	invertido = models.BooleanField(default=False)
	imagem = models.ImageField(upload_to='article/%Y/%m/%d', blank=True)
	slug = models.SlugField(max_length=80, blank=True, editable=False)


	class Meta:
		abstract = True	


	def __str__(self):
		return self.titulo + ' - ' + str(self.data)


	def save(self, *args, **kwargs):
		if not self.pk:
			super(Article, self).save(*args, **kwargs)

		dateSlug = self.data.strftime("-%y%m%d")
		self.slug = slugify(self.titulo)[:60] + dateSlug

		super(Article, self).save(*args, **kwargs)



class Event(Article):
	def __str__(self):
		return self.titulo + ' - ' + str(self.data)


	def get_absolute_url(self):
		return reverse("flatmap:evtsDisp", args=[self.slug])



class NewsReport(Article):
	def __str__(self):
		return self.titulo + ' - ' + str(self.data)


	def get_absolute_url(self):
		return reverse("flatmap:newsDisp", args=[self.slug])



class Video(Article):
	link = models.URLField(max_length=400, default='')


	def __str__(self):
		return self.titulo + ' - ' + str(self.data)


	def get_absolute_url(self):
		return reverse("flatmap:vidsDisp", args=[self.slug])
