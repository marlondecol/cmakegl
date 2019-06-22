# Importa os pacotes necessários.
from sys import stdout
import itertools, os, queue, shutil, time
import tkinter as tk

# Faz backup de um arquivo.
# Caso não consiga fazer o backup, retorna uma exceção de IOError.
def backupFile(file):
	# A extensão do backup será .bkp.
	bkp = file + ".bkp"
	shutil.copyfile(file, bkp)
	
	# Se conseguiu criar o backup, retorna o caminho até ele.
	return bkp

# Limpa a tela executando o comando específico do sistema operacional.
def clearScreen():
	os.system("cls" if os.name == "nt" else "clear")

# Faz um print com uma margem de uma linha em branco acima e dois espaços à esquerda.
def clprint(str, end="\n"):
	cnlprint(str, 1, end)

# Faz um print com uma margem de N linhas em branco acima e dois espaços à esquerda.
def cnlprint(str, breaklines=2, end="\n"):
	for i in range(0, breaklines):
		print()
	
	cprint(str, end)

# Configura as janelas do TKinter.
def configDialogs():
	root = tk.Tk()
	root.withdraw()

# Faz um print com uma margem de dois espaços à esquerda.
def cprint(str, end="\n"):
	print("  {}".format(str), end=end)

# Retorna um arquivo sem a extensão .bkp.
def fileFromBkp(bkp):
	return bkp[:-4]

# Lista todos os arquivos dentro de uma pasta, recursivamente,
# podendo exibir apenas determinadas extensões e/ou até determinada profundidade.
def fileTree(path, ext=(), maxdepth=0):
	tree = []

	# Se a profundidade máxima for menor que 0, já termina.
	if maxdepth < 0:
		return tree
	
	# Se foram informadas extensões, transforma tudo para tupla, caso não seja.
	if ext and type(ext) is not tuple:
		ext = tuple(ext) if type(ext) is list else (ext,)

	# Faz a busca nesta pasta.
	scan = sorted(os.scandir(path), key=lambda x: (x.is_file(), x.name.lower()))

	# Verifica cada entrada.
	for entry in scan:
		# Se a entrada for uma pasta, faz uma nova busca.
		if entry.is_dir():
			depth = maxdepth

			if maxdepth:
				if maxdepth - 1 == 0:
					continue
				
				depth -= 1
			
			filesInside = fileTree("{}/{}".format(path, entry.name.strip()), ext, depth)

			if filesInside:
				for file in filesInside:
					tree.append("{}/{}".format(entry.name.strip(), file))
		
		# Apenas quando a entrada for um arquivo é que será adicionada à árvore.
		else:
			if ext and os.path.splitext(entry)[1] not in ext:
				continue

			tree.append(entry.name.strip())
	
	return tree

# Verifica se uma pasta está dentro de outra.
def isInsideFolder(child, parent):
	return child.startswith(os.path.abspath(parent) + os.sep)

# Imprime o título.
def printTitle(margin=True):
	lines = [
		" ██████╗███╗   ███╗ █████╗ ██╗  ██╗███████╗ ██████╗ ██╗",
		"██╔════╝████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔════╝ ██║",
		"██║     ██╔████╔██║███████║█████╔╝ █████╗  ██║  ███╗██║",
		"██║     ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██║   ██║██║",
		"╚██████╗██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗╚██████╔╝███████╗",
		" ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝"
	]

	# Caso deve exibir uma margem, deixa uma linha em branco antes,...
	if margin:
		print("\n\n")
	
	for line in lines:
		# ... dois espaços no início de cada linha...
		if margin:
			print("      ", end="")
		
		print(line)
	
	# ... e outra linha em branco depois.
	if margin:
		print("\n\n")

# Restaura um backup.
# Caso não consiga restaurar, retorna uma exceção de IOError.
def restoreFile(bkp):
	# A extensão .bkp é removida.
	file = fileFromBkp(bkp)
	shutil.copyfile(bkp, file)
	
	# Se conseguiu restaurar, retorna o caminho do arquivo.
	return file

# Gera uma animação de feedback enquanto executa um subprocesso.
def rotatePipe(statusQueue):
	# A animação consiste em um "traço girando", usando os caracteres abaixo.
	for c in itertools.cycle(["|", "/", "-", "\\"]):
		# Para a animação caso o processo termine.
		try:
			if not statusQueue.get_nowait():
				break
		except queue.Empty:
			pass
		
		stdout.write("\r  " + c)
		stdout.flush()

		# Delay de transição dos caracteres.
		time.sleep(1/8)
	
	stdout.write("")

# Salva uma cópia de um arquivo antes de modificar o original.
# Caso não consiga salvar, retorna uma exceção de IOError.
def saveFile(file):
	# A extensão do arquivo copiado será .old.
	old = file + ".old"
	shutil.copyfile(file, old)

	# Se conseguiu copiar, retorna o caminho do arquivo.
	return old

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