import pygame
import random


pygame.init()


print("""\
                                                                                                                         

 ______     __  __     ______     ______     ______     __    __     __     __   __     ______     ______    
/\  == \   /\ \/\ \   /\  ___\   /\  ___\   /\  __ \   /\ "-./  \   /\ \   /\ "-.\ \   /\  __ \   /\  ___\   
\ \  __<   \ \ \_\ \  \ \___  \  \ \ \____  \ \  __ \  \ \ \-./\ \  \ \ \  \ \ \-.  \  \ \  __ \  \ \___  \  
 \ \_____\  \ \_____\  \/\_____\  \ \_____\  \ \_\ \_\  \ \_\ \ \_\  \ \_\  \ \_\\"\_\  \ \_\ \_\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/  \/_/   \/_/   \/_/ \/_/   \/_/\/_/   \/_____/ 
                                                                                                             

                                                                                                                         
""")
print("Bienvenido, porfavor escriba el tamaño de la cuadricula")
print("NIVEL FACIL (1-10)")
print("NIVEL INTERMEDIO (11-20)")
print("NIVEL DIFICIL (21-30)")


color_fondo = (100, 150, 237)
tamano_ancho = int(input()) 
tamano_alto = tamano_ancho
numero_minas = int(tamano_ancho * 1.5)
tamano_cuadrito = 30 
bordes = 15  
borde_superior = 100 
ancho_pantalla = tamano_cuadrito * tamano_ancho + bordes * 2  
alto_pantalla = tamano_cuadrito * tamano_alto + bordes + borde_superior 
creacion_pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))  # creacion de la pantalla del juego
contador_tiempo = pygame.time.Clock()  # creacion contadr tiempo
pygame.display.set_caption("Buscaminas")  # nombre en la pantalla del juego

# IMPORTAR IMAGENES
img_vacio = pygame.image.load("Sprites/empty.png")
img_bandera = pygame.image.load("Sprites/flag.png")
img_cuadro = pygame.image.load("Sprites/Grid.png")
img_cuadro1 = pygame.image.load("Sprites/grid1.png")
img_cuadro2 = pygame.image.load("Sprites/grid2.png")
img_cuadro3 = pygame.image.load("Sprites/grid3.png")
img_cuadro4 = pygame.image.load("Sprites/grid4.png")
img_cuadro5 = pygame.image.load("Sprites/grid5.png")
img_cuadro6 = pygame.image.load("Sprites/grid6.png")
img_cuadro7 = pygame.image.load("Sprites/grid7.png")
img_cuadro8 = pygame.image.load("Sprites/grid8.png")
img_mina = pygame.image.load("Sprites/mine.png")
img_mina_activada = pygame.image.load("Sprites/mineClicked.png")
img_mina_falsa = pygame.image.load("Sprites/mineFalse.png")

#creacion matriz juego
cuadricula = []  # cuadrado principal
minas = []  # posicion de minas


# funcion para escribir textos
def escribir_textos(txt, tamaño, yOff=0):
    texto_pantalla = pygame.font.SysFont("Calibri", tamaño, True).render(txt, True, (0, 0, 0)) #sysfont(nombre,tamaño,negrita=bool)
    rectangulo = texto_pantalla.get_rect()
    rectangulo.center = (tamano_ancho * tamano_cuadrito / 2 + bordes, tamano_alto * tamano_cuadrito / 2 + borde_superior + yOff)
    creacion_pantalla.blit(texto_pantalla, rectangulo)



# Create class cuadricula
class Cuadricula:
    def __init__(self, xcuadricula, ycuadricula, type):
        self.xcuadricula = xcuadricula  # posicion x de la cuadricula
        self.ycuadricula = ycuadricula  # posicion y de la cuadricula
        self.clicked = False  # comprobar si  la casilla ha sido clikeada
        self.mina_presionada = False  # comprobar si  la casilla ha sido clikeada y es una mina
        self.mina_falsa = False  # comprobar si la casilla tiene la bandera en posicion errada
        self.bandera = False  # comprobar la posicion de la bandera

        # Create rectanguloObject to handle drawing and collisions
        self.rectangulo = pygame.Rect(bordes + self.xcuadricula * tamano_cuadrito, borde_superior + self.ycuadricula * tamano_cuadrito, tamano_cuadrito, tamano_cuadrito)
        self.valor = type  # valorue of the cuadricula, -1 is mine

    def dibujar_cuadricula(self):
        # dibujar la cuadricula respecto a las variables
        if self.mina_falsa:
            creacion_pantalla.blit(img_mina_falsa, self.rectangulo)
        else:
            if self.clicked:
                if self.valor == -1:
                    if self.mina_presionada:
                        creacion_pantalla.blit(img_mina_activada, self.rectangulo)
                    else:
                        creacion_pantalla.blit(img_mina, self.rectangulo)
                else:
                    if self.valor == 0:
                        creacion_pantalla.blit(img_vacio, self.rectangulo)
                    elif self.valor == 1:
                        creacion_pantalla.blit(img_cuadro1, self.rectangulo)
                    elif self.valor == 2:
                        creacion_pantalla.blit(img_cuadro2, self.rectangulo)
                    elif self.valor == 3:
                        creacion_pantalla.blit(img_cuadro3, self.rectangulo)
                    elif self.valor == 4:
                        creacion_pantalla.blit(img_cuadro4, self.rectangulo)
                    elif self.valor == 5:
                        creacion_pantalla.blit(img_cuadro5, self.rectangulo)
                    elif self.valor == 6:
                        creacion_pantalla.blit(img_cuadro6, self.rectangulo)
                    elif self.valor == 7:
                        creacion_pantalla.blit(img_cuadro7, self.rectangulo)
                    elif self.valor == 8:
                        creacion_pantalla.blit(img_cuadro8, self.rectangulo)

            else:
                if self.bandera:
                    creacion_pantalla.blit(img_bandera, self.rectangulo)
                else:
                    creacion_pantalla.blit(img_cuadro, self.rectangulo)

    def revelar_cuadricula(self):
        self.clicked = True
        # auto revelar cuando sea un cero
        if self.valor == 0:
            for x in range(-1, 2):
                if self.xcuadricula + x >= 0 and self.xcuadricula + x < tamano_ancho:
                    for y in range(-1, 2):
                        if self.ycuadricula + y >= 0 and self.ycuadricula + y < tamano_alto:
                            if not cuadricula[self.ycuadricula + y][self.xcuadricula + x].clicked:
                                cuadricula[self.ycuadricula + y][self.xcuadricula + x].revelar_cuadricula()
        elif self.valor == -1:
            # revelar todas la minas cuando es una mina
            for m in minas:
                if not cuadricula[m[1]][m[0]].clicked:
                    cuadricula[m[1]][m[0]].revelar_cuadricula()

    def actualizar_valor(self):
        # actualizar el valor cuando la cuadricula es generada
        if self.valor != -1:
            for x in range(-1, 2):
                if self.xcuadricula + x >= 0 and self.xcuadricula + x < tamano_ancho:
                    for y in range(-1, 2):
                        if self.ycuadricula + y >= 0 and self.ycuadricula + y < tamano_alto:
                            if cuadricula[self.ycuadricula + y][self.xcuadricula + x].valor == -1:
                                self.valor += 1


def repeticion_juego():
    estado_juego = "Jugando"  
    minas_sobrantes = numero_minas  
    global cuadricula  
    cuadricula = []
    global minas
    t = 0  # inicio tiempo

    # generar minas
    minas = [[random.randrange(0, tamano_ancho),
              random.randrange(0, tamano_alto)]]

    for c in range(numero_minas - 1):
        pos = [random.randrange(0, tamano_ancho),
               random.randrange(0, tamano_alto)]
        igual = True
        while igual:
            for i in range(len(minas)):
                if pos == minas[i]:
                    pos = [random.randrange(0, tamano_ancho), random.randrange(0, tamano_alto)]
                    break
                if i == len(minas) - 1:
                    igual = False
        minas.append(pos)

    # generar toda la  cuadricula
    for j in range(tamano_alto):
        linea= []
        for i in range(tamano_ancho):
            if [i, j] in minas:
                linea.append(Cuadricula(i, j, -1))
            else:
                linea.append(Cuadricula(i, j,0))
        cuadricula.append(linea)


    # actualizacion de la cuadricula
    for i in cuadricula:
        for j in i:
            j.actualizar_valor()

    # loop principal
    while estado_juego != "Exit":
        # reiniciar pantalla
        creacion_pantalla.fill(color_fondo)

        # entradas de usuario
        for evento in pygame.event.get():
            # verificar si el jugardor cierra la ventana
            if evento.type == pygame.QUIT:
                estado_juego = "Exit"
            # verificar si el juego se reinicia
            if estado_juego == "Game Over" or estado_juego == "Win":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        estado_juego = "Exit"
                        repeticion_juego()
            else:
                if evento.type == pygame.MOUSEBUTTONUP:
                    for i in cuadricula:
                        for j in i:
                            if j.rectangulo.collidepoint(evento.pos):
                                if evento.button == 1:
                                    # si el jugador oprime click izquierdo en la cuadricula
                                    j.revelar_cuadricula()
                                    # quitar bandera
                                    if j.bandera:
                                        minas_sobrantes += 1
                                        j.bandera = False
                                    # si es una mina
                                    if j.valor == -1:
                                        estado_juego = "Game Over"
                                        j.mina_presionada = True
                                elif evento.button == 3:
                                    # jugador presiona click derecho
                                    if not j.clicked:
                                        if j.bandera:
                                            j.bandera = False
                                            minas_sobrantes += 1
                                        else:
                                            if minas_sobrantes == 0 :
                                                minas_sobrantes = 0 
                                            else :
                                                j.bandera = True
                                                minas_sobrantes -= 1
                                            

        # verificar si gano
        w = True
        for i in cuadricula:
            for j in i:
                j.dibujar_cuadricula()
                if j.valor != -1 and not j.clicked:
                    w = False
        if w and estado_juego != "Exit":
            estado_juego = "Win"

        # dibujar texto
        if estado_juego != "Game Over" and estado_juego != "Win":
            t += 1
        elif estado_juego == "Game Over":
            escribir_textos("Game Over!", 40)
            escribir_textos("R PARA REINICIAR", 35, 50)
            for i in cuadricula:
                for j in i:
                    if j.bandera and j.valor != -1:
                        j.mina_falsa = True
        else:
            escribir_textos("GANASTE!", 40)
            escribir_textos("R PARA REINICIAR", 35, 50)
        # DIBUJAR TIEMPO
        s = str(t // 15)
        texto_pantalla = pygame.font.SysFont("Calibri", 50).render(s, True, (255, 255, 255))
        creacion_pantalla.blit(texto_pantalla, (bordes, bordes))
        # DIBUJAR MINAS SOBRANTES
        texto_pantalla = pygame.font.SysFont("Calibri", 50).render(minas_sobrantes.__str__(), True, (0, 0, 0))
        creacion_pantalla.blit(texto_pantalla, (ancho_pantalla - bordes - 50, bordes))

        pygame.display.update()  # ACTUALIZAR PANTALLA

        contador_tiempo.tick(15)  # VELOCIDAD DEL CONTADOR

if __name__ == "__main__":   
    repeticion_juego()
    pygame.quit()
    quit()
