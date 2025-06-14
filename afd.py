import os

# Cores ANSI (compatíveis com terminais modernos)
class Cor:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

class AFD:
    def __init__(self, caminho_arquivo):
        self.estados = set()
        self.estado_inicial = ""
        self.estado_final = ""
        self.transicoes = {}
        self.estado_erro = ""
        self.carregar_afd(caminho_arquivo)

    def carregar_afd(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        
        self.estados = set(linhas[0][3:].split())
        self.estado_inicial = linhas[1].split(":")[1].strip()
        self.estado_final = linhas[2].split(":")[1].strip()

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

        self.estado_erro = next((estado for estado in self.estados if "erro" in estado.lower()), None)

    def mostrar_ascii(self):
        print(Cor.AZUL + r"""
     ____       _ _     _              
    |  _ \ __ _(_) | __| | ___ _ __  _   _ 
    | |_) / _` | | |/ _` |/ _ \ '_ \| | | |
    |  __/ (_| | | | (_| |  __/ | | | |_| |
    |_|   \__,_|_|_|\__,_|\___|_| |_|\__,_|            
        """ + Cor.RESET)

    def mostrar_transicoes(self):
        print(Cor.NEGRITO + "\nTabela de Transições:\n" + Cor.RESET)
        for (origem, simbolo), destino in self.transicoes.items():
            print(f"  ({origem}, '{simbolo}') → {destino}")
        print()

    def exibir_interface(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.mostrar_ascii()
        print(Cor.NEGRITO + "🧪  SIMULADOR DE PRODUÇÃO DE POÇÕES - Poções Mágicas" + Cor.RESET)
        print("-" * 50)
        print("Ingredientes disponíveis:")
        print(" - a (água)")
        print(" - p (pétalas)")
        print(" - o (óleo)")
        print(Cor.AMARELO + "\n⚠️  Água e óleo não podem estar na mesma receita." + Cor.RESET)
        print("💡 Receita válida: a p p  (Poção de restauração comum)")
        print("-" * 50)
        self.mostrar_transicoes()

    def executar(self):
        self.exibir_interface()

        estado_atual = self.estado_inicial
        ingredientes = []

        while True:
            print(Cor.VERDE + f"\n📍 Estado atual: {estado_atual}" + Cor.RESET)
            simbolo = input("🧾 Insira o símbolo do ingrediente (a, p, o): ").strip()
            ingredientes.append(simbolo)

            proximo_estado = self.transicoes.get((estado_atual, simbolo), self.estado_erro)
            print(f"➡️  Transição: ({estado_atual}, '{simbolo}') → {proximo_estado}")
            estado_atual = proximo_estado

            if estado_atual == self.estado_erro:
                print(Cor.VERMELHO + "\n❌ Erro na mistura: ingrediente inválido!" + Cor.RESET)
                break

            continuar = input("➕ Deseja inserir mais um ingrediente (s/n)? ").strip().lower()
            if continuar != 's':
                if estado_atual == self.estado_final:
                    print(Cor.VERDE + "\n✅ Mistura finalizada com sucesso!" + Cor.RESET)
                    print('\033[5m' + '⚠️ Mistura instável!' + '\033[0m')
                else:
                    print(Cor.VERMELHO + "\n❌ Erro na mistura: sequência incompleta ou inválida." + Cor.RESET)
                break

def rodar():
    afd = AFD("entrada.txt")
    afd.executar()
