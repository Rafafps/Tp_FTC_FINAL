import os

class Cor:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

class MaquinaDeMoore:
    def __init__(self, caminho_arquivo):
        self.estados = set()
        self.estado_inicial = ""
        self.estado_final = ""
        self.estado_erro = "erro"
        self.transicoes = {}
        self.saidas = {}
        self.carregar_moore(caminho_arquivo)

    def carregar_moore(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]


        self.estados = set(linhas[0][3:].split())
        self.estado_inicial = linhas[1].split(":")[1].strip()
        self.estado_final = linhas[2].split(":")[1].strip()
        self.saidas = {}
        saida_raw = linhas[3][2:].split()
        estado_atual = None

        for item in saida_raw:
            if ':' in item:
                estado, valor = item.split(":", 1)
                estado_atual = estado
                self.saidas[estado] = valor
            else:
                # Continua a saída anterior (caso contenha espaços ou emojis)
                if estado_atual:
                    self.saidas[estado_atual] += " " + item


        for linha in linhas[4:]:
            if linha == "---":
                break
            origem, resto = linha.split("->")
            destino, simbolos = resto.split("|")
            origem = origem.strip()
            destino = destino.strip()
            simbolos = simbolos.strip().split()
            for simbolo in simbolos:
                self.transicoes[(origem, simbolo)] = destino

    def executar(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(Cor.AZUL + r"""
╭──────────────────────────────────────────╮
│ 🍜 MÁQUINA DE MOORE - LÁMEN GOURMET 🍜  │
╰──────────────────────────────────────────╯
""" + Cor.RESET)

        estado_atual = self.estado_inicial
        ingredientes = []

        while True:
            saida = self.saidas.get(estado_atual, 'sem efeito')
            print(f"\n{Cor.NEGRITO}📍 Estado atual: {Cor.AZUL}{estado_atual}{Cor.RESET} → {Cor.VERDE}{saida}{Cor.RESET}")
            simbolo = input("🧾 Ingrediente (c, m, t, o, a): ").strip().lower()
            ingredientes.append(simbolo)

            proximo_estado = self.transicoes.get((estado_atual, simbolo), self.estado_erro)
            print(f"➡️  Transição: ({estado_atual}, '{simbolo}') → {proximo_estado}")
            estado_atual = proximo_estado

            if estado_atual == self.estado_erro:
                print(Cor.VERMELHO + "\n❌ Erro na mistura!" + Cor.RESET)
                break

            continuar = input("➕ Deseja inserir mais um ingrediente (s/n)? ").strip().lower()
            if continuar != 's':
                break

        print(Cor.NEGRITO + "\n🧪 Resultado Final:" + Cor.RESET)
        print(Cor.AZUL + "📜 Ingredientes usados: " + ', '.join(ingredientes) + Cor.RESET)
        print(Cor.VERDE + f"📍 Estado final: {estado_atual}" + Cor.RESET)
        print(Cor.VERDE + f"🔊 Efeito: {self.saidas.get(estado_atual, 'desconhecido')}" + Cor.RESET)

        if estado_atual == self.estado_final:
            print(Cor.VERDE + "\n✅ Lámen preparado com sucesso!" + Cor.RESET)
        else:
            print(Cor.VERMELHO + "\n❌ Receita incompleta ou inválida!" + Cor.RESET)


def rodar():
    moore = MaquinaDeMoore("entrada_moore.txt")
    moore.executar()


if os.path.exists("entrada_moore.txt"):
    rodar()
else:
    print(Cor.VERMELHO + "❌ Arquivo 'entrada_moore.txt' não encontrado!" + Cor.RESET)

