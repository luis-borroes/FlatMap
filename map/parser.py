from xml.etree import ElementTree as ET
from luis.settings import BASE_DIR
from os.path import join
from random import random




class Point:

	def __init__(self, rawString, rand = False, stretchFlip = True):
		split = rawString.split(",")

		self.x = split[0]
		self.y = split[1]

		self.xf = float(self.x)
		self.yf = float(self.y)

		if rand:
			self.xf = self.xf + (random() - 0.5) * 0.001
			self.yf = self.yf + (random() - 0.5) * 0.001

		if stretchFlip:
			self.yf = self.yf * -1.2 # stretch map vertically and flip


		self.x = "{:.4f}".format(self.xf)
		self.y = "{:.4f}".format(self.yf)




	def __str__(self):
		return "({}, {})".format(self.x, self.y)




class Poly:
	MIN_POINTS = 150

	def __init__(self, rawPoints, reduceBy = 1, rand = True, stretchFlip = True):
		self.rawPoints = rawPoints
		self.points = []
		self.reducedPoints = []

		self.parsePoints(rand, stretchFlip)

		if reduceBy > 1:
			self.reducePoints(reduceBy)


	def __len__(self):
		return len(self.points)


	def __str__(self):
		return self.polyLine()



	def parsePoints(self, rand, stretchFlip):
		split = self.rawPoints.split()

		for i in split:
			self.points.append(Point(i, rand, stretchFlip))



	def reducePoints(self, step):
		""" Limits number of points on polygon by only taking a point every "step" points (e.g. every 200 points)"""
		count = 0

		if len(self.points) < Poly.MIN_POINTS * step:
			step = int(len(self.points) / Poly.MIN_POINTS)

			if step < 1:
				self.reducedPoints = self.points
				return

		for i in self.points:
			count += 1

			if count == step:
				self.reducedPoints.append(i)

				count = 0


	def joinReduced(self):
		out = ""

		for i in self.reducedPoints:
			out += i.x + "," + i.y + " "

		return out


	def polyLine(self):
		return "		<polygon class='fill-cyan-500 hover:fill-cyan-700' points='" + self.joinReduced() + "'/>"



	def getBox(self, reduced = False):
		pointSet = self.reducedPoints if reduced else self.points

		if len(pointSet) == 0:
			return "0 0 0 0"

		minX = pointSet[0].xf
		minY = pointSet[0].yf
		maxX = minX
		maxY = minY
		width = 0
		height = 0

		for i in pointSet:
			if i.xf < minX:
				minX = i.xf
			
			elif i.xf > maxX:
				maxX = i.xf

			if i.yf < minY:
				minY = i.yf

			elif i.yf > maxY:
				maxY = i.yf

		width = maxX - minX
		height = maxY - minY


		padX = width/20
		padY = height/20
		pad = min(padX, padY)

		minX -= pad
		width += pad * 2

		minY -= pad
		height += pad * 2


		out = "{:.4f} {:.4f} {:.4f} {:.4f}".format(minX, minY, width, height)

		return out




class Area:

	def __init__(self, dicofre, dist, conc = "", freg = ""):
		self.dicofre = dicofre
		self.dist = dist
		self.conc = conc
		self.freg = freg
		self.polys = []


	def __str__(self):
		return self.dist + self.conc + self.freg + self.dicofre


	def addPoly(self, poly):
		self.polys.append(poly)


	def printPolys(self):
		for poly in self.polys:
			print(poly)


	def printLongestPoly(self):
		maxPoly = None
		maxLen = 0

		for poly in self.polys:
			if len(poly) > maxLen:
				maxPoly = poly
				maxLen = len(poly)

		print(maxPoly)


	def getLongestPoly(self):
		maxPoly = None
		maxLen = 0

		for poly in self.polys:
			if len(poly) > maxLen:
				maxPoly = poly
				maxLen = len(poly)

		return maxPoly.joinReduced()



class ShapeMap:

	def __init__(self, level, reduceBy):
		assert(level in range(1, 4))

		self.level = level

		if level != 3:
			files = [join(BASE_DIR, 'main', 'map', 'gadm40_PRT_{}.kml'.format(level))]

		else:
			files = [join(BASE_DIR, 'main', 'map', 'gadm40_PRT_{}_1.kml'.format(level)),
					join(BASE_DIR, 'main', 'map', 'gadm40_PRT_{}_2.kml'.format(level))]

		self.trees = [ET.parse(file) for file in files]
		self.roots = [tree.getroot() for tree in self.trees]

		self.areas = []
		self.areaCache = {}
		self.reduceBy = reduceBy


		self.extract()


	def extract(self):
		name = ""
		area = None
		poly = Poly("0,0")
		rawPoints = ""


		dicofreIndex = 6
		distIndex = 1
		concIndex = -1
		fregIndex = -1

		if self.level == 2:
			dicofreIndex = 8
			distIndex = 0
			concIndex = 3

		if self.level == 3:
			dicofreIndex = 0
			distIndex = 3
			concIndex = 2
			fregIndex = 1


		for root in self.roots:
			# every placemark in kml/document/folder
			for placemark in root[0][1][1:]:

				for el in placemark:
					if el.tag == "{http://www.opengis.net/kml/2.2}ExtendedData":


						dicofre = el[0][dicofreIndex].text


						if dicofre is None:
							dicofre = "None"

						if dicofre in self.areaCache:
							area = self.areas[self.areaCache[dicofre]]


						else:
							self.areaCache[dicofre] = len(self.areas)
							dist = el[0][distIndex].text

							if self.level == 1:
								area = Area(dicofre, dist)

							elif self.level == 2:
								conc = el[0][concIndex].text
								area = Area(dicofre, dist, conc)

							elif self.level == 3:
								conc = el[0][concIndex].text
								freg = el[0][fregIndex].text
								area = Area(dicofre, dist, conc, freg)

							self.areas.append(area)



					if el.tag == "{http://www.opengis.net/kml/2.2}MultiGeometry":
						for poly in el:
							rawPoints = poly[0][0][0].text
							poly = Poly(rawPoints, self.reduceBy)

							self.areas[self.areaCache[dicofre]].addPoly(poly)



					if self.level == 3 and el.tag == "{http://www.opengis.net/kml/2.2}Polygon":
						rawPoints = el[0][0][0].text
						poly = Poly(rawPoints, self.reduceBy)

						self.areas[self.areaCache[dicofre]].addPoly(poly)







if __name__ == "__main__":
	districts = ShapeMap("gadm40_PRT_1.kml", 1)

	for area in districts.areas:
		#print(area)
		#print(len(area.polys))

		area.printLongestPoly()
