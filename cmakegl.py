# /home/zorn/Trabalhos/Engenharia de Computação/Matérias/Computação Gráfica II/Exercícios/opengl
# ../../Trabalhos/Engenharia de Computação/Matérias/Computação Gráfica II/Exercícios/opengl

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

import itertools, os, time
from pathlib import Path
from subprocess import Popen, PIPE, SubprocessError
from sys import stdout, _getframe as gf
from threading import Thread

# Limpa a tela executando o comando específico do sistema operacional.
def clearScreen():
	os.system("cls" if os.name == "nt" else "clear")

# Lista todos os arquivos dentro de uma pasta, recursivamente.
def fileTree(path):
	tree = []

	scan = sorted(os.scandir(path), key=lambda x: (x.is_file(), x.name.lower()))

	for entry in scan:
		if entry.is_dir():
			filesInside = fileTree("{}/{}".format(path, entry.name.strip()))

			for file in filesInside:
				tree.append("{}/{}".format(entry.name.strip(), file))
		else:
			tree.append(entry.name.strip())
	
	return tree

# Lista as pastas existentes dentro de um diretório.
def scanDir(path):
	# Inicializa a variável da lista.
	folders = []

	# Para cada entrada que há no diretório,
	# certifica-se de que é uma pasta e não um arquivo,
	# aplica um strip no nome e adiciona-o na lista.
	for entry in os.scandir(path):
		if entry.is_dir():
			folders.append(entry.name.strip())
	
	# Retorna a lista com as pastas.
	return folders

# Gera uma animação de feedback enquanto executa um subprocesso.
def rotatePipe():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if processDone:
            break

        stdout.write("\r  " + c)
        stdout.flush()

		# Delay de transição dos caracteres.
        time.sleep(0.125)

    stdout.write("")

clearScreen()

print("\n   ██████╗███╗   ███╗ █████╗ ██╗  ██╗███████╗ ██████╗ ██╗")
print("  ██╔════╝████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔════╝ ██║")
print("  ██║     ██╔████╔██║███████║█████╔╝ █████╗  ██║  ███╗██║")
print("  ██║     ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██║   ██║██║")
print("  ╚██████╗██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗╚██████╔╝███████╗")
print("   ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝")

print("\n  Bem-vindo ao CMakeGL!")

print("\n  Este programa executa todos os procedimentos para a criação do seu projeto OpenGL")
print("  Utiliza as dependências necessárias, constrói os arquivos e compila tudo, tendo como base os tutoriais do opengl-tutorial.org")
print("\n  Antes de iniciar tenha certeza que a pasta do seu projeto já está no diretório dos arquivos OpenGL (onde está o arquivo CMakeLists.txt)!")

# Como o programa funciona apenas em ambiente Linux,
# verifica o S.O. atual e finaliza o programa caso não cumpra esta condição.
if os.name.lower() != "posix":
	print("\n  Infelizmente, o programa funciona apenas em sistemas Linux! :(")
	exit()

input("\n  Pressione [ENTER] para começar!")

# Espera por um diretório que contenha o arquivo CMakeLists.txt do CMake.
# Se o diretório informado não contém este arquivo,
# faz o pedido novamente, até que seja encontrado.
# A variável com o diretório informado será utilizado
# como base para o resto do programa também.
while True:
	# Limpa a tela a cada pedido.
	clearScreen()

	print("\n  Onde está localizado o arquivo CMakeLists.txt?")
	print("  Caminhos relativos ao atual são válidos.\n")

	# Diretório que contém o arquivo CMakeLists.txt.
	cmakelistsPath = input("  Informe o local: ")

	# Se o caminho não for informado.
	if not cmakelistsPath:
		input("\n  Caminho inválido! Pressione [ENTER] e tente novamente.")
		continue
	
	# Se o caminho não for absoluto.
	if cmakelistsPath[0] != "/":
		cmakelistsPath = "{}/{}".format(os.getcwd(), cmakelistsPath)
	
	# Verifica se a pasta existe.
	if not os.path.exists(cmakelistsPath):
		input("\n  O caminho informado não existe! Pressione [ENTER] e tente novamente.")
		continue
	
	# Armazena o caminho do arquivo CMakeLists.txt.
	cmakelistsFile = "{}/CMakeLists.txt".format(cmakelistsPath)

	# Verifica se o arquivo foi encontrado.
	if not os.path.exists(cmakelistsFile):
		input("\n  Não foi encontado o arquivo CMakeLists.txt neste diretório! Pressione [ENTER] e tente novamente.")
	else:
		break

# Nesta etapa do programa, devem ser listadas pastas existente dentro do diretório informado.
# Isto serve para que o programa liste, depois de excluir as pastas padrão dos arquivos OpenGL,
# apenas os projetos disponíveis para serem construídos pelo CMake.
while True:
	# Pastas existentes no diretório.
	folders = scanDir(cmakelistsPath)

	for folder in folders:
		if folder[0] == ".":
			folders.remove(folder)

	folders.sort()

	# Separa o texto inteiro do arquivo CMakeLists.txt
	# entre os executáveis existentes no mesmo.
	with open(cmakelistsFile, "r") as f:
		executablesText = f.read().split("add_executable(")

	# Remove a primeira parte do texto, antes do primeiro executável.
	executablesText.pop(0)

	# Instancia uma variável para os executáveis.
	executables = []

	# Captura apenas o nome do executável, excluindo o resto
	# do texto de cada elemento encontrado anteriormente.
	for executable in executablesText:
		executables.append(executable.split("\n")[0].strip())

	# Esta variável não é mais necessária.
	del executablesText

	executables.sort()

	# Pastas padrão dos arquivos do OpenGL,
	# entre outros projetos que não têm entrada
	# no arquivo CMakeLists.txt.
	defaultFolders = [
		"build",
		"common",
		"distrib",
		"external",
		"misc01_math_cheatsheet",
		"misc04_building_your_own_app",
		"misc05_picking",
		"tutorial18_billboards_and_particles"
	]

	# Exclui da lista de pastas as que possuem
	# entrada no arquivo CMakeLists.txt.
	for project in executables:
		if project in folders:
			folders.remove(project)

	# Exclui da lista de pastas as que não possuem entrada no arquivo
	# CMakeLists.txt, mas fazem parte do arquivos padrão dos projetos OpenGL.
	# Depois desta etapa, restam apenas os projetos
	# disponíveis para serem construídos posteriormente.
	for folder in defaultFolders:
		if folder in folders:
			folders.remove(folder)

	if folders:
		folders.sort()
		break

	clearScreen()

	print("\n  Não foi encontrada nenhuma pasta com um novo projeto!\n")
	print("\n  Crie uma pasta com um projeto novo no diretório informado anteriormente")
	input("\n  Após isso, pressione [ENTER] para tentar novamente.")

# Lista as pastas encontradas que não fazem parte dos arquivos
# padrão do OpenGL e nem foram adicionadas aos projetos atuais.
while True:
	try:
		clearScreen()
		
		# Lista as pastas que ainda não foram inclusas aos projetos pelo CMake.
		for n, i in enumerate(folders):
			print("\n  {:2d}. {}".format(n, i), end="")
		
		newProject = int(input("\n\n  Qual pasta listada acima contém o projeto a ser construído? "))
		
		# Verifica se o valor informado está presente na lista.
		if not newProject in range(0, len(folders)):
			raise ValueError()
		
		newProject = folders[newProject]
		
		break
	# Caso a opção informada seja inválida.
	except ValueError:
		input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")

clearScreen()

print("\n  Que nome deseja dar ao projeto?\n")
print("  Este nome será usado apenas como comentário antes das entradas no arquivo CMakeLists.txt.")
print("  Se não informar nada, o nome usado será o mesmo da pasta escolhida anteriormente.\n")

# Recebe um nome para o projeto.
projectName = str(input("  Nome do projeto: "))

# Se o nome informado estiver vazio, utiliza o nome da pasta do projeto.
if not projectName:
	projectName = newProject

# Lista os arquivos disponíveis na pasta do projeto,
# que podem ser inclusos como parte do código.
availableFiles = fileTree(cmakelistsPath + "/" + newProject)

# Recebe os arquivos que foram selecionados para fazer parte do código.
selectedFiles = []

while True:
	try:
		clearScreen()
		
		print("\n  Arquivos existentes na pasta do seu projeto:\n")

		# Lista os arquivos dentro da pasta do projeto a ser construído.
		for n, i in enumerate(availableFiles):
			print("  X {:3d}. {}".format(n, i)) if n in selectedFiles else print("    {:3d}. {}".format(n, i))
		
		print("\n  Quais arquivos acima fazem parte do código?")
		print("\n  Para incluir ou desfazer inclusão, informe o número referente ao arquivo.")
		print("  Devem ser selecionados na ordem em que devem ser inclusos.")
		print("  Quando estiver pronto, apenas pressione [ENTER].")
		
		# Recebe o arquivo a ser adicionado ou descartado.
		fileToAdd = input("\n  Índice do arquivo: ")

		# Se nenhum arquivo for informado, pula esta etapa.
		if not fileToAdd:
			if not selectedFiles:
				input("\n  Pelo menos um arquivo deve ser selecionado! Pressione [ENTER] para tentar novamente.")
				continue
			
			break
		
		fileToAdd = int(fileToAdd)
		
		# Verifica se o valor informado está presente na lista.
		if not fileToAdd in range(0, len(availableFiles)):
			raise ValueError()
		
		selectedFiles.remove(fileToAdd) if fileToAdd in selectedFiles else selectedFiles.append(fileToAdd)
	# Caso a opção informada seja inválida.
	except ValueError:
		input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")

clearScreen()

# Monta o primeiro texto que deve ser adicionado ao CMakeLists.txt.
firstTextToWrite = []

firstTextToWrite.append("\n# {}\n".format(projectName))
firstTextToWrite.append("add_executable({}\n".format(newProject))

# Inclui no primeiro texto os arquivos selecionados anteriormente.
if selectedFiles:
	for i in selectedFiles:
		firstTextToWrite.append("\t{}/{}\n".format(newProject, availableFiles[i]))

	firstTextToWrite.append("\n")

# Inclui os arquivos das bibliotecas padrão.
commonFiles = fileTree(cmakelistsPath + "/common")

for i in commonFiles:
	firstTextToWrite.append("\tcommon/{}\n".format(i))

firstTextToWrite.append(")\n\n")
firstTextToWrite.append("target_link_libraries({}\n".format(newProject))
firstTextToWrite.append("\t${ALL_LIBS}\n")
firstTextToWrite.append("\tANTTWEAKBAR_116_OGLCORE_GLFW\n")
firstTextToWrite.append("\tassimp\n")
firstTextToWrite.append("\tBulletCollision\n")
firstTextToWrite.append("\tBulletDynamics\n")
firstTextToWrite.append("\tLinearMath\n")
firstTextToWrite.append(")\n\n")

firstTextToWrite.append("# Xcode and Visual working directories\n")
firstTextToWrite.append("set_target_properties({} PROPERTIES XCODE_ATTRIBUTE_CONFIGURATION_BUILD_DIR \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\")\n".format(newProject, newProject))
firstTextToWrite.append("create_target_launcher({} WORKING_DIRECTORY \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\")\n".format(newProject, newProject))

# Monta o segundo texto que deve ser adicionado ao CMakeLists.txt.
secondTextToWrite = []

secondTextToWrite.append("add_custom_command(\n")
secondTextToWrite.append("   TARGET {} POST_BUILD\n".format(newProject))
secondTextToWrite.append("   COMMAND ${{CMAKE_COMMAND}} -E copy \"${{CMAKE_CURRENT_BINARY_DIR}}/${{CMAKE_CFG_INTDIR}}/{}${{CMAKE_EXECUTABLE_SUFFIX}}\" \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\"\n".format(newProject, newProject))
secondTextToWrite.append(")\n")

# Recebe a linha em que o primeiro texto deve ser escrito.
lineToAddFirstText = int(0)

# Procura qual é a linha da última vez em que o comando "create_target_launcher()"
# é chamado, para escrever o primeiro texto depois de tal linha.
with open(cmakelistsFile, "r") as f:
	for n, i in enumerate(f):
		if "create_target_launcher(" in i:
			# É incrementado 1 e não 2 pois o índice das linhas na função open() começa em 0.
			lineToAddFirstText = n + 1

# Flag de permissão de escrita do primeiro texto no arquivo.
allowWriteFirstText = True

# Caso não achou uma linha apropriada para adicionar o primeiro texto.
if not lineToAddFirstText:
	while True:
		clearScreen()

		# Exibe todo o texto que deve ser adicionado no CMakeLists.txt.
		print("\n  Os comandos que devem ser escritos no CMakeLists.txt foram gerados com sucesso!")
		print("\n  Primeira seção:")

		for i in firstTextToWrite:
			print(i)

		print("\n  Segunda seção:\n")
			
		for i in secondTextToWrite:
			print(i)
		
		# Espera por uma decisão do usuário.
		try:
			print("  O CMakeGL não encontrou um local apropriado para escrever a primeira seção.")
			print("  O que deseja fazer?\n")
			print("  [1] Incluir automaticamente mesmo assim.")
			print("  [2] Copiar o texto e incluir manualmente.\n")
			
			opt = int(input("  Sua opção: "))

			# Verifica se o valor informado está disponível.
			if not opt in [1, 2]:
				raise ValueError()
			
			# Se o usuário quiser escrever o texto manualmente, não permite que o programa escreva.
			if opt == 2:
				allowWriteFirstText = False
			
			break
		except ValueError:
			input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")

# Recebe a linha em que o segundo texto deve ser escrito.
lineToAddSecondText = int(0)

# Procura qual é a linha da última vez em que o comando "add_custom_command()"
# é chamado, para escrever o segundo texto depois de tal função.
with open(cmakelistsFile, "r") as f:
	for n, i in enumerate(f):
		if "add_custom_command(" in i:
			# É incrementado 4 e não 5 pois o índice das linhas na função open() começa em 0.
			lineToAddSecondText = n + 4

# Flag de permissão de escrita do segundo texto no arquivo.
allowWriteSecondText = True

# Caso não achou uma linha apropriada para adicionar o segundo texto.
if not lineToAddSecondText:
	while True:
		clearScreen()

		# Exibe todo o texto que deve ser adicionado no CMakeLists.txt.
		print("\n  Os comandos que devem ser escritos no CMakeLists.txt foram gerados com sucesso!")
		print("\n  Primeira seção:")

		for i in firstTextToWrite:
			print(i)

		print("\n  Segunda seção:\n")
			
		for i in secondTextToWrite:
			print(i)
		
		# Espera por uma decisão do usuário.
		try:
			print("  O CMakeGL não encontrou um local apropriado para escrever a segunda seção.")
			print("  O que deseja fazer?\n")
			print("  [1] Incluir automaticamente mesmo assim.")
			print("  [2] Copiar o texto e incluir manualmente.\n")
			
			opt = int(input("  Sua opção: "))

			# Verifica se o valor informado está disponível.
			if not opt in [1, 2]:
				raise ValueError()
			
			# Se o usuário quiser escrever o texto manualmente, não permite que o programa escreva.
			if opt == 2:
				allowWriteSecondText = False
			
			break
		except ValueError:
			input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")



# Inicia as operações finais.
clearScreen()

print("\n  Tudo pronto!")

print("\n  Executando as operações necessárias.")
print("  Aguarde. Nenhuma ação é necessária.")



# Escreve o primeiro texto no arquivo.
print("\n  Escrevendo a primeira seção no arquivo CMakeLists.txt...", end="")

# Captura o conteúdo do arquivo e insere o primeiro texto na linha encontrada anteriormente.
with open(cmakelistsFile, "r") as f:
	fileContent = f.readlines()

fileContent[lineToAddFirstText:lineToAddFirstText] = firstTextToWrite

fileContent = "".join(fileContent)

# Tenta escrever o primeiro texto no arquivo.
# Se der erro, finaliza o programa.
while True:
	try:
		with open(cmakelistsFile, "w") as f:
			f.write(fileContent)
		
		print("\n  Primeira seção escrita com sucesso!")
		
		break
	except Exception as e:
		print("\n  Houve um erro ao escrever a primeira seção:")
		print("\n  {}".format(str(e)))
		print("\n  Saindo...\n")
		
		exit()



# Escreve o segundo texto.
print("\n  Escrevendo a segunda seção no arquivo CMakeLists.txt...", end="")

# Recebe a linha em que o segundo texto deve ser escrito.
lineToAddSecondText = int(0)

# Procura novamente qual é a linha da última vez em que o comando "add_custom_command()"
# é chamado, para escrever o segundo texto depois de tal função.
# É necessário verificar novamente já que o conteúdo
# foi modificado pela inserção do primeiro texto.
with open(cmakelistsFile, "r") as f:
	for n, i in enumerate(f):
		if "add_custom_command(" in i:
			# É incrementado 4 e não 5 pois o índice das linhas na função open() começa em 0.
			lineToAddSecondText = n + 4

# Captura o conteúdo do arquivo e insere o segundo texto na linha encontrada anteriormente.
with open(cmakelistsFile, "r") as f:
	fileContent = f.readlines()

fileContent[lineToAddSecondText:lineToAddSecondText] = secondTextToWrite

fileContent = "".join(fileContent)

# Tenta escrever o segundo texto no arquivo.
# Se der erro, finaliza o programa.
while True:
	try:
		with open(cmakelistsFile, "w") as f:
			f.write(fileContent)
		
		print("\n  Segunda seção escrita com sucesso!")
		
		break
	except Exception as e:
		print("\n  Houve um erro ao escrever a segunda seção:")
		print("\n  {}".format(str(e)))
		print("\n  Saindo...\n")
		
		exit()



# Etapa de criação da pasta build.
print("\n  Criando a pasta build dentro do diretório informado anteriormente...", end="")

# Tenta criar a pasta build dentro da pasta informada pelo usuário.
# Se ela já existir pula esta etapa.
try:
	os.mkdir("{}/build".format(cmakelistsPath))

	print("\n  Pasta criada com sucesso!")
except FileExistsError:
	print("\n  Pasta já criada anteriormente.")
	
	if os.path.exists("{}/build/CMakeCache.txt".format(cmakelistsPath)):
		os.remove("{}/build/CMakeCache.txt".format(cmakelistsPath))



# Constrói o projeto com o CMake.
try:
	print("\n  Construindo o projeto com o CMake...")
	print("  Executando comando: cd build && cmake ..")
	
	# Cria um subprocesso para executar os comandos de construção.
	cmd = Popen("cd \"{}/build\" && cmake ..".format(cmakelistsPath), stdout=PIPE, stderr=PIPE, shell=True, encoding="utf-8")
	
	# Informa o ID do subprocesso.
	print("  PID: {}".format(cmd.pid))

	# Estado da execução do subprocesso.
	processDone = False
	
	# Thread da animação de execução.
	feedbackThread = Thread(target=rotatePipe)
	feedbackThread.start()
	
	cmd.wait()
	
	# Quando a espera acabar, muda o estado de execução da animação.
	processDone = True

	# Captura os erros do subprocesso.
	errors = cmd.communicate()[1]

	# Se houver erros, exibe-os.
	if errors:
		print("\r  Houve alguns erros ao construir o projeto com o CMake:\n\n  ---\n")
		print(errors)
		print("\n  ---")
	else:
		print("\r  Nenhum erro foi relatado ao executar o comando!")
# Captura erros provenientes do subprocesso em si.
except SubprocessError as e:
	cmd.kill()

	print("\r  Houve alguns erros ao executar o subprocesso:\n\n  ---\n")
	print("\n  {}".format(str(e)))
	print("\n  ---")



# Compila todos os projetos.
try:
	print("\n  Compilando os projetos com o Make...")
	print("  Executando comando: cd build && make all")
	
	# Cria um subprocesso para executar os comandos de compilação.
	cmd = Popen("cd \"{}/build\" && make all".format(cmakelistsPath), stdout=PIPE, stderr=PIPE, shell=True, encoding="utf-8")
	
	# Informa o ID do subprocesso.
	print("  PID: {}".format(cmd.pid))
	
	# Estado da execução do subprocesso.
	processDone = False
	
	# Thread da animação de execução.
	feedbackThread = Thread(target=rotatePipe)
	feedbackThread.start()
	
	cmd.wait()
	
	# Quando a espera acabar, muda o estado de execução da animação.
	processDone = True

	# Captura os erros do subprocesso.
	errors = cmd.communicate()[1]

	# Se houver erros, exibe-os.
	if errors:
		print("\r  Houve alguns erros ao compilar os projetos com o Make:\n\n  ---\n")
		print(errors)
		print("\n  ---")
	else:
		print("\r  Nenhum erro foi relatado ao executar o comando!")
# Captura erros provenientes do subprocesso em si.
except SubprocessError as e:
	cmd.kill()

	print("\r  Houve alguns erros ao executar o subprocesso:\n\n  ---\n")
	print("\n  {}".format(str(e)))
	print("\n  ---")



# Exibe uma última mensagem informando a finalização dos procedimentos.
print("\n  Todas as operações pertinentes foram realizadas com êxito!")
print("  Confira no log acima se houve algum erro e, se necessário, execute este programa novamente.")

input("\n  Pressione [ENTER] para continuar...")

clearScreen()

print("\n  Muito obrigado por utilizar este aplicativo!")

print("\n  Desenvolvido por Marlon Luís de Col")
print("  Engenharia de Computação")
print("  2019 - Unoesc Chapecó")

input("\n  Pressione [ENTER] para finalizar...")

print()