gente, aqui eu vou colocar explicadinho o que eu fiz:
# entrada.txt:
    -> Ele é a entrada da afd, tem a criação de até 3 ingredientes.
    -> A transição segue o que foi pedido pelodaniel, onde agua e oleo não podem ficar juntas e com tres estados, ing1, ing2 e o final que é com o terceiro ingrediente
    -> O oleo não pode sser inserido a partir do segundo elemento, vai para erro.
    -> Estado de erro absorve qualquer simbolo para manter a especificação.
# entrada_pilha.txt:
    -> As pocoes que eu implementei são:
        Farelo, que empliha quente. Sangue, que empilha vermelho. Carvão que remove quente se estiver na pilha, se não, vai empilhar frio. Agua que remove o topo da pilha. Petalas que vai empilhar floral. OLeo que só é aceito no estado de erro. Final que aceita a mistura.
    -> Se qualquer ordem for quebrada ou algum símbolo for inesperado, a máquina entra no estado erro.
    -> O estado erro aceita qualquer coisa que venha depois (inclusive o) para simular uma poção instável.
# IMplementação dos .py dos automatos:
    -> Eu pensei em implementar os automatos em .py separados para maior facilidade na detecção de erros e para "liga-los", fiz um interface.py que ira ser um main.
    -> AFD e o de pilha forma implementados como classes, com metodos que irão fazer o funcionamento dasmesmas de forma igual ao que o daniel colocou em sala(implementação que eu i pela internet).
    -> Implementei tbm o  ANSI para sair bonitinho no terminal, e coloque emoji, para as saidas. Tem uma animação tbm, que eu achei legal demais, fucei  ate a morte pra achar, mas que ele "treme" oterminal quando dá mistura instavel.

# ana:
-explicacao do que eu fiz:
    - Eu fiz a implementacao da interface, utilizei o PyQt5, dps deem uma olhada
    - possivelmente voces vao precisar fazer a instalacao do PyQt5 e PyInstaller
    - na pasta imagens eu adicionei imagens .png q eu mesma desenhei em pixel arte, esta inclusive faltando imagens de alguns ingredientes como:  oil.png, coal.png e bran.png, ent quem for mexer a seguir e tive vontade de desenhar, acho que ficaria bem legal, no grupo do wpp vou mandar o .piskell q é uma ferramenta muito legal GRATUITA E ONLINE  (e boa, oq eh quase impossivel hj em dia), entao use e abusem, voces conseguem salvar esse .piskel e abrir eles clicando em um icone de import, vcs tbm conseguem exportar imagens, eu estava exportando na escala 768x768 (mas a pixel art em si é de 32x32), por favor sigam o mesmo padrao
    - fiz o carregamento do arquivo pega interface, ent vcs precisam selecionar a opcao correta de automato
    - eu estou utilizando um pouco da logica do codigo da rafa, no entanto nem tudo está funcionando 100% na interface, alguns problemas q identifiquei:
    - meu codigo ta lendo de um arquivo .txt fixo, mas seria mais interessante adicionar a posibilidade de colocar o nome do arquivo
    - algumas misturas vaidas estao aparecendo um alerta de sequencia invalida (masss acho q isso nao é um erro, e pode ser por conta do arquivo de entrada)
    - as mensagens ao finalizar pocoes precisam ser revisadas pra ver se está certinho, principalmente se for adicionar mais uma combinacao de poção e tals

    - precisa adicionar imagens para as pocoes produzidas, eu ja fiz o mix1, q é pra pocao de restauracao, mas precisa adicionar na interface

- pra compilar precisa rodar o interface.py, e é importante >nao< chamar a funcao rodar nos outros arquivos afd.py e aut_pilha.py  ao mesmo tempo
- tbm adicionei um caso de teste extra q aceita so a pocao de forca q é "f s c"
- qualquer duvida podem me mandar msg


