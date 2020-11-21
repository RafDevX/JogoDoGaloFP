# OLD criterio_vitoria
# Mais eficiente, mais confuso

def obter_indice_para_completar_vetor(vetor, jogador): # aux
	if not (eh_vetor(vetor) and eh_jogador(jogador)):
		raise ValueError("obter_indice_para_completar_vetor: " \
			+ "algum dos argumentos e invalido")
	
	ind = None
	for j in range(len(vetor)):
		if vetor[j] == 0:
			if ind is None:
				ind = j
			else:
				return None
		elif vetor[j] != jogador:
			return None
	return ind

def criterio_vitoria(tab, jogador): # aux
	if not (eh_tabuleiro(tab) and eh_jogador(jogador)):
		raise ValueError("criterio_vitoria: algum dos argumentos e invalido")

	for i in range(1, DIMENSAO_TABULEIRO + 1):
		linha = obter_linha(tab, i)
		ind = obter_indice_para_completar_vetor(linha, jogador)
		if ind is not None:
			return ind + 1 + (i - 1) * DIMENSAO_TABULEIRO
		
		col = obter_coluna(tab, i)
		ind = obter_indice_para_completar_vetor(col, jogador)
		if ind is not None:
			return i + ind * DIMENSAO_TABULEIRO
	
	diag1 = obter_diagonal(tab, 1)
	ind = obter_indice_para_completar_vetor(diag1, jogador)
	if ind is not None:
		return 1 + ind * (DIMENSAO_TABULEIRO + 1)

	diag2 = obter_diagonal(tab, 2)
	ind = obter_indice_para_completar_vetor(diag2, jogador)
	if ind is not None:
		return 1 + (DIMENSAO_TABULEIRO - ind) * (DIMENSAO_TABULEIRO - 1)