import re

class AddressRegex:

	def __init__(self):
		streetCommaNumber = r'([a-z0-9àáãâéêíóõôúçºª \.\-\(\)]+?) ?, ?(n\.o|no)?\.? ?([0-9]+ ?(a|e) ?[0-9/]+|[0-9/]+|s/n) ?(,|-)? ?(.*)'
		self.streetCommaNumberExp = re.compile(streetCommaNumber, re.IGNORECASE)

		streetNumber = r'([a-z0-9àáãâéêíóõôúçºª \.\-\(\)]+?) ?, ?(n\.o|no)?\.? ?([0-9]+ ?(a|e) ?[0-9/]+|[0-9/]+|s/n) ?(,|-)? ?(.*)'
		self.streetNumberExp = re.compile(streetCommaNumber, re.IGNORECASE)

		textDash = r'([a-z0-9àáãâéêíóõôúçºª \.\-\(\)]+?) ?- ?(.*)'
		self.textDashExp = re.compile(textDash, re.IGNORECASE)
		
		self.commaExp = re.compile(r'.*,.*', re.IGNORECASE)
		self.numberExp = re.compile(r'.*([0-9]+|s/n\.?o?|s\.n\.?o?).*', re.IGNORECASE)
		self.numberDashExp = re.compile(r'.*[0-9]+\-[0-9]+.*', re.IGNORECASE)


	def parse(self, addresses):
		out = ""
		count = 0

		for address in addresses:
			original = address.original

			match = self.streetCommaNumberExp.match(original)
			strNumMatch = self.streetNumberExp.match(original)
			textDashMatch = self.textDashExp.match(original)

			hasComma = self.commaExp.match(original)
			hasNumber = self.numberExp.match(original)
			hasNumberDash = self.numberDashExp.match(original)



			#if hasNumber and not hasComma:
				#out += str(count) + " - " + textDashMatch.group() + " # " + textDashMatch.group(1) + " # " + textDashMatch.group(2) + "<br>"
				#out += str(count) + " - " + original + "<br><br>"
				#count += 1

				#if textDashMatch.group(4) == "Rios":
				#	address.arteria = "Quinta de Abôl"
				#	address.localidade = "Eja (Entre-os-Rios)"
				#	address.save()

				#address.arteria = original
				#address.porta = textDashMatch.group(2)
				#address.alojamento = textDashMatch.group(2)
				#address.localidade = textDashMatch.group(2)
				#address.save()


			#if not hasNumber and not hasComma:
				#out += str(count) + " - " + hasNumber.group() + "<br>"
				#out += str(count) + " - " + original + "<br>"
				#count += 1



			out += str(count) + " - " + str(address) + "<br>"
			out += str(count) + " - " + original + "<br><br>"
			count += 1


			print(count)


		return out
