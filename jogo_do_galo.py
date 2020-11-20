# 99311 Rafael Serra e Oliveira

# CONVENCAO DE VOCABULARIO
# vetor: linha ou coluna
# posicao: 1 ... 9 (para dimensao = 3)
# jogador: -1, 0, 1
# simbolo: O, _, X (espaço para vazio)

DIMENSAO_TABULEIRO = 3 # Quantas celulas ha em cada linha/coluna/diagonal

def eh_vetor(tab): # aux
	if isinstance(tab, tuple):
		if len(tab) == DIMENSAO_TABULEIRO:
			for el in tab:
				if not isinstance(el, int):
					return False
				elif abs(el) > 1:
					return False
			
			return True
	
	return False

def eh_tabuleiro(tab):
	if isinstance(tab, tuple):
		if len(tab) == DIMENSAO_TABULEIRO:
			for el in tab:
				if not eh_vetor(el):
					return False
			
			return True
	return False

def eh_posicao(pos):
	return isinstance(pos, int) and 1 <= pos <= (DIMENSAO_TABULEIRO ** 2)

def eh_numero_de_vetor(num): # aux
	return isinstance(num, int) and 1 <= num <= DIMENSAO_TABULEIRO

def obter_coluna(tab, num_col):
	if not (eh_tabuleiro(tab) and eh_numero_de_vetor(num_col)):
		raise ValueError("obter_coluna: algum dos argumentos e invalido")

	col = ()
	for linha in tab:
		col = col + (linha[num_col - 1],)
	
	return col

def obter_linha(tab, num_linha):
	if not (eh_tabuleiro(tab) and eh_numero_de_vetor(num_linha)):
		raise ValueError("obter_linha: algum dos argumentos e invalido")

	return tab[num_linha - 1]

def obter_diagonal(tab, num_diagonal):
	if not (eh_tabuleiro(tab) and 1 <= num_diagonal <= 2):
		raise ValueError("obter_diagonal: algum dos argumentos e invalido")

	diag = ()
	for i in range(len(tab)):
		col = obter_coluna(tab, i + 1)
		diag = diag + (col[i if num_diagonal != 2 else len(col) - i - 1],)
	
	return diag

def simbolo_str(jogador): # aux
	if jogador == 1:
		return 'X'
	elif jogador == -1:
		return 'O'
	else:
		return ' '

def tabuleiro_str(tab):
	if not eh_tabuleiro(tab):
		raise ValueError("tableiro_str: o argumento e invalido")

	res = ""
	for i in range(len(tab)):
		if i > 0:
			res = res + "\n-----------\n"
		linha = tab[i]
		for j in range(len(linha)):
			if j > 0:
				res = res + "|"
			res = res + " " + simbolo_str(linha[j]) + " "

	return res

def obter_coordenadas(pos): # aux
	if not eh_posicao(pos):
		raise ValueError("obter_coordenadas: o argumento e invalido")
	
	linha, col = divmod(pos - 1, DIMENSAO_TABULEIRO)

	return (linha, col)

def obter_jogador(tab, pos): # aux
	if not (eh_tabuleiro(tab) and eh_posicao(pos)):
		raise ValueError("obter_jogador: algum dos argumentos e invalido")

	coords = obter_coordenadas(pos)

	return tab[coords[0]][coords[1]]

def eh_posicao_livre(tab, pos):
	if not (eh_tabuleiro(tab) and eh_posicao(pos)):
		raise ValueError("eh_posicao_livre: algum dos argumentos e invalido")

	return obter_jogador(tab, pos) == 0

def iterar_por_celulas(tab, func): # aux
	if not (eh_tabuleiro(tab) and callable(func)):
		raise ValueError("iterar_por_celulas: algum dos argumentos e invalido")

	pos = 0
	for i in range(len(tab)):
		for j in range(len(tab[i])):
			pos = pos + 1
			func(tab[i][j], pos, (i, j))

def obter_posicoes_livres(tab):
	if not eh_tabuleiro(tab):
		raise ValueError("obter_posicoes_livres: o argumento e invalido")

	livres = ()
	for i in range(1, DIMENSAO_TABULEIRO ** 2 + 1):
		if eh_posicao_livre(tab, i):
			livres = livres + (i,)
	
	return livres

def vetor_ganhador(vetor): # aux
	if not eh_vetor(vetor):
		raise ValueError("vetor_ganhador: o argumento e invalido")

	jogador = vetor[0]

	if jogador == 0:
		return 0
	
	for i in range(1, len(vetor)):
		if vetor[i] != vetor[0]:
			return 0
	
	return jogador

def jogador_ganhador(tab):
	if not eh_tabuleiro(tab):
		raise ValueError("jogador_ganhador: o argumento e invalido")

	for i in range(1, DIMENSAO_TABULEIRO + 1):
		ganhador_linha = vetor_ganhador(obter_linha(tab, i))
		if ganhador_linha != 0:
			return ganhador_linha
		ganhador_coluna = vetor_ganhador(obter_coluna(tab, i))
		if ganhador_coluna != 0:
			return ganhador_coluna

	for i in range(1, 3):
		ganhador_diagonal = vetor_ganhador(obter_diagonal(tab, i))
		if ganhador_diagonal != 0:
			return ganhador_diagonal

	return 0

def eh_jogador(jogador): # aux
	return isinstance(jogador, int) and abs(jogador) == 1

def marcar_posicao(tab, jogador, pos):
	if not (eh_tabuleiro(tab) and eh_jogador(jogador) \
		and eh_posicao(pos) and eh_posicao_livre(tab, pos)):
		raise ValueError("marcar_posicao: algum dos argumentos e invalido")

	coords = obter_coordenadas(pos)
	novo_tab = ()

	for i in range(len(tab)):
		linha = ()
		for j in range(len(tab[i])):
			if (i, j) == coords:
				linha = linha + (jogador,)
			else:
				linha = linha + (tab[i][j],)
		novo_tab = novo_tab + (linha,)

	return novo_tab

def escolher_posicao_manual(tab):
	if not eh_tabuleiro(tab):
		raise ValueError("escolher_posicao_manual: o argumento e invalido")

	escolha = int(input('Turno do jogador. Escolha uma posicao livre: '))

	if not (eh_posicao(escolha) and eh_posicao_livre(tab, escolha)):
		raise ValueError("escolher_posicao_manual: " \
			+ "a posicao introduzida e invalida")

	return escolha

def eh_estrategia(estrategia): # aux
	return isinstance(estrategia, str) and estrategia in (
		'basico',
		'normal',
		'perfeito'
	)

def obter_centro(): # aux
	return (DIMENSAO_TABULEIRO ** 2) // 2 + 1 # posicao

def obter_cantos(): # aux
	return ( # por ordem de posicao
		1,
		DIMENSAO_TABULEIRO,
		DIMENSAO_TABULEIRO * (DIMENSAO_TABULEIRO - 1),
		DIMENSAO_TABULEIRO ** 2,
	)

def obter_indice_para_completar_vetor(vetor, jogador): # aux
	if not (eh_vetor(vetor) and eh_jogador(jogador)):
		raise ValueError("obter_indice_para_completar_vetor: " \
			+ "algum dos argumentos e invalido")
	
	ind = None
	for j in range(len(vetor)):
		if vetor[j] == 0:
			if ind is None:
				return None
			else:
				ind = j
		elif vetor[j] != jogador:
			return None
	
	return ind

def criterio_vitoria(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_vitoria: algum dos argumentos e invalido")

	for i in range(1, DIMENSAO_TABULEIRO):
		linha = obter_linha(tab, i)
		ind = obter_indice_para_completar_vetor(linha, jogador)
		if ind is not None:
			return ind + 1 + (i - 1) * DIMENSAO_TABULEIRO
		
		col = obter_coluna(tab, i)
		ind = obter_indice_para_completar_vetor(col, jogador)
		if ind is not None:
			return ind
	
	for i in range(1, 3):
		diag = obter_diagonal(tab, i)
		ind = obter_indice_para_completar_vetor(diag, jogador)
		if ind is not None:
			return ind

def criterio_bloqueio(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bloqueio: algum dos argumentos e invalido")

	# TODO
	return 1

def criterio_bifurcacao(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bifurcacao: algum dos argumentos e invalido")

	# TODO
	return 1

def criterio_bloqueio_bifurcacao(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bloqueio_bifurcacao: " + \
			"algum dos argumentos e invalido")

	# TODO
	return 1

def criterio_centro(tab, jogador): # aux
	if not eh_tabuleiro(tab):
		raise ValueError("criterio_centro: o argumento e invalido")

	centro = obter_centro()
	if eh_posicao_livre(tab, centro):
		return centro

def criterio_canto_oposto(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_canto_oposto: " + \
			"algum dos argumentos e invalido")

	# TODO
	return 1

def criterio_canto_vazio(tab, jogador): # aux
	if not eh_tabuleiro(tab):
		raise ValueError("criterio_canto_vazio: o argumento e invalido")

	cantos = obter_cantos()

	for pos in cantos:
		if eh_posicao_livre(tab, pos):
			return pos

def criterio_lateral_vazio(tab, jogador): # aux
	if not eh_tabuleiro(tab):
		raise ValueError("criterio_lateral_vazio: o argumento e invalido")

	cantos = obter_cantos()
	centro = obter_centro()

	for pos in range(1, DIMENSAO_TABULEIRO ** 2 + 1):
		if pos != centro and (pos not in cantos) and eh_posicao_livre(tab, pos):
			return pos

def escolher_posicao_auto(tab, jogador, estrategia):
	if not (eh_tabuleiro(tab) and eh_jogador(jogador) \
		and eh_estrategia(estrategia)):
		raise ValueError("escolher_posicao_auto: " + \
			"algum dos argumentos e invalido")
	
	crits_perfeitos = estrategia == "perfeito"
	crits_normais = crits_perfeitos or estrategia == "normal"
	crits_basicos = crits_normais or estrategia == "basico"

	criterios = (
		# tentar aplicar (bool), criterio (function)
		(crits_normais, criterio_vitoria),
		(crits_normais, criterio_bloqueio),
		(crits_perfeitos, criterio_bifurcacao),
		(crits_perfeitos, criterio_bloqueio_bifurcacao),
		(crits_basicos, criterio_centro),
		(crits_normais, criterio_canto_oposto),
		(crits_basicos, criterio_canto_vazio),
		(crits_basicos, criterio_lateral_vazio)
	)

	for el in criterios:
		if el[0]:
			pos = (el[1])(tab, jogador)
			if pos:
				return pos
	
	raise RuntimeError("escolher_posicao_auto: nenhum criterio foi aplicado")