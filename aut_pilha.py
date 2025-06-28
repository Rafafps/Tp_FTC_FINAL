import os

class Cor:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

class AutomatoDePilha:
    def __init__(self, caminho_arquivo=None):
        self.pilha = []
        self.mistura = []
        self.estado = None
        self.estado_final = None
        self.estado_inicial = None
        self.estado_erro = "erro"
        self.estados = set()
        self.transicoes = {}

        if caminho_arquivo:
            self.carregar_automato(caminho_arquivo)
        else:
            self.estado = "I"
            self.estado_final = "F"

    def carregar_automato(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        self.estados = set(linhas[0][2:].strip().split())
        self.estado = linhas[1][2:].strip()
        self.estado_inicial = self.estado
        self.estado_final = linhas[2][2:].strip()

        self.transicoes = {}
        for linha in linhas[3:]:
            if linha == "---":
                break
            origem, resto = linha.split("->")
            destino, simbolos = resto.split("|")
            origem = origem.strip()
            destino = destino.strip()
            simbolos = simbolos.strip().split()
            for simbolo in simbolos:
                self.transicoes[(origem, simbolo)] = destino

        print(f"DEBUG: Estados carregados: {self.estados}")
        print(f"DEBUG: Estado inicial: {self.estado}")
        print(f"DEBUG: Estado final: {self.estado_final}")
        print(f"DEBUG: Transições carregadas:")
        for chave, valor in self.transicoes.items():
            print(f"  {chave} -> {valor}")

    def mostrar_interface(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(Cor.AZUL + r"""
  ____        _         _           
 |  _ \  __ _| |_ _   _| | ___  ___ 
 | | |/ _` | __| | | | | |/ _ \/ __|
 | |_| (_| | |_| |_| | |  __/\__ \
 |____\__,_|\__|\__, |_|\___||___/
                 |___/              
        """ + Cor.RESET)
        print(Cor.NEGRITO + "\n🧪  SIMULADOR DE AUTÔMATO DE PILHA - Poções Mágicas\n" + Cor.RESET)
        print("-" * 60)
        print("Ingredientes disponíveis:")
        print(" 🧱 f → farelo       → aumenta temperatura (🔥)")
        print(" 🩸 s → sangue       → coloração vermelha (🟥)")
        print(" 🧤 c → carvão       → reduz temperatura (❄️)")
        print(" 💧 a → água         → neutraliza a última reação da pilha")
        print(" 🌸 p → pétalas      → aroma floral")
        print(Cor.AMARELO + "\n⚠️  A ordem dos ingredientes afeta a mistura final!" + Cor.RESET)
        print("-" * 60)

    def aplicar_entrada(self, simbolo):
        simbolo = simbolo.lower()
        if simbolo not in ['f', 's', 'c', 'a', 'p']:
            print(Cor.VERMELHO + "❌ Símbolo inválido! Use apenas f, s, c, a, p." + Cor.RESET)
            self.estado = self.estado_erro
            return

        proximo_estado = self.transicoes.get((self.estado, simbolo), self.estado_erro)
        print(f"DEBUG: Transição ({self.estado}, {simbolo}) -> {proximo_estado}")

        if proximo_estado == self.estado_erro:
            print(Cor.VERMELHO + "❌ Ingrediente inválido ou transição não permitida!" + Cor.RESET)
            self.estado = self.estado_erro
            return

        self.estado = proximo_estado
        self.mistura.append(simbolo)

        if simbolo == 'f':
            self.pilha.append('🔥 quente')
            print("🔥 Reação: temperatura aumentada.")
        elif simbolo == 's':
            self.pilha.append('🟥 vermelho')
            print("🟥 Reação: coloração vermelha adicionada.")
        elif simbolo == 'c':
            if '🔥 quente' in self.pilha:
                self.pilha.remove('🔥 quente')
                print("❄️ Reação: temperatura resfriada.")
            else:
                self.pilha.append('❄️ frio')
                print("❄️ Reação: mistura ficou fria.")
        elif simbolo == 'a':
            if self.pilha:
                removido = self.pilha.pop()
                print(f"💧 Reação: '{removido}' foi neutralizado com água.")
            else:
                print("💧 Nada para neutralizar.")
        elif simbolo == 'p':
            self.pilha.append('🌸 floral')
            print("🌸 Reação: aroma floral adicionado.")

    def executar(self):
        self.mostrar_interface()

        while self.estado != self.estado_erro:
            print(Cor.VERDE + f"\n📍 Mistura atual: {', '.join(self.mistura) if self.mistura else '(vazia)'}" + Cor.RESET)
            print(Cor.AZUL + "📦 Pilha de reações:", ', '.join(self.pilha) if self.pilha else "(vazia)" + Cor.RESET)

            simbolo = input("🧾 Insira um ingrediente (f, s, c, a, p): ").strip().lower()
            self.aplicar_entrada(simbolo)

            if self.estado == self.estado_final:
                print(Cor.VERDE + "\n✅ Estado final alcançado." + Cor.RESET)
                break

            continuar = input("➕ Deseja inserir mais um ingrediente (s/n)? ").strip().lower()
            if continuar != 's':
                break

        print(Cor.NEGRITO + "\n🧪 Resultado Final da Mistura:" + Cor.RESET)
        print(Cor.AZUL + "📍 Ingredientes utilizados:", ', '.join(self.mistura) + Cor.RESET)
        print(Cor.AZUL + "📦 Pilha final:", ', '.join(self.pilha) if self.pilha else "Sem reações ativas." + Cor.RESET)

        if self.estado == self.estado_erro:
            print(Cor.VERMELHO + "\n❌ Erro na mistura: ingrediente inválido ou sequência inválida!" + Cor.RESET)
            print('\033[5m' + '⚠️ Mistura instável!' + '\033[0m')
        else:
            print(Cor.VERDE + "✅ Mistura finalizada com sucesso!" + Cor.RESET)

def rodar():
    maquina = AutomatoDePilha("entrada_pilha.txt")
    maquina.executar()