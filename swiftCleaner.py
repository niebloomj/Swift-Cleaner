import fileinput
import os
import sys

shouldFixLongLines = False

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
	for file in files:
		if file.endswith(".swift"):

			print(os.path.join(root, file))

			f = open(os.path.join(root, file),'r')
			filedata = f.read()
			f.close()

			newdata = filedata
			newdata = newdata.replace("    ", "\t")
			newdata = newdata.replace("\t\t   ", "\t\t\t")
			newdata = newdata.replace("\n\n\n", "\n\n")
			newdata = newdata.replace("delete this line\n\n", "")
			newdata = newdata.replace("delete this line\n", "")
			newdata = filedata.split("\n")

			for temp in range(len(newdata[14:])):
				x = temp + 14
				if "\t" == newdata[x] or "\t\t" == newdata[x] or "\t\t\t" == newdata[x] or "\t\t\t\t" == newdata[x] or "\t\t\t\t\t" == newdata[x] or "\t\t\t\t\t\t" == newdata[x] or "\t\t\t\t\t\t\t" == newdata[x] or "\t" * 8 == newdata[x] or "\t" * 9 == newdata[x] or "\t" * 10 == newdata[x] or "\t" * 11 == newdata[x]:
					newdata[x] = ""
				if "///" in newdata[x]:
					continue
				elif "//" in newdata[x]:
						if newdata[x-1] != "" and "//" not in newdata[x-1]:
							newdata[x] = "\n" + newdata[x]
						elif newdata[x+1] == "":
							newdata[x+1] = "delete this line"
				if "\tif" in newdata[x]:
					index = newdata[x].find("\tif")
					try:
						if newdata[x][index + 3] != " ":
							newdata[x] = newdata[x][:index + 3] + " " + newdata[x][index + 3:]
					except Exception as e:
						pass
				if "\tif" in newdata[x] and "else" not in newdata[x]:
					if newdata[x-1] != "" and "//" not in newdata[x-1]:
						print(newdata[x-1])
						newdata[x] = "\n"+newdata[x]
				elif "else" in newdata[x]:
					index = newdata[x].find("else")
					try:
						if newdata[x][index - 1] == "}":
							newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
					except Exception as e:
						pass
				charactersToHaveSpacesOnBothSides = [":", ",", "==", "="]
				for character in charactersToHaveSpacesOnBothSides:
					if character in newdata[x]:
						index = newdata[x].find(character)
						while (index != -1):
							if (len(newdata[x]) > index + len(character)):
								if (not (character == "=" and ("==" in newdata[x] or "!=" in newdata[x]))):
									if newdata[x][index + len(character)] != " ":
											newdata[x] = newdata[x][:index + len(character)] + " " + newdata[x][index + len(character):]
									if character != ",":
										if newdata[x][index  - 1] != " ":
											newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
								index = newdata[x].find(character, index + len(character))
							else:
								break
				if "->" in newdata[x]:
					index = newdata[x].find("->")
					try:
						if newdata[x][index - 1] != " ":
							newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
						index = newdata[x].find("->")
						if newdata[x][index + 2] != " ":
							newdata[x] = newdata[x][:index + 2] + " " + newdata[x][index+ 2:]
					except Exception as e:
						pass
				if "{" in newdata[x]:
					index = newdata[x].find("{")
					try:
						if newdata[x][index - 1] != " ":
							newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
					except Exception as e:
						pass
				if (shouldFixLongLines):
					if len(newdata[x]) > 80 and "//" not in newdata[x]:
						if '"' in newdata[x]:
							pass
							# newdata[x] = newdata[x] + " //Line has too many characters says SwiftCleaner"
						elif "," in newdata[x]:
							index = newdata[x].find(",")
							newdata[x] = newdata[x][:index + 1] + "\n" + ("\t" * (newdata[x].count("\t") + 2))  + newdata[x][index + 1:]
						elif "->" in newdata[x]:
							index = newdata[x].find("->")
							newdata[x] = newdata[x][:index - 1] + "\n" + ("\t" * (newdata[x].count("\t") + 2))  + newdata[x][index - 1:]
						elif " = " in newdata[x]:
							index = newdata[x].find("=")
							newdata[x] = newdata[x][:index + 1] + "\n" + ("\t" * (newdata[x].count("\t") + 2))  + newdata[x][index + 1:]
						else:
							pass
							# print("Could not fix line")
							# newdata[x] = newdata[x] + " //Line has too many characters says SwiftCleaner"

			newdata = "\n".join(str(x) for x in newdata)
			newdata = newdata.replace("    ", "\t")
			newdata = newdata.replace("\t\t   ", "\t\t\t")
			newdata = newdata.replace("\n\n\n", "\n\n")
			newdata = newdata.replace("delete this line\n\n", "")
			newdata = newdata.replace("delete this line\n", "")
			# newdata = newdata.replace("\n\n\n", "\n\n")
			# print(newdata)

			f = open(os.path.join(root, file),'w')
			f.write(newdata)
			f.close()