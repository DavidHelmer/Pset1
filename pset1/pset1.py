# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: David Helmer Cândido
#    Matrícula: 202200999
#    Turma: CC3M
#    Email: david.hcandido1@gmail.com
#    Repositório Github: https://github.com/DavidHelmer/Pset1
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.
#


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage

# Função que recebe um parâmetro n que sera o tamanho do kernel
# A função cria um kernel utilizando da formula para obter uma matriz
# com o numero de pixels que tera o kernel, distribuindo os pesos igualmente

def criarKernel(n):
    kernel = [[1/n**2 for index in range(n)]for index in range(n)]
    return kernel


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):

        #Condições para que, se x < 0 ou y < 0, os pixels
        #fora do limite terão o valor do pixel adjacente
        if x < 0:
            x = 0
        elif x >= self.largura:
            x = self.largura - 1

        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1

        return self.pixels[(y * self.largura + x)]

    def set_pixel(self, x, y, c):
        self.pixels[(x + y * self.largura)] = c

    #Função responsavel por aplicar a cor nova da imagem invertida em todos os pixels
    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    #Função responsável por inverter a cor da imagem, utilizando da outra função
    #de aplicar a cor nos pixels, e aplicando a formula da inversão
    # 255 - c (onde c é o valor original do pixel)

    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255-c)

    #Função responsável de aplicar correlacao, utilizando dos kernels,
    #utilizando dois for a mais, com o proposito similar aos outros para
    #para formar a largura e altura da matriz kernel, e ao final fazendo a
    #formula da correlacao

    def correlacao(self, n):
        tamanhoKernel = len(n)
        imagem = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                somaCorrelacao = 0
                for z in range(tamanhoKernel):
                    for w in range(tamanhoKernel):
                        somaCorrelacao += self.get_pixel((x-(tamanhoKernel//2) + z), (y-(tamanhoKernel//2))+w)*n[z][w]

                imagem.set_pixel(x, y, somaCorrelacao)
        return imagem

    #Função responsável por aplicar o filtro que deixa a imagem borraada, utilizando da funcao criarKernel
    #e utilizando da função normalizarPixel para que o pixel mais escuro tenha valor 0 e o mais claro 255

    def borrada(self, n):
        kernel = self.correlacao(criarKernel(n))
        kernel.normalizarPixel()
        return kernel

    #Função responsável por permitir uma normalizaçao dos pixels, fazendo assim um dimensionamento linear dos
    #pixels, fazendo assim que o pixel mais escuro da imagem na saída tenha valor 0 e o mais claro tenha valor 255
    #utiliza apenas condicionais para tornar isso possivel

    def normalizarPixel(self):
        for x in range(self.largura):
            for y in range(self.altura):
                pixelObservado = self.get_pixel(x,y)

                if pixelObservado < 0:
                    pixelObservado = 0

                elif pixelObservado > 255:
                    pixelObservado = 255

                pixelObservado = round(pixelObservado)
                #Pixels devem ser inteiros, portanto devem
                #ser arredondados utilizando a função round

                self.set_pixel(x,y, pixelObservado)


    #Função responsável por deixar a imagem focada, utilizando da formula que basicamente
    #dobra o tamanho da imagem original e depois subtrai a versão da imagem original borrada
    #e tambem conta com a função normalizarPixel

    def focada(self, n):
        imagemBorrada = self.borrada(n)
        imagem = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                formulaImagemFocada = round(2*self.get_pixel(x,y)-(imagemBorrada.get_pixel(x, y)))
                imagem.set_pixel(x, y, formulaImagemFocada)
        imagem.normalizarPixel()
        return imagem

    #Função responsável por detectar as bordas da imagem, utilizando de um operador Sorbel
    #que é basicamente a combinação de dois kernels de imagem e possui sua formula, a função
    #tambem é implementada junto com a normalizarPixel~

    def bordas(self):
        imagem = Imagem.nova(self.largura, self.altura)
        pixelSobelX = [[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]]

        pixelSobelY = [[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]]

        aplicarSobelX = self.correlacao(pixelSobelX)
        aplicarSobelY = self.correlacao(pixelSobelY)

        for x in range(self.largura):
            for y in range(self.altura):
                operacaoSobel = round(math.sqrt(aplicarSobelX.get_pixel(x,y)**2 + aplicarSobelY.get_pixel(x,y)**2))
                imagem.set_pixel(x, y, operacaoSobel)
        imagem.normalizarPixel()

        return imagem

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.largura, event.altura), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.altura, width=event.largura)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.altura, width=e.largura))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':

    #Questão 1:
    #Vamos começar com uma imagem4×1 que é definida com os seguintes parâmetros:
    #altura: 1
    #largura: 4
    #pixels: [29, 89, 136, 200]
    # se você passar essa imagem pelo filtro de inversão, qual seria o
    #output esperado? Justifique sua resposta.
    #R: Considerando que os pixels têm uma escala de cores de 0 a 255, onde 0 representa
    #o preto e 255 o branco, podemos determinar que a cor invertida do branco (valor 0)
    #é o preto (valor 255), e vice-versa. Em outras palavras, o inverso do preto pode ser
    #obtido subtraindo-se o valor do preto do valor máximo possível de um pixel.
    # 255 (maior valor) - 0 (preto(menor valor possivel)) = branco
    #logo os valores dos pixel são [226, 166, 119, 155]

    #Questão 2
    peixe = Imagem.carregar('test_images/bluegill.png')
    peixeInvertido = peixe.invertida()
    Imagem.salvar(peixeInvertido, 'imagens_resposta/peixe.png')

    #Questão 3
    #Para obter a imagem resultante da correlação, podemos calcular a soma dos produtos entre
    #os pixels correspondentes do kernel e da imagem. Por exemplo, multiplicamos o kernel K[0,0]
    #pelo pixel I[0,0], e assim por diante. Ao final, obteremos:
    #1°: (80 * 0,00) + (53 * (-0,07)) + (99 * 0) + (129 * (-0,45)) + (127 * 1,2) + (148 * (-0,25)) + (175 * 0) + (174 * (-0,12)) + (193 * 0)
    #2°: =  0 + (-3.71) + (0) + (-58.05) + (152.4) + (-37) + 0 + (-20.88) + 0
    #3°: = 32.76

    #Questão 4
    kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    porcoPassaro = Imagem.carregar('test_images/pigbird.png')
    correlacaoPorcoPassaro = porcoPassaro.correlacao(kernel)
    Imagem.salvar(correlacaoPorcoPassaro, 'imagens_resposta/porco_e_passaro.png')

    #Imagem cat borrada

    gato = Imagem.carregar('test_images/cat.png')
    gatoBorrado = gato.borrada(5)
    Imagem.salvar(gatoBorrado, 'imagens_resposta/gato.png')


    #Questão 5
    #Sim, é viável realizar a operação de nitidez utilizando apenas uma correlação.
    #A fórmula para aplicar a nitidez é definida como:
    #S x,y = round( 2 * Ix,y - Bx,y )
    #Onde S x,y é o pixel resultante, Ix,y é o pixel da imagem original e Bx,y é o pixel
    #da imagem borrada. Sabemos que o kernel de identidade retorna a mesma imagem na saída.
    #Portanto, como temos o dobro da imagem original na fórmula acima, temos:

    piton = Imagem.carregar('test_images/python.png')
    pitonFocada = piton.focada(11)
    Imagem.salvar(pitonFocada, 'imagens_resposta/piton.png')

    #Questão 6
    #Cada um dos kernels mencionados desempenha o papel de realçar as bordas na imagem, sendo um
    #deles responsável por realçar as bordas no eixo x e o outro no eixo y.

    pixelSobelX = [[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]]

    pixelSobelY = [[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]]

    construcao = Imagem.carregar('test_images/construct.png')
    construcaoSobelX = construcao.correlacao(pixelSobelX)
    Imagem.salvar(construcaoSobelX, 'imagens_resposta/construcao_sobel_x.png')

    contrucaoSobelY = construcao.correlacao(pixelSobelY)
    Imagem.salvar(contrucaoSobelY, 'imagens_resposta/construcao_sobel_y.png')

    construcaoBorda = construcao.bordas()
    Imagem.salvar(construcaoBorda, 'imagens_resposta/construcao.png')

    pass

    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
