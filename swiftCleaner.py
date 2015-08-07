import fileinput
import os
import sys
import copy

shouldFixLongLines = False

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
	for file in files:
		if file.endswith(".swift"):

			print(os.path.join(root, file))

			f = open(os.path.join(root, file),'r')
			filedata = f.read()
			f.close()

			newdata = filedata
			# newdata = newdata.replace("    ", "\t")
			newdata = newdata.replace("\t\t   ", "\t\t\t")
			newdata = newdata.replace("\n\n\n", "\n\n")
			newdata = newdata.replace("delete this line\n\n", "")
			newdata = newdata.replace("delete this line\n", "")
			newdata = filedata.split("\n")

			for temp in range(len(newdata[14:])):
				# This is explain below more. Maybe we should start implementing this.
				# newdata[x] = " ".join(newdata[x].split())
				x = temp + 14
				if "\t" == newdata[x] or "\t\t" == newdata[x] or "\t\t\t" == newdata[x] or "\t\t\t\t" == newdata[x] or "\t\t\t\t\t" == newdata[x] or "\t\t\t\t\t\t" == newdata[x] or "\t\t\t\t\t\t\t" == newdata[x] or "\t" * 8 == newdata[x] or "\t" * 9 == newdata[x] or "\t" * 10 == newdata[x] or "\t" * 11 == newdata[x]:
					newdata[x] = ""
				if "*" in newdata[x]:
					continue
				if "///" in newdata[x]:
					continue
				elif "//" in newdata[x]:
						if newdata[x-1] != "" and "//" not in newdata[x-1]:
							newdata[x] = "\n" + newdata[x]
						elif newdata[x+1] == "":
							newdata[x+1] = "delete this line"
				if "//" in newdata[x]:
					continue
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

				#There appear to be some cases where this does not work. i think it is
				#when there are no spaces on either side. I am not sure yet.
				charactersToHaveSpacesOnBothSides = [":", ",", "->", "==", "+=", "-=", ">=", "<=", "="]
				for character in charactersToHaveSpacesOnBothSides:
					if character in newdata[x]:
						index = newdata[x].find(character)
						while (index != -1):
							if (len(newdata[x]) > index + len(character)):
								if (not (character == "=" and ("==" in newdata[x] or "!=" in newdata[x] or "+=" in newdata[x] or "-=" in newdata[x] or "<=" in newdata[x] or ">=" in newdata[x]))):
									#Is Next Space
									if newdata[x][index + len(character)] != " " and newdata[x][index + len(character)] != "\t":
										newdata[x] = newdata[x][:index + len(character)] + " " + newdata[x][index + len(character):]
									#Is Previous Space
									if character != ",":
										if newdata[x][index  - 1] != " " and newdata[x][index  - 1] != "\t":
											newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
								index = newdata[x].find(character, index + len(character) + 1)
							else:
								break
				if "{" in newdata[x]:
					index = newdata[x].find("{")
					try:
						if newdata[x][index - 1] != " ":
							newdata[x] = newdata[x][:index] + " " + newdata[x][index:]
					except Exception as e:
						pass

				#this appears to work in 90% of the cases. in some cases, this just
				#will keep adding white space on every single run
				#I believe a viable fix will be to start this off after the initial tabs
				#and then call " ".join(theline.split()) so we can remove any types of
				#whitespace. Maybe this tactic should be done for each line at the top
				#and apply to every single part of this script.
				numberOfLinesToAlign = 1
				charactersToAlignAt = [":", "="]
				for chatacter in charactersToAlignAt:
					if chatacter in newdata[x] and "==" not in newdata[x]:
						index = newdata[x].find(chatacter)
						lineNums = [(x, index)]
						y = copy.deepcopy(x)
						while (True):
							y -= 1
							if ("==" not in newdata[y]):
								index = newdata[y].find(chatacter)
							else:
								break
							if index == -1:
								break
							lineNums.append((y, index))
						if (len(lineNums) > 1):
							print(lineNums)
							greatest = -1
							for line in lineNums:
								if line[1] > greatest:
									greatest = line[1]
							for line in lineNums:
								if line[1] < greatest:
									diff = greatest - line[1]
									if diff < 15:
										newdata[line[0]] = newdata[line[0]][:line[1] - 1] + (" "*diff) + newdata[line[0]][line[1] - 1:]




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
			# newdata = newdata.replace("    ", "\t")
			newdata = newdata.replace("\t\t   ", "\t\t\t")
			newdata = newdata.replace("\n\n\n", "\n\n")
			newdata = newdata.replace("delete this line\n\n", "")
			newdata = newdata.replace("delete this line\n", "")
			# newdata = newdata.replace("\n\n\n", "\n\n")
			# print(newdata)

			f = open(os.path.join(root, file),'w')
			f.write(newdata)
			f.close()
