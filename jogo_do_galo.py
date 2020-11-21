# 99311 Rafael Serra e Oliveira

# CONVENCAO DE VOCABULARIO
# vetor: linha ou coluna
# posicao: 1 ... 9 (para dimensao = 3)
# jogador: -1, 0, 1
# simbolo: O, _, X (espaco para vazio)

DIMENSAO_TABULEIRO = 3 # Quantas celulas ha em cada linha/coluna/diagonal

# Algumas funcoes podiam ser variaveis globais, mas o prof. Joao Martins Pavao
# pediu para ter o minimo de variaveis globais possiveis

def eh_vetor(tab): # aux
	if type(tab) == tuple:
		if len(tab) == DIMENSAO_TABULEIRO:
			for el in tab:
				if type(el) != int:
					return False
				elif abs(el) > 1:
					return False
			
			return True
	
	return False

def eh_tabuleiro(tab):
	if type(tab) == tuple:
		if len(tab) == DIMENSAO_TABULEIRO:
			for el in tab:
				if not eh_vetor(el):
					return False
			
			return True
	return False

def obter_posicoes(): # aux
	return range(1, DIMENSAO_TABULEIRO ** 2 + 1)

def eh_posicao(pos):
	return type(pos) == int and pos in obter_posicoes()

def eh_numero_de_vetor(num): # aux
	return type(num) == int and 1 <= num <= DIMENSAO_TABULEIRO

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

def obter_posicoes_livres(tab):
	if not eh_tabuleiro(tab):
		raise ValueError("obter_posicoes_livres: o argumento e invalido")

	livres = ()
	for pos in obter_posicoes():
		if eh_posicao_livre(tab, pos):
			livres = livres + (pos,)
	
	return livres

def vetor_ganhador(vetor): # aux
	if not eh_vetor(vetor):
		raise ValueError("vetor_ganhador: o argumento e invalido")

	jogador = vetor[0]

	if (jogador != 0) and (vetor == (jogador,) * len(vetor)):
		return jogador
	else:
		return 0

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
	return type(jogador) == int and abs(jogador) == 1

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
	return type(estrategia) == str and estrategia in (
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
		DIMENSAO_TABULEIRO * (DIMENSAO_TABULEIRO - 1) + 1,
		DIMENSAO_TABULEIRO ** 2,
	)

def criterio_vitoria(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_vitoria: algum dos argumentos e invalido")

	for pos in obter_posicoes():
		if eh_posicao_livre(tab, pos) \
			and jogador_ganhador(marcar_posicao(tab, jogador, pos)) == jogador:
			return pos

def criterio_bloqueio(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bloqueio: algum dos argumentos e invalido")

	return criterio_vitoria(tab, -jogador)

def obter_bifurcacoes(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("obter_bifurcacoes: algum dos argumentos e invalido")

	cantos = obter_cantos()
	bifurcacoes = ()
	for pos in obter_posicoes():
		if eh_posicao_livre(tab, pos):
			coords = obter_coordenadas(pos)
			linha = obter_linha(tab, coords[0] + 1)
			col = obter_coluna(tab, coords[1] + 1)
			diag = ()
			lc = len(cantos)
			for i in range(lc):
				if cantos[i] == pos:
					diag = obter_diagonal(tab, 2 if 1 < i + 1 < lc else 1)
			vfs = ( # verificacoes, 2+ tem que ser True para haver bifurcacao
				linha.count(0) == 2 and linha.count(-jogador) == 0,
				col.count(0) == 2 and col.count(-jogador) == 0,
				diag.count(0) == 2 and diag.count(-jogador) == 0,
			)
			if (vfs[0] and (vfs[1] or vfs[2])) or (vfs[1] and vfs[2]):
				bifurcacoes = bifurcacoes + (pos,)
	
	return bifurcacoes

def criterio_bifurcacao(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bifurcacao: algum dos argumentos e invalido")

	bifurcacoes = obter_bifurcacoes(tab, jogador)
	if len(bifurcacoes) > 0:
		return bifurcacoes[0]

def obter_posicao_de_coordenadas(coords): # aux
	if not (type(coords) == tuple and len(coords) == 2 \
		and 0 <= coords[0] <= DIMENSAO_TABULEIRO - 1 \
		and 0 <= coords[1] <= DIMENSAO_TABULEIRO - 1):
		raise ValueError("obter_posicao_de_coordenadas: o argumento e invalido")
	
	return coords[0] * DIMENSAO_TABULEIRO + coords[1] + 1

def obter_posicoes_adjacentes(pos): # aux
	if not eh_posicao(pos):
		raise ValueError("obter_posicoes_adjacentes: o argumento e invalido")

	adjs = ()
	coords = obter_coordenadas(pos)
	for i in range(coords[0] - 1, coords[0] + 2):
		if 0 <= i <= (DIMENSAO_TABULEIRO - 1):
			for j in range(coords[1] - 1, coords[1] + 2):
				if 0 <= j <= (DIMENSAO_TABULEIRO - 1) and (i, j) != coords:
					p = obter_posicao_de_coordenadas((i, j))
					if p not in adjs:
						adjs = adjs + (p,)
	
	return adjs

def criterio_bloqueio_bifurcacao(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_bloqueio_bifurcacao: " + \
			"algum dos argumentos e invalido")

	bifurcacoes = obter_bifurcacoes(tab, -jogador)
	lb = len(bifurcacoes)
	if lb == 1:
		return bifurcacoes[0]
	elif lb > 1:
		posicoes_para_2_em_linha = ()
		for pos in obter_posicoes():
			if obter_jogador(tab, pos) == jogador:
				for adj in obter_posicoes_adjacentes(pos):
					if eh_posicao_livre(tab, adj) \
						and adj not in posicoes_para_2_em_linha:
						posicoes_para_2_em_linha += (adj,)
		for pos in posicoes_para_2_em_linha:
				novo_tab = marcar_posicao(tab, jogador, pos)
				if criterio_bloqueio(novo_tab, -jogador) not in bifurcacoes:
					return pos

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

	cantos = obter_cantos()

	for i in range(len(cantos)):
		oposto = len(cantos) - 1 - i
		if eh_posicao_livre(tab, cantos[i]) \
			and obter_jogador(tab, cantos[oposto]) == -jogador:
			return cantos[i]

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

	for pos in obter_posicoes():
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

def eh_simbolo(simbolo):
	return type(simbolo) == str and simbolo in ('X', 'O')

def converter_simbolo_em_jogador(simbolo):
	if not eh_simbolo(simbolo):
		raise ValueError("converter_simbolo_em_jogador: o argumento e invalido")

	return ({'X': 1, 'O': -1})[simbolo]

def jogo_do_galo(simbolo_humano, estrategia):
	if not (eh_simbolo(simbolo_humano) and eh_estrategia(estrategia)):
		raise ValueError("jogo_do_galo: algum dos argumentos e invalido")

	jogador_humano = converter_simbolo_em_jogador(simbolo_humano)

	print("Bem-vindo ao JOGO DO GALO.")
	print("O jogador joga com '" + simbolo_humano + "'.")

	jogador_atual = 1
	tabuleiro = ((0,) * DIMENSAO_TABULEIRO,) * DIMENSAO_TABULEIRO

	while True:
		escolha = None
		if jogador_atual == jogador_humano:
			escolha = escolher_posicao_manual(tabuleiro)
		else:
			print('Turno do computador (' + estrategia + '):')
			escolha = escolher_posicao_auto(
				tabuleiro,
				jogador_atual,
				estrategia
			)

		tabuleiro = marcar_posicao(tabuleiro, jogador_atual, escolha)
		print(tabuleiro_str(tabuleiro))

		ganhador = jogador_ganhador(tabuleiro)
		if ganhador:
			return simbolo_str(ganhador)
		elif len(obter_posicoes_livres(tabuleiro)) == 0:
			return 'EMPATE'
		
		jogador_atual = -jogador_atual