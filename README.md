gente, aqui eu vou colocar explicadinho o que eu fiz:
#entrada.txt:
    -> Ele é a entrada da afd, tem a criação de até 3 ingredientes.
    -> A transição segue o que foi pedido pelodaniel, onde agua e oleo não podem ficar juntas e com tres estados, ing1, ing2 e o final que é com o terceiro ingrediente
    -> O oleo não pode sser inserido a partir do segundo elemento, vai para erro.
    -> Estado de erro absorve qualquer simbolo para manter a especificação.
#entrada_pilha.txt:
    -> As pocoes que eu implementei são:
        Farelo, que empliha quente. Sangue, que empilha vermelho. Carvão que remove quente se estiver na pilha, se não, vai empilhar frio. Agua que remove o topo da pilha. Petalas que vai empilhar floral. OLeo que só é aceito no estado de erro. Final que aceita a mistura.
    -> Se qualquer ordem for quebrada ou algum símbolo for inesperado, a máquina entra no estado erro.
    -> O estado erro aceita qualquer coisa que venha depois (inclusive o) para simular uma poção instável.
#IMplementação dos .py dos automatos:
    -> Eu pensei em implementar os automatos em .py separados para maior facilidade na detecção de erros e para "liga-los", fiz um interface.py que ira ser um main.
    -> AFD e o de pilha forma implementados como classes, com metodos que irão fazer o funcionamento dasmesmas de forma igual ao que o daniel colocou em sala(implementação que eu i pela internet).
 -> Implementei tbm o  ANSI para sair bonitinho no terminal, e coloque emoji, para as saidas. Tem uma animação tbm, que eu achei legal demais, fucei  ate a morte pra achar, mas que ele "treme" oterminal quando dá mistura instavel.
