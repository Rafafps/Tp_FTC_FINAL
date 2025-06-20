RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

class TuringPalindromoMagico:
    def __init__(self, fita):
        self.fita = list(fita) + ['_']  # Adiciona espaço branco ao final
        self.pos = 0
        self.estado = 'inicio'

    def mostrar_fita(self):
        fita_str = ''.join(self.fita)
        marcador = ' ' * self.pos + '^'
        print(f"\n{MAGENTA}Fita:{RESET} {fita_str}\n      {marcador} (Estado: {self.estado})")

    def executar(self):
        print("\n" + CYAN + "✦✧" * 35)
        print(MAGENTA + "🎩✨ Iniciando o truque mágico de reconhecimento de palíndromo... ✨🎩")
        print(CYAN + "✦✧" * 35 + RESET +"\n")

        while True:
            self.mostrar_fita()

            if self.estado == 'inicio':
                if self.fita[self.pos] in ['a', 'b', 'c']:
                    simbolo = self.fita[self.pos]
                    print(f"🔎 Marcando esquerda: '{simbolo}'")
                    self.fita[self.pos] = 'X'
                    self.estado = f'buscar_{simbolo}'
                    self.pos += 1
                elif self.fita[self.pos] in ['X', '_']:
                    print("\n✅ Palíndromo confirmado! O truque foi um sucesso! 🎉")
                    break
                else:
                    print(f"\n💥 Símbolo inválido encontrado: '{self.fita[self.pos]}'. Truque falhou!")
                    break

            elif self.estado.startswith('buscar_'):
                alvo = self.estado.split('_')[1]
                while self.fita[self.pos] not in ['_', 'X']:
                    self.pos += 1
                # Se chegou no branco direto (ex: tamanho ímpar como 'a')
                if self.fita[self.pos] == '_':
                    self.pos -= 1
                    self.estado = f'comparar_{alvo}'
                elif self.fita[self.pos] == 'X':
                    self.pos -= 1
                    self.estado = f'comparar_{alvo}'

            elif self.estado.startswith('comparar_'):
                alvo = self.estado.split('_')[1]
                if self.fita[self.pos] == alvo:
                    print(f"✨ Par confirmado: '{alvo}' na direita.")
                    self.fita[self.pos] = 'X'
                    self.estado = 'retornar'
                    self.pos -= 1
                elif self.fita[self.pos] in ['X']:
                    # Caso especial: se a cabeça parou sobre um X, significa que só havia um símbolo (caso ímpar)
                    print(f"✨ Ponto intermediário alcançado. Prosseguindo.")
                    self.estado = 'retornar'
                else:
                    print(f"\n💥 Erro! Esperava '{alvo}', mas encontrou '{self.fita[self.pos]}'. Truque falhou!")
                    break

            elif self.estado == 'retornar':
                while self.pos >= 0 and self.fita[self.pos] != 'X':
                    self.pos -= 1
                self.pos += 1
                self.estado = 'inicio'

# Execução:
if __name__ == "__main__":
    entrada = input("🔮 Digite a sequência mágica (apenas com a, b, c - ex: aba, abcba, a): ").strip().replace(' ', '')
    mt = TuringPalindromoMagico(entrada)
    mt.executar()
