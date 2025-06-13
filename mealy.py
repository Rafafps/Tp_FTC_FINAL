import os

class Cor:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    NEGRITO = '\033[1m'
    RESET = '\033[0m'

class Mealy:
    def __init__(self, arquivo_entrada):
        self.estado_atual = "I"
        self.estado_final = "F"
        self.estado_erro = "erro"
        self.transicoes = {}
        self.carregar(arquivo_entrada)

    def carregar(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        
        self.estado_inicial = linhas[1].split(":")[1].strip()
        self.estado_final = linhas[2].split(":")[1].strip()
        
        for linha in linhas[3:]:
            if linha == "---":
                break
            origem, resto = linha.split("->")
            destino, simbolo_saida = resto.strip().split("|")
            simbolo, saida = simbolo_saida.strip().split(":", 1)
            self.transicoes[(origem.strip(), simbolo.strip())] = (destino.strip(), saida.strip())

    def executar(self):
        os.system("cls" if os.name == "nt" else "clear")

        print(Cor.NEGRITO + "\n🧙 MÁQUINA MEALY: Vestindo o Mago!\n" + Cor.RESET)
        print("-" * 50)
        print("Ingredientes disponíveis:")
        print(" c → Capa mágica")
        print(" t → Túnica arcana")
        print(" l → Luvas lunares")
        print(" o → Olhos de vampiro")
        print(" b → Botas assustadoras")
        print(" coroa → Coroa encantada")
        print("-" * 50)

        historia = []

        while self.estado_atual != self.estado_erro:
            print(Cor.VERDE + f"\n📍 Estado atual: {self.estado_atual}" + Cor.RESET)
            entrada = input("🧾 Escolha um item mágico: ").strip()

            chave = (self.estado_atual, entrada)
            if chave not in self.transicoes:
                print(Cor.VERMELHO + "❌ Transição inválida!" + Cor.RESET)
                self.estado_atual = self.estado_erro
                break

            novo_estado, saida = self.transicoes[chave]
            print(f"✨ {saida}")
            historia.append(saida)
            self.estado_atual = novo_estado

            if self.estado_atual == self.estado_final:
                print(Cor.VERDE + "\n✅ Transformação completa!" + Cor.RESET)
                break

            continuar = input("➕ Adicionar outro item? (s/n): ").lower()
            if continuar != 's':
                break

        print("\n" + Cor.NEGRITO + "🧙 RESUMO DA TRANSFORMAÇÃO:" + Cor.RESET)
        for i, parte in enumerate(historia, 1):
            print(f"{i}. {parte}")

        if self.estado_atual == self.estado_erro:
            print(Cor.VERMELHO + "\n❌ A combinação falhou... O maguinho ficou confuso!" + Cor.RESET)

def rodar():
    maquina = Mealy("entrada_mealy.txt")
    maquina.executar()

if __name__ == "__main__":
    rodar()
