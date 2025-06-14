import os

class Cor:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'
    ROXO = '\033[95m'

class Moore:
    def __init__(self, arquivo_entrada):
        self.transicoes = {}
        self.saidas = {
            "I": "🔲 Mistura vazia, caldeirão pronto para uso.",
            "M1": "🧪 Um brilho leve surge da mistura...",
            "M2": "✨ A poção borbulha suavemente e exala aroma doce.",
            "M3": "🌈 A mistura flutua e cintila com cores mágicas!",
            "F_bolo": "🎂 Você criou um Bolo Místico!",
            "F_cha": "🍵 Você preparou um Chá Mágico!",
            "F_sorvete": "🍨 Você invocou um Sorvete dos Sonhos!",
            "F_pizza": "🍕 Você assou uma Pizza de Magma!",
            "F_sopa": "🥣 Você cozinhou uma Sopa Encantada!",
            "erro": "💥 Erro! A mistura se desfez em fumaça negra!"
        }
        self.carregar(arquivo_entrada)
        self.estado_atual = self.estado_inicial

    def carregar(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        
        self.estados = linhas[0].split(":")[1].strip().split()
        self.estado_inicial = linhas[1].split(":")[1].strip()
        self.estado_final = linhas[2].split(":")[1].strip()  # usado simbolicamente

        for linha in linhas[3:]:
            if linha == "---":
                break
            origem, resto = linha.split("->")
            destino, simbolos = resto.strip().split("|")
            simbolos = simbolos.strip().split()
            for simbolo in simbolos:
                self.transicoes[(origem.strip(), simbolo.strip())] = destino.strip()

    def executar(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(Cor.ROXO + """
╭──────────────────────────────────────────────────╮
│ """ + Cor.NEGRITO + Cor.AMARELO + "✨🍳 MÁQUINA DE MOORE: A Cozinha Encantada! 🍲✨" + Cor.ROXO + """ │
╰──────────────────────────────────────────────────╯
""" + Cor.RESET)

        print(Cor.AMARELO + f"\n{self.saidas[self.estado_atual]}" + Cor.RESET)

        ultimo_ingrediente = ""
        estado_anterior = ""

        while self.estado_atual != "erro":
            self.exibir_ingredientes()
            ingrediente = input("\n🧾 Adicione um ingrediente mágico: ").strip()
            chave = (self.estado_atual, ingrediente)

            if chave not in self.transicoes:
                print(Cor.VERMELHO + "❌ Transição inválida!" + Cor.RESET)
                estado_anterior = self.estado_atual
                self.estado_atual = "erro"
                ultimo_ingrediente = ingrediente
                break

            estado_anterior = self.estado_atual
            self.estado_atual = self.transicoes[chave]
            ultimo_ingrediente = ingrediente

            print(Cor.AZUL + f"\n📍 Novo estado: {self.estado_atual}" + Cor.RESET)
            print(Cor.AMARELO + f"{self.saidas.get(self.estado_atual, '')}" + Cor.RESET)

            if self.estado_atual.startswith("F_"):
                print(Cor.VERDE + "\n✅ Receita concluída com sucesso!" + Cor.RESET)
                return

            if self.estado_atual == "erro":
                break

            continuar = input("➕ Adicionar outro ingrediente? (s/n): ").lower()
            if continuar != 's':
                break

        if self.estado_atual == "erro":
            if estado_anterior == "M3" and ultimo_ingrediente == "f":
                print(Cor.VERMELHO + "\n⚠️ Poeira de Fada usada no final corrompeu a comida!" + Cor.RESET)
            else:
                print(Cor.VERMELHO + "\n💥 A receita falhou! O caldeirão explodiu!" + Cor.RESET)
        elif not self.estado_atual.startswith("F_"):
            print(Cor.VERMELHO + "\n❌ Mistura incompleta! A receita não pôde ser finalizada." + Cor.RESET)

    def exibir_ingredientes(self):
        print("\n" + Cor.AMARELO + "-" * 50 + Cor.RESET)
        print(Cor.AMARELO+ "📦 Ingredientes mágicos disponíveis:" + Cor.RESET)
        print(f" {Cor.VERDE}p{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.ROXO}Pétalas de Fênix{Cor.RESET}")
        print(f" {Cor.VERDE}e{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.AZUL}Essência de Gelo{Cor.RESET}")
        print(f" {Cor.VERDE}n{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.ROXO}Néctar de Estrela{Cor.RESET}")
        print(f" {Cor.VERDE}f{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.AZUL}Poeira de Fada{Cor.RESET}")
        print(f" {Cor.VERDE}c{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.ROXO}Cristal de Maná{Cor.RESET}")
        print(f" {Cor.VERDE}l{Cor.RESET} {Cor.AZUL}→{Cor.RESET} {Cor.AZUL}Lágrima de Dragão{Cor.RESET}")
        print(Cor.AMARELO + "-" * 50 + Cor.RESET)



def rodar():
    maquina = Moore("entrada_moore.txt")
    maquina.executar()

if __name__ == "__main__":
    rodar()
