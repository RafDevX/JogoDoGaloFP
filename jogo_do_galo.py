# 99311 Rafael Serra e Oliveira

def eh_linha_de_tabuleiro(tab): # aux
	if isinstance(tab, tuple):
		if len(tab) == 3:
			for el in tab:
				if not isinstance(el, int):
					return False
				elif abs(el) > 1:
					return False
			
			return True
	
	return False

def eh_tabuleiro(tab):
	if isinstance(tab, tuple):
		if len(tab) == 3:
			for el in tab:
				if not eh_linha_de_tabuleiro(el):
					return False
			
			return True
	return False

def eh_posicao(pos):
	return isinstance(pos, int) and 1 <= pos <= 9

def eh_numero_de_vetor(num): # aux
	return isinstance(num, int) and 1 <= num <= 3

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