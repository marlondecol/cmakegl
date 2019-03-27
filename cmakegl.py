"""

 ██████╗███╗   ███╗ █████╗ ██╗  ██╗███████╗ ██████╗ ██╗
██╔════╝████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔════╝ ██║
██║     ██╔████╔██║███████║█████╔╝ █████╗  ██║  ███╗██║
██║     ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██║   ██║██║
╚██████╗██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗╚██████╔╝███████╗
 ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝

CMakeGL.py

Pasta do arquivo CMakeLists.txt
Pasta dos arquivos de construção do CMake
Pasta do projeto a ser construído

Desenvolvido por Marlon Luís de Col
Engenharia de Computação
2019 UNOESC Chapecó

"""

import os
from pathlib import Path
from sys import _getframe as gf

def clearScreen():
	os.system("cls" if os.name == "nt" else "clear")

def readFile(mustBeName = ""):
	clearScreen()

	if mustBeName == "":
		print("\n  É necessário definir o nome do arquivo a ser encontrado na função {}, linha {}\n".format(gf().f_code.co_name, gf().f_lineno))
		exit()

	filePath = input("\n  Informe onde está o arquivo {}: ".format(mustBeName))
	fileName = filePath + "/" + mustBeName
	
	if not os.path.exists(fileName):
		input("\n  O arquivo {} não foi encontrado nesta pasta!")
		return readFile(mustBeName)
	
	return open(fileName, "w")

"""

alfabeto = list(input("\nQual é o alfabeto? (separe cada caractere por espaço único) ").split(' '))

prefixo = input("\nQual prefixo deseja utilizar em seus estados? ")
qtEstados = int(input("\nQuantos estados serão computados? "))
inicio = int(input("Qual é o estado inicial? "))
finais = list(map(int, input("Quais são os estados finais? (separe-os por espaço único) ").split(' ')))

estados = []

print("\nInsira as transições abaixo, separadas por espaço único e com um hífen caso não haja destino.\n")

for i in range(qtEstados):
	estados.append(input().split(' '))

esperadas = len(estados) * len(alfabeto)
transitions = 0
efetivadas = 0
vazios = 0

f = criarArquivo(input("\nQue nome quer dar ao arquivo do JFLAP? (se houver um arquivo com o mesmo nome, ele não será substituído) "))

f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><!--Created with AutoFLAP for JFLAP!--><structure>\n")
f.write("\t<type>fa</type>\n")
f.write("\t<automaton>\n")

for i in range(len(estados)):
	f.write("\t\t<state id=\"{}\" name=\"{}{}\">\n".format(i, prefixo, i))

	theta = float(2 * math.pi * float(i) / float(len(estados)))
	raio = float(qtEstados * 20)

	f.write("\t\t\t<x>{:.1f}</x>\n".format(float(raio * math.cos(theta) + raio + 128)))
	f.write("\t\t\t<y>{:.1f}</y>\n".format(float(raio * math.sin(theta) + raio + 128)))

	if i == inicio:
		f.write("\t\t<initial/>\n")
	elif i in finais:
		f.write("\t\t<final/>\n")

	f.write("\t\t</state>\n")

f.write("\t\t<!--The list of transitions.-->\n")

for i in range(len(estados)):
	for j in range(len(estados[i])):
		transitions = transitions + 1

		if estados[i][j] == "-":
			vazios = vazios + 1
			continue

		efetivadas = efetivadas + 1

		f.write("\t\t<transition>\n")
		f.write("\t\t\t<from>{}</from>\n".format(i))
		f.write("\t\t\t<to>{}</to>\n".format(estados[i][j].replace(prefixo, "")))
		f.write("\t\t\t<read>{}</read>\n".format(alfabeto[j]))
		f.write("\t\t</transition>\n")

f.write("\t</automaton>\n")
f.write("</structure>")

print("\nO arquivo \"" + f.name + "\" foi criado com sucesso!")

print("\nEram esperadas {} transições.".format(esperadas))
print("Foram encontradas {} transições.".format(transitions))
print("Destas, {} transições não tinham destino.".format(vazios))
print("Ao todo, {} foram efetivadas.\n".format(efetivadas))

"""

f = readFile("CMakeLists.txt")

for line in f.readlines():
	print(line, end='')