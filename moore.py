import os

class Cor:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

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
            "erro": "💥 Explosão de sabores descontrolados!"
        }
        self.carregar(arquivo_entrada)
        self.estado_atual = self.estado_inicial

    def carregar(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        
        self.estados = linhas[0].split(":")[1].strip().split()
        self.estado_inicial = linhas[1].split(":")[1].strip()
        self.estado_final = linhas[2].split(":")[1].strip()  # Um dos finais, mas aceitamos vários
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
        print(Cor.NEGRITO + "\n🍳 MÁQUINA DE MOORE: Cozinha Encantada!\n" + Cor.RESET)
        print("-" * 50)
        print("Ingredientes mágicos disponíveis:")
        print(" p → Pétalas de Fênix")
        print(" e → Essência de Gelo")
        print(" n → Néctar de Estrela")
        print(" f → Poeira de Fada")
        print(" c → Cristal de Maná")
        print(" l → Lágrima de Dragão")
        print("-" * 50)

        print(Cor.AMARELO + f"\n{self.saidas[self.estado_atual]}" + Cor.RESET)

        while self.estado_atual != "erro":
            ingrediente = input("\n🧾 Adicione um ingrediente mágico: ").strip()
            chave = (self.estado_atual, ingrediente)

            if chave not in self.transicoes:
                print(Cor.VERMELHO + "❌ Transição inválida!" + Cor.RESET)
                self.estado_atual = "erro"
                break

            self.estado_atual = self.transicoes[chave]
            print(Cor.AZUL + f"\n📍 Novo estado: {self.estado_atual}" + Cor.RESET)
            print(Cor.AMARELO + f"{self.saidas.get(self.estado_atual, '')}" + Cor.RESET)

            # Aqui detecta se chegou a um estado final e encerra
            if self.estado_atual.startswith("F_"):
                print(Cor.VERDE + "\n✅ Receita concluída com sucesso!" + Cor.RESET)
                break

            # Caso não tenha finalizado ainda, pergunta se deseja continuar
            continuar = input("➕ Adicionar outro ingrediente? (s/n): ").lower()
            if continuar != 's':
                break


        if self.estado_atual == "erro":
            print(Cor.VERMELHO + "\n💥 A receita falhou! O caldeirão explodiu!" + Cor.RESET)

def rodar():
    maquina = Moore("entrada_moore.txt")
    maquina.executar()   

if __name__ == "__main__":
    rodar()
