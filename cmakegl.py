# Importa os pacotes necessários.
from subprocess import Popen, PIPE, SubprocessError
from threading import Thread
from tkinter import filedialog as fd
import os, queue, utils

# Constrói e compila todos os projetos.
def buildProj(cmakelistsFile):
	# Extrai o diretório do arquivo selecionado.
	cmakelistsPath = os.path.dirname(cmakelistsFile)
	
	# Etapa de criação da pasta build.
	print("\n  Criando a pasta \"build\" no diretório informado...", end="")

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
		print("\n  Construindo os executáveis com o CMake...")
		print("  Executando comando: cd build && cmake ..")
		
		# Cria um subprocesso para executar os comandos de construção.
		cmd = Popen("cd \"{}/build\" && cmake ..".format(cmakelistsPath), stdout=PIPE, stderr=PIPE, shell=True, encoding="utf-8")
		
		# Informa o ID do subprocesso.
		print("  PID: {}".format(cmd.pid))
		
		# Envia o status do processo à Thread de animação.
		statusQueue = queue.Queue()
		statusQueue.put(True)
		
		# Thread da animação de execução.
		feedbackThread = Thread(target=utils.rotatePipe, args=(statusQueue,))
		feedbackThread.start()
		
		cmd.wait()
		
		# Quando a espera acabar, muda o status do processo.
		statusQueue.put(False)

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
		
		# Envia o status do processo à Thread de animação.
		statusQueue = queue.Queue()
		statusQueue.put(True)
		
		# Thread da animação de execução.
		feedbackThread = Thread(target=utils.rotatePipe, args=(statusQueue,))
		feedbackThread.start()
		
		cmd.wait()
		
		# Quando a espera acabar, muda o status do processo.
		statusQueue.put(False)

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

# Retorna uma lista com todos os executáveis existentes.
def getExecs(cmakelistsFile):
	# Separa o texto inteiro do arquivo CMakeLists.txt entre os executáveis existentes.
	with open(cmakelistsFile, "r") as f:
		executablesText = f.read().split("add_executable(")

	# Remove a primeira parte do texto, antes do primeiro executável.
	executablesText.pop(0)

	# Instancia uma variável para os executáveis.
	executables = []

	# Captura apenas o nome do executável, excluindo o resto do texto de cada elemento encontrado anteriormente.
	for executable in executablesText:
		executables.append(executable.split("\n")[0].strip())

	# Esta variável não é mais necessária.
	del executablesText

	# Ordena a lista.
	executables.sort()

	# Retorna a lista
	return executables

# Adiciona um projeto.
def addExec(cmakelistsFile):
	# Extrai o diretório do arquivo CMakeLists.txt.
	cmakelistsPath = os.path.dirname(cmakelistsFile)

	# Espera o usuário informar a pasta que contém os arquivos do novo projeto.
	while True:
		utils.clearScreen()

		print("\n  Selecione a pasta com os arquivos do novo projeto.", end="")
		
		# Inicia um diálogo para selecionar a pasta do novo projeto.
		newExecFolder = fd.askdirectory(initialdir=cmakelistsPath, title="Selecione a pasta do novo projeto")

		# Verifica se é uma pasta válida.
		# Deve ser uma pasta dentro da mesma pasta do arquivo CMakeLists.txt.
		if not utils.isInsideFolder(newExecFolder, cmakelistsPath):
			print("\n\n  A pasta informada não é válida!")
			print("  Ela deve ser uma pasta dentro de {}".format(cmakelistsPath))
			input("\n  Pressione [ENTER] para tentar novamente...")
			continue
		
		# Se chegou até aqui, a pasta é válida.
		break
	
	# Lista os arquivos disponíveis na pasta do projeto,
	# que podem ser inclusos como parte do código.
	availableFiles = utils.fileTree(newExecFolder)

	# Recebe os arquivos que foram selecionados para fazer parte do código.
	selectedFiles = []

	# Espera o usuário selecionar os arquivo
	while True:
		try:
			utils.clearScreen()
			
			print("\n  Arquivos existentes na pasta {}:\n".format(newExecFolder))

			# Lista os arquivos dentro da pasta do projeto a ser construído.
			for n, i in enumerate(availableFiles):
				print("  X {:3d}. {}".format(n, i)) if n in selectedFiles else print("    {:3d}. {}".format(n, i))
			
			print("\n  Quais arquivos acima fazem parte do projeto?")
			print("\n  Para incluir ou desfazer inclusão, informe o número referente ao arquivo.")
			print("  Devem ser selecionados na ordem em que devem ser inclusos.")
			print("  Quando estiver pronto, apenas pressione [ENTER].")
			
			# Recebe o arquivo a ser adicionado ou descartado.
			fileToAdd = input("\n  Índice do arquivo: ")

			# Se nenhum arquivo for informado, pula esta etapa.
			if not fileToAdd:
				if not selectedFiles:
					print("\n  Pelo menos um arquivo deve ser selecionado!")
					input("\n  Pressione [ENTER] para tentar novamente...")
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
	
	# Bibliotecas disponíveis.
	libs = utils.fileTree(cmakelistsPath + os.sep + "common", ".hpp", 1)

	# Retira a extensão das bibliotecas.
	for i, lib in enumerate(libs):
		libs[i] = os.path.splitext(lib)[0]

	# Recebe as bibliotecas que serão adicionadas ao novo projeto.
	newExecLibs = []

	# Espera o usuário informar as bibliotecas externas que deseja incluir ao projeto.
	while True:
		try:
			utils.clearScreen()

			print("\n  Bibliotecas disponíveis para incluir ao seu novo projeto:\n")
			
			# Lista as bibliotecas disponíveis.
			for n, i in enumerate(libs):
				print("  X {:d}. {}".format(n, i)) if n in newExecLibs else print("    {:d}. {}".format(n, i))
			
			print("\n  Deseja incluir alguma? Isto é opcional. Depende do seu projeto.")
			print("\n  Para incluir ou desfazer inclusão, informe o número referente à biblioteca.")
			print("  Quando estiver pronto, apenas pressione [ENTER].")
			
			# Recebe a biblioteca a ser adicionada ou descartada.
			libToAdd = input("\n  Índice da biblioteca: ")

			# Se nenhuma biblioteca for informada, pula esta etapa.
			if not libToAdd:
				break
			
			libToAdd = int(libToAdd)
			
			# Verifica se o valor informado está presente na lista.
			if not libToAdd in range(0, len(libs)):
				raise ValueError()
			
			newExecLibs.remove(libToAdd) if libToAdd in newExecLibs else newExecLibs.append(libToAdd)
		# Caso a opção informada seja inválida.
		except ValueError:
			input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")
	
	# Ordena as bibliotecas.
	newExecLibs.sort()
	
	# Bibliotecas externas disponíveis.
	externalLibs = [
		"ANTTWEAKBAR_116_OGLCORE_GLFW",
		"assimp",
		"BulletCollision",
		"BulletDynamics",
		"LinearMath"
	]

	# Recebe as bibliotecas externas que serão adicionadas ao novo projeto.
	newExecExternals = []
	
	# Espera o usuário informar as bibliotecas externas que deseja incluir ao projeto.
	while True:
		try:
			utils.clearScreen()

			print("\n  Bibliotecas externas disponíveis para incluir ao seu novo projeto:\n")
			
			# Lista as bibliotecas externas disponíveis.
			for n, i in enumerate(externalLibs):
				print("  X {:d}. {}".format(n, i)) if n in newExecExternals else print("    {:d}. {}".format(n, i))
			
			print("\n  Deseja incluir alguma? Isto é opcional. Depende do seu projeto.")
			print("\n  Para incluir ou desfazer inclusão, informe o número referente à biblioteca.")
			print("  Quando estiver pronto, apenas pressione [ENTER].")
			
			# Recebe a biblioteca a ser adicionada ou descartada.
			libToAdd = input("\n  Índice da biblioteca: ")

			# Se nenhuma biblioteca for informada, pula esta etapa.
			if not libToAdd:
				break
			
			libToAdd = int(libToAdd)
			
			# Verifica se o valor informado está presente na lista.
			if not libToAdd in range(0, len(externalLibs)):
				raise ValueError()
			
			newExecExternals.remove(libToAdd) if libToAdd in newExecExternals else newExecExternals.append(libToAdd)
		# Caso a opção informada seja inválida.
		except ValueError:
			input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")
	
	# Ordena as bibliotecas externas.
	newExecExternals.sort()
	
	# Lista todos os executáveis existentes.
	executables = getExecs(cmakelistsFile)

	# Espera o usuário informar um nome para o executável.
	while True:
		try:
			utils.clearScreen()
			
			newExecName = str(input("\n  Informe o nome do novo executável: ")).strip()
			
			# Caso o nome informado seja inválido.
			if not newExecName or not newExecName.isidentifier():
				raise Exception("O nome informado é inválido!")
			
			# Caso o nome já existe.
			if newExecName in executables:
				raise Exception("Já existe um executável com este nome!")
			
			# Não pode permitir o nome "test" pois é reservado pelo CMake.
			if newExecName == "test":
				raise Exception("Este nome é reservado pelo CMake!")
			
			# Caso o nome seja muito extenso.
			if len(newExecName) >= 100:
				raise Exception("Este nome é muito extenso!")
			
			# Se chegou até aqui, o nome é válido.
			break
		except Exception as e:
			print("\n  {}".format(str(e)))
			input("\n  Pressione [ENTER] para tentar novamente...")
	
	utils.clearScreen()

	print("\n  Que título deseja dar ao executável?\n")
	print("  Este título será usado apenas como comentário antes das entradas no arquivo CMakeLists.txt.")
	print("  Se não informar nada, o título usado será igual ao nome do executável que definiu anteriormente.\n")

	# Recebe um nome para o projeto.
	newExecTitle = str(input("  Título do projeto: ")).strip()

	# Se o nome informado estiver vazio, utiliza o nome da pasta do projeto.
	if not newExecTitle:
		newExecTitle = newExecName.capitalize()
	
	utils.clearScreen()

	# Monta o primeiro texto que deve ser adicionado ao CMakeLists.txt.
	firstTextToWrite = []

	firstTextToWrite.append("\n# {}\n".format(newExecTitle))
	firstTextToWrite.append("add_executable({}\n".format(newExecName))
	
	# Extrai apenas o nome da pasta do novo projeto.
	newExecFolder = newExecFolder.split(os.sep)[-1]

	# Inclui no primeiro texto os arquivos selecionados anteriormente.
	if selectedFiles:
		for i in selectedFiles:
			firstTextToWrite.append("\t{}/{}\n".format(newExecFolder, availableFiles[i]))

		firstTextToWrite.append("\n")
	
	# Inclui as bibliotcas padrão selecionadas anteriormente.
	for lib in newExecLibs:
		for ext in ["cpp", "hpp"]:
			firstTextToWrite.append("\tcommon/{}.{}\n".format(libs[lib], ext))

	firstTextToWrite.append(")\n\n")
	firstTextToWrite.append("target_link_libraries({}\n".format(newExecName))
	firstTextToWrite.append("\t${ALL_LIBS}\n")
	
	# Inclui as bibliotecas externas.
	for lib in newExecExternals:
		firstTextToWrite.append("\t{}\n".format(externalLibs[lib]))
	
	firstTextToWrite.append(")\n\n")

	firstTextToWrite.append("# Xcode and Visual working directories\n")
	firstTextToWrite.append("set_target_properties({} PROPERTIES XCODE_ATTRIBUTE_CONFIGURATION_BUILD_DIR \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\")\n".format(newExecName, newExecFolder))
	firstTextToWrite.append("create_target_launcher({} WORKING_DIRECTORY \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\")\n".format(newExecName, newExecFolder))

	# Monta o segundo texto que deve ser adicionado ao CMakeLists.txt.
	secondTextToWrite = []

	secondTextToWrite.append("add_custom_command(\n")
	secondTextToWrite.append("   TARGET {} POST_BUILD\n".format(newExecName))
	secondTextToWrite.append("   COMMAND ${{CMAKE_COMMAND}} -E copy \"${{CMAKE_CURRENT_BINARY_DIR}}/${{CMAKE_CFG_INTDIR}}/{}${{CMAKE_EXECUTABLE_SUFFIX}}\" \"${{CMAKE_CURRENT_SOURCE_DIR}}/{}/\"\n".format(newExecName, newExecFolder))
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
			utils.clearScreen()

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
				
				# Se o usuário quiser escrever o texto manualmente, não permite que o programa escreva posteriormente.
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
			utils.clearScreen()

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
				
				# Se o usuário quiser escrever o texto manualmente, não permite que o programa escreva, posteriormente.
				if opt == 2:
					allowWriteSecondText = False
				
				break
			except ValueError:
				input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")
	
	# Inicia as operações finais.
	utils.clearScreen()

	print("\n  Tudo pronto!")

	print("\n  Executando as operações necessárias.")
	print("  Aguarde. Nenhuma ação é necessária.")
	
	# Faz o backup do arquivo CMakeLists.txt.
	print("\n  Fazendo backup do arquivo CMakeLists.txt...", end="")
	
	try:
		bkp = utils.backupFile(cmakelistsFile)

		print("\n  Backup realizado com sucesso!")
		print("  O backup está localizado em: {}".format(bkp))
	except IOError:
		print("\n  AVISO: Não foi possível realizar o backup!")
	
	# Escreve o primeiro texto no arquivo.
	if allowWriteFirstText:
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
				input("\n  Pressione [ENTER] para voltar ao menu principal...")
				
				return False
	
	# Escreve o segundo texto.
	if allowWriteSecondText:
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
				input("\n  Pressione [ENTER] para voltar ao menu principal...")
				
				return False
	
	# Constrói e compila o projeto.
	buildProj(cmakelistsFile)
	
	# Exibe uma última mensagem informando a finalização dos procedimentos.
	print("\n  Todas as operações pertinentes foram realizadas com êxito!")
	print("  Confira no log acima se houve algum erro e, se necessário, execute esta etapa novamente.")

	input("\n  Pressione [ENTER] para voltar ao menu principal...")

# Constrói e compila todos os projetos.
def rebuildAll(cmakelistsFile):
	# Constrói e compila todos os projetos.
	buildProj(cmakelistsFile)

	# Finalização dos procedimentos.
	print("\n  Todos os projetos foram construídos e compilados com êxito!")
	print("  Confira no log acima se houve algum erro e, se necessário, execute esta etapa novamente.")

	input("\n  Pressione [ENTER] para voltar ao menu principal...")

# Lista os executáveis existentes.
def listExecs(cmakelistsFile):
	print("\n  Executáveis encontrados no arquivo CMakeLists.txt:\n")
	
	# Obtém os executáveis disponíveis.
	execs = getExecs(cmakelistsFile)

	for ex in execs:
		print("  {}".format(ex))
	
	# Exibe a quantidade de executáveis.
	print("\n  Total: {:d} executáveis.".format(len(execs)))
	
	input("\n  Pressione [ENTER] para voltar ao menu principal...")

# Restaura um backup do arquivo CMakeLists.txt.
def restoreBackup(cmakelistsFile):
	# Inicia um diálogo para selecionar o arquivo CMakeLists.txt.
	cmakelistsBkpFile = cmakelistsFile + ".bkp"

	# Verifica se o backup existe.
	if os.path.isfile(cmakelistsBkpFile):
		# Inicia o processo de restauração.
		try:
			# Salva o arquivo original.
			print("\n  Salvando o arquivo CMakeLists.txt atual...", end="")
			cmakelistsOldFile = utils.saveFile(utils.fileFromBkp(cmakelistsBkpFile))
			print("\n  Arquivo atual salvo com sucesso!")
			print("  O arquivo está localizado em: {}".format(cmakelistsOldFile))

			# Restaura o backup.
			print("\n  Restaurando o arquivo CMakeLists.txt...", end="")
			cmakelistsFile = utils.restoreFile(cmakelistsBkpFile)
			print("\n  Restauração realizada com sucesso!")
			print("  O arquivo está localizado em: {}".format(cmakelistsFile))

			# Exclui o backup.
			print("\n  Excluindo arquivo de backup...", end="")
			os.remove(cmakelistsBkpFile)
			print("\n  Backup excluído com sucesso!")
			
			buildProj(cmakelistsFile)
		except IOError:
			print("\n  AVISO: Não foi possível terminar o processo de restauração!")
			print("  Será algum problema com as permissões dos arquivos?")
	else:
		print("\n  O arquivo de backup ainda não foi criado nesta pasta!")
	
	input("\n  Pressione [ENTER] para voltar ao menu principal...")

# Configura as janelas do Tkinter.
utils.configDialogs()

# Arquivo CMakeLists.txt.
cmakelistsFile = None

# Menu principal do programa.
while True:
	utils.clearScreen()
	utils.printTitle()

	print("  Bem-vindo ao CMakeGL!")

	print("\n  O CMakeGL é um programa CLI que gerencia projetos OpenGL.")
	print("  Utiliza as dependências necessárias, constrói os arquivos e compila tudo.")
	print("\n  Consulte a documentação em https://github.com/mlc2307/cmakegl")
	print("  Ou acesse o site http://www.opengl-tutorial.org")

	# Caso o programa foi executado agora.
	if cmakelistsFile is None:
		input("\n  Pressione [ENTER] para continuar...")
		cmakelistsFile = ""
		continue

	# Etapa de seleção do arquivo CMakeLists.txt.
	if not cmakelistsFile:
		print("\n  Selecione o arquivo CMakeLists.txt na pasta dos arquivos OpenGL.", end="")
		
		# Inicia um diálogo para selecionar o arquivo CMakeLists.txt.
		cmakelistsFile = fd.askopenfilename(title="Selecione o arquivo CMakeLists.txt", filetypes=[["Arquivo do CMake", "CMakeLists.txt"]])

		# Aviso se o arquivo for inválido.
		if not cmakelistsFile:
			print("\n\n  O arquivo selecionado é inválido!")
			input("\n  Pressione [ENTER] para tentar novamente...")

		# Se chegou até aqui sem lançar um erro, o arquivo é válido.
		continue

	# Menu principal.
	options = [
		["Adicionar executável", "addExec"],
		["Reconstruir projetos", "rebuildAll"],
		["Listar executáveis", "listExecs"],
		["Restaurar backup", "restoreBackup"]
	]

	print("\n  O que deseja fazer?\n")
	
	# Lista as opções.
	for i, opt in enumerate(options):
		print("  [{:d}] {}".format(i + 1, opt[0]))
	
	print("  [0] Sair")

	# Exibe a pasta selecionada.
	print("\n  Trabalhando na pasta {}".format(os.path.dirname(cmakelistsFile)))
	
	# Permite trocar de pasta.
	print("\n  [X] Selecionar arquivo CMakeLists.txt novamente")

	# Lê a opção escolhida pelo usuário.
	try:
		opt = input("\n  Sua opção: ")
		
		if opt in ["X", "x"]:
			cmakelistsFile = ""
			continue
		
		opt = int(opt)
		
		# Verifica se a opção existe.
		if opt not in range(0, len(options) + 1):
			raise ValueError()
		
		# Se a opção for 0, sai do programa.
		if not opt:
			break
		
		utils.clearScreen()
		
		# Senão, executa a opção correspondente.
		locals()[options[opt - 1][1]](cmakelistsFile)
	except ValueError:
		input("\n  Opção inválida! Pressione [ENTER] para tentar novamente.")
		continue

utils.clearScreen()
utils.printTitle()

# Agradecimentos e encerramento do programa.
print("  Muito obrigado por utilizar o CMakeGL!")

print("\n  Desenvolvido por Marlon Luís de Col")
print("  Engenharia de Computação")
print("  2019 - Unoesc Chapecó")

input("\n  Pressione [ENTER] para finalizar...")

print()

utils.clearScreen()