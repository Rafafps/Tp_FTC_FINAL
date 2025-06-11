import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QMessageBox, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from afd import AFD
from aut_pilha import AutomatoDePilha

# Ajuste os nomes dos ingredientes e imagens conforme sua pasta 'imagens/'
INGREDIENTES = [
    {"nome": "Água", "simbolo": "a", "img": "imagens/water.png"},
    {"nome": "Pétalas", "simbolo": "p", "img": "imagens/petals.png"},
    {"nome": "Óleo", "simbolo": "o", "img": "imagens/oil.png"},
    {"nome": "Farelo", "simbolo": "f", "img": "imagens/bonemeal.png"},
    {"nome": "Sangue", "simbolo": "s", "img": "imagens/blood.png"},
    {"nome": "Carvão", "simbolo": "c", "img": "imagens/coal.png"},
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Simulador de Poções Mágicas")
        self.setGeometry(200, 100, 1000, 600)
        self.setStyleSheet("background-color: #23272e; color: white;")
        self.poção_atual = []  # Lista de símbolos dos ingredientes
        self.saidas = []      # Lista de mensagens de saída
        self.automato = None  # Autômato atual (AFD ou Autômato de Pilha)
        self.estado_atual = None  # Estado atual do autômato
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Título
        titulo = QLabel("🧪 Simulador de Poções Mágicas")
        titulo.setFont(QFont("Arial", 28, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Botões para escolher o autômato
        automato_layout = QHBoxLayout()
        btn_afd = QPushButton("Autômato Finito Determinístico")
        btn_afd.setStyleSheet("background-color: #4477CE; color: white; font-size: 16px; padding: 10px; border-radius: 10px;")
        btn_afd.clicked.connect(lambda: self.escolher_automato("afd"))
        automato_layout.addWidget(btn_afd)

        btn_pilha = QPushButton("Autômato de Pilha")
        btn_pilha.setStyleSheet("background-color: #725CAD; color: white; font-size: 16px; padding: 10px; border-radius: 10px;")
        btn_pilha.clicked.connect(lambda: self.escolher_automato("pilha"))
        automato_layout.addWidget(btn_pilha)
        layout.addLayout(automato_layout)

        # Grid de ingredientes (inicialmente oculto)
        self.grid = QGridLayout()
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid)
        self.grid_widget.hide()
        layout.addWidget(self.grid_widget)

        # Área de exibição da poção
        self.pocao_frame = QFrame()
        self.pocao_layout = QHBoxLayout(self.pocao_frame)
        layout.addWidget(self.pocao_frame)

        # Imagem inicial da poção
        self.potion_img = QLabel()
        self.potion_img.setAlignment(Qt.AlignCenter)
        if os.path.exists("imagens/potion.png"):
            pix = QPixmap("imagens/potion.png").scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.potion_img.setPixmap(pix)
        self.pocao_layout.addWidget(self.potion_img)

        # Área de saída de mensagens
        self.saida_label = QLabel()
        self.saida_label.setWordWrap(True)
        self.saida_label.setFont(QFont("Arial", 18))
        self.saida_label.setAlignment(Qt.AlignCenter)
        self.saida_label.setStyleSheet("background: #1e2228; border-radius: 8px; padding: 10px; margin-top: 10px;")
        layout.addWidget(self.saida_label)

        # Botão para finalizar
        self.finalizar_btn = QPushButton("Finalizar Poção")
        self.finalizar_btn.setStyleSheet("background-color: #27ae60; color: white; font-size: 16px; padding: 10px; border-radius: 10px;")
        self.finalizar_btn.setFixedWidth(200)
        self.finalizar_btn.clicked.connect(self.finalizar_pocao)
        self.finalizar_btn.hide()
        layout.addWidget(self.finalizar_btn, alignment=Qt.AlignCenter)

        self.atualizar_pocao_visual()
        self.atualizar_saida()

    def escolher_automato(self, tipo):
        # Abre diálogo para selecionar arquivo
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo de entrada",
            "",
            "Arquivos de Texto (*.txt);;Todos os Arquivos (*.*)"
        )
        
        if not arquivo:  # Se o usuário cancelar a seleção
            return
            
        try:
            # Reseta o autômato e a interface
            if tipo == "afd":
                self.automato = AFD(arquivo)
                self.estado_atual = self.automato.estado_inicial
            else:
                self.automato = AutomatoDePilha(arquivo)
                self.estado_atual = self.automato.estado
            
            # Reseta todas as variáveis e interface
            self.saidas = []
            self.poção_atual = []
            self.atualizar_pocao_visual()
            self.atualizar_saida()
            
            # Mostra os elementos da interface
            self.grid_widget.show()
            self.finalizar_btn.show()
            self.criar_botoes_ingredientes()
            
            # Mostra mensagem de sucesso
            QMessageBox.information(
                self,
                "Arquivo Carregado",
                f"Arquivo carregado com sucesso: {os.path.basename(arquivo)}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro ao Carregar Arquivo",
                f"Erro ao carregar o arquivo: {str(e)}"
            )

    def criar_botoes_ingredientes(self):
        # Limpa o grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Adiciona botões de ingredientes
        row, col = 0, 0
        for idx, ing in enumerate(INGREDIENTES):
            btn = QPushButton()
            btn.setFixedSize(150, 180)
            btn.setStyleSheet("background-color: #34495e; border-radius: 10px; text-align: center;")
            if os.path.exists(ing["img"]):
                pix = QPixmap(ing["img"]).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                btn.setIcon(QIcon(pix))
                btn.setIconSize(pix.size())
            btn.setText(f"{ing['nome']}\n({ing['simbolo']})")
            btn.setFont(QFont("Arial", 10))
            btn.clicked.connect(lambda _, s=ing['simbolo']: self.adicionar_ingrediente(s))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def adicionar_ingrediente(self, simbolo):
        if not self.automato:
            return
        self.poção_atual.append(simbolo)
        # Integra a lógica real do autômato
        if isinstance(self.automato, AFD):
            proximo_estado = self.automato.transicoes.get((self.estado_atual, simbolo), self.automato.estado_erro)
            msg = f"Transição: ({self.estado_atual}, '{simbolo}') → {proximo_estado}"
            if proximo_estado == self.automato.estado_erro:
                msg += " ❌ Erro na mistura: ingrediente inválido!"
                QMessageBox.warning(self, "Mistura Instável", "A mistura ficou instável ou em sequência inválida!")
            elif proximo_estado == self.automato.estado_final:
                msg += " ✅ Estado final alcançado!"
            self.estado_atual = proximo_estado
        else:  # Autômato de Pilha
            self.automato.aplicar_entrada(simbolo)
            if self.automato.estado == self.automato.estado_erro:
                msg = "❌ Erro na mistura: ingrediente inválido ou sequência inválida!"
                QMessageBox.warning(self, "Mistura Instável", "A mistura ficou instável ou em sequência inválida!")
            elif self.automato.estado == self.automato.estado_final:
                msg = "✅ Estado final alcançado!"
            else:
                msg = f"Estado atual: {self.automato.estado}, Pilha: {', '.join(self.automato.pilha) if self.automato.pilha else '(vazia)'}"
        self.saidas.append(msg)
        self.atualizar_pocao_visual()
        self.atualizar_saida()

    def atualizar_pocao_visual(self):
        # Limpa o layout
        for i in reversed(range(self.pocao_layout.count())):
            widget = self.pocao_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Se não há ingredientes, mostra a imagem da poção
        if not self.poção_atual:
            if os.path.exists("imagens/potion.png"):
                pix = QPixmap("imagens/potion.png").scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.potion_img.setPixmap(pix)
            self.pocao_layout.addWidget(self.potion_img)
        else:
            # Adiciona imagens dos ingredientes
            for simb in self.poção_atual:
                ing = next((i for i in INGREDIENTES if i['simbolo'] == simb), None)
                if ing and os.path.exists(ing['img']):
                    lbl = QLabel()
                    pix = QPixmap(ing['img']).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    lbl.setPixmap(pix)
                    self.pocao_layout.addWidget(lbl)
                else:
                    lbl = QLabel(simb)
                    lbl.setFont(QFont("Arial", 18))
                    self.pocao_layout.addWidget(lbl)

    def atualizar_saida(self):
        if not self.automato:
            self.saida_label.setText("Escolha a opção de autômato desejada!")
        elif not self.saidas:
            self.saida_label.setText("Clique nos ingredientes para começar a misturar sua poção!")
        else:
            self.saida_label.setText("<br>".join(self.saidas[-5:]))  # Mostra as últimas 5 mensagens

    def finalizar_pocao(self):
        if self.validar_mistura():
            self.poção_atual = []
            self.atualizar_saida()

    def validar_mistura(self):
        if not self.poção_atual:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um ingrediente!")
            return False

        if isinstance(self.automato, AFD):
            # Validações específicas do AFD
            if 'a' in self.poção_atual and 'o' in self.poção_atual:
                QMessageBox.warning(self, "Mistura Inválida", 
                    "❌ Água e óleo não podem estar na mesma receita!\n\n" +
                    "Mistura atual: " + " ".join(self.poção_atual))
                return False

            # Verifica se a sequência é válida
            estado_atual = self.automato.estado_inicial
            for simbolo in self.poção_atual:
                if (estado_atual, simbolo) not in self.automato.transicoes:
                    QMessageBox.warning(self, "Mistura Inválida",
                        f"❌ Sequência inválida após '{simbolo}'!\n\n" +
                        "Mistura atual: " + " ".join(self.poção_atual))
                    return False
                estado_atual = self.automato.transicoes[(estado_atual, simbolo)]

            # Verifica se chegou a um estado final
            if estado_atual != self.automato.estado_final:
                QMessageBox.warning(self, "Mistura Incompleta",
                    "❌ A mistura está incompleta!\n\n" +
                    "Mistura atual: " + " ".join(self.poção_atual))
                return False

            # Verifica número mínimo de ingredientes apenas se a sequência for válida
            if len(self.poção_atual) < 3:
                QMessageBox.warning(self, "Mistura Incompleta",
                    "❌ Cada poção deve ter pelo menos 3 ingredientes!\n\n" +
                    "Mistura atual: " + " ".join(self.poção_atual))
                return False

            # Determina o tipo de poção baseado na mistura
            if self.poção_atual == ['a', 'p', 'p']:
                poção = "Poção de Restauração Comum"
                # Mostra a imagem mix1.png
                if os.path.exists("imagens/mix1.png"):
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Mistura Válida")
                    msg_box.setText(f"✅ Mistura válida!\n\nTipo de Poção: {poção}\nIngredientes: {' '.join(self.poção_atual)}")
                    pixmap = QPixmap("imagens/mix1.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    msg_box.setIconPixmap(pixmap)
                    msg_box.exec_()
                else:
                    QMessageBox.information(self, "Mistura Válida",
                        f"✅ Mistura válida!\n\n" +
                        f"Tipo de Poção: {poção}\n" +
                        f"Ingredientes: {' '.join(self.poção_atual)}")
            elif self.poção_atual == ['a', 'p', 's']:
                poção = "Poção de Cura Avançada"
                # Mostra a imagem mix3.png
                if os.path.exists("imagens/mix3.png"):
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Mistura Válida")
                    msg_box.setText(f"✅ Mistura válida!\n\nTipo de Poção: {poção}\nIngredientes: {' '.join(self.poção_atual)}")
                    pixmap = QPixmap("imagens/mix3.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    msg_box.setIconPixmap(pixmap)
                    msg_box.exec_()
            elif self.poção_atual == ['f', 's', 'c']:
                poção = "Poção de Força"
                # Mostra a imagem mix2.png
                if os.path.exists("imagens/mix2.png"):
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Mistura Válida")
                    msg_box.setText(f"✅ Mistura válida!\n\nTipo de Poção: {poção}\nIngredientes: {' '.join(self.poção_atual)}")
                    pixmap = QPixmap("imagens/mix2.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    msg_box.setIconPixmap(pixmap)
                    msg_box.exec_()
            else:
                poção = "Poção Desconhecida"
                QMessageBox.information(self, "Mistura Válida",
                    f"✅ Mistura válida!\n\n" +
                    f"Tipo de Poção: {poção}\n" +
                    f"Ingredientes: {' '.join(self.poção_atual)}")
            return True

        else:  # autômato de pilha
            # Validações específicas do APD
            estado_atual = self.automato.estado
            pilha = []
            reacoes = []

            # Verifica se a sequência é válida
            for simbolo in self.poção_atual:
                if (estado_atual, simbolo) not in self.automato.transicoes:
                    QMessageBox.warning(self, "Mistura Inválida",
                        f"❌ Sequência inválida após '{simbolo}'!\n\n" +
                        "Mistura atual: " + " ".join(self.poção_atual))
                    return False

                estado_atual = self.automato.transicoes[(estado_atual, simbolo)]

                # Processa os efeitos na pilha
                if simbolo == 'f':
                    pilha.append('🔥 quente')
                    reacoes.append("Temperatura aumentada")
                elif simbolo == 's':
                    pilha.append('🟥 vermelho')
                    reacoes.append("Coloração vermelha adicionada")
                elif simbolo == 'c':
                    if '🔥 quente' in pilha:
                        pilha.remove('🔥 quente')
                        reacoes.append("Temperatura resfriada")
                    else:
                        pilha.append('❄️ frio')
                        reacoes.append("Mistura ficou fria")
                elif simbolo == 'a':
                    if pilha:
                        removido = pilha.pop()
                        reacoes.append(f"'{removido}' neutralizado com água")
                    else:
                        reacoes.append("Nada para neutralizar")
                elif simbolo == 'p':
                    pilha.append('🌸 floral')
                    reacoes.append("Aroma floral adicionado")

            # Verifica se chegou a um estado final
            if estado_atual != self.automato.estado_final:
                QMessageBox.warning(self, "Mistura Incompleta",
                    "❌ A mistura está incompleta!\n\n" +
                    "Mistura atual: " + " ".join(self.poção_atual))
                return False

            # Determina o tipo de poção baseado nas reações
            poção = "Poção Mágica"
            if '🔥 quente' in pilha and '🟥 vermelho' in pilha:
                poção = "Poção de Fogo"
            elif '❄️ frio' in pilha and '🟥 vermelho' in pilha:
                poção = "Poção de Gelo"
            elif '🌸 floral' in pilha and '🟥 vermelho' in pilha:
                poção = "Poção de Cura"
            elif '🌸 floral' in pilha and '❄️ frio' in pilha:
                poção = "Poção de Calmante"

            QMessageBox.information(self, "Mistura Válida",
                f"✅ Mistura válida!\n\n" +
                f"Tipo de Poção: {poção}\n" +
                f"Ingredientes: {' '.join(self.poção_atual)}\n" +
                f"Reações: {', '.join(reacoes)}")
            return True

def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Erro ao abrir a interface: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()