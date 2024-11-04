import pygame
import json
import os

pygame.init()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego del Dinosaurio que Salta")

WHITE = (255, 255, 200)
GROUND_COLOR = (150, 150, 150)

game_speed = 10

dino_img = pygame.image.load("dinosaurio.png")
dino_img = pygame.transform.scale(dino_img, (50, 60))
cactus_img = pygame.image.load("cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (40, 40))

dino_width = dino_img.get_width()
dino_height = dino_img.get_height()
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 50
dino_y_velocity = 0
is_jumping = False

cactus_width = cactus_img.get_width()
cactus_height = cactus_img.get_height()
cactus_x = SCREEN_WIDTH
cactus_y = SCREEN_HEIGHT - cactus_height - 50

score = 0
high_scores_file = "scores.json"  # Archivo donde se guardarán los puntajes

clock = pygame.time.Clock()

def draw_dino(x, y):
    screen.blit(dino_img, (x, y))

def draw_cactus(x, y):
    screen.blit(cactus_img, (x, y))

def display_message(text, size, color, y_offset=0):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def save_high_scores(scores):
    """ Guarda los puntajes en un archivo JSON """
    with open(high_scores_file, 'w') as file:
        json.dump(scores, file)

def load_high_scores():
    """ Carga los puntajes desde un archivo JSON """
    if os.path.exists(high_scores_file):
        with open(high_scores_file, 'r') as file:
            return json.load(file)
    return []  # Si no existe el archivo, devuelve una lista vacía

def display_high_scores(scores):
    """ Muestra los 3 mejores puntajes """
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 50)
    title = font.render("Top 3 Mejores Puntajes", True, (0, 0, 0))
    screen.blit(title, [SCREEN_WIDTH // 2 - 150, 100])
    
    for i, score in enumerate(scores[:3]):
        text = font.render(f"{i + 1}: {score['name']} - {score['score']}", True, (0, 0, 0))
        screen.blit(text, [SCREEN_WIDTH // 2 - 150, 150 + i * 50])

    pygame.display.flip()
    pygame.time.wait(3000)  # Pausa para que se pueda ver la ventana por 3 segundos

def update_high_scores(current_score, name, scores):
    """ Actualiza los puntajes con el nombre del jugador """
    scores.append({'name': name, 'score': current_score})
    scores.sort(key=lambda x: x['score'], reverse=True)
    if len(scores) > 3:  # Solo guarda los 3 mejores
        scores = scores[:3]
    save_high_scores(scores)

def get_player_name():
    """ Permite al jugador ingresar su nombre """
    font = pygame.font.SysFont(None, 50)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        screen.fill(WHITE)
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(name, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        pygame.display.flip()
        clock.tick(30)

def game_loop():
    global dino_y, dino_y_velocity, is_jumping, cactus_x, game_speed, score
    
    high_scores = load_high_scores()  # Cargar los puntajes anteriores
    
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Actualizar los mejores puntajes, solicitar nombre y mostrar la ventana
                        player_name = get_player_name()
                        if player_name:
                            update_high_scores(score, player_name, high_scores)
                        display_high_scores(high_scores)
                        
                        # Reiniciar el juego
                        game_over = False
                        cactus_x = SCREEN_WIDTH
                        dino_y = SCREEN_HEIGHT - dino_height - 50
                        game_speed = 10
                        score = 0
                    elif not is_jumping:
                        dino_y_velocity = -15
                        is_jumping = True
        
        if not game_over:
            dino_y += dino_y_velocity
            dino_y_velocity += 1.2  # Gravedad

            if dino_y >= SCREEN_HEIGHT - dino_height - 50:
                dino_y = SCREEN_HEIGHT - dino_height - 50
                is_jumping = False
                dino_y_velocity = 0

            cactus_x -= game_speed
            if cactus_x < -cactus_width:
                cactus_x = SCREEN_WIDTH
                score += 1  
                game_speed += 0.5  

            if dino_x + dino_width > cactus_x and dino_x < cactus_x + cactus_width:
                if dino_y + dino_height > cactus_y:
                    game_over = True  

        screen.fill(WHITE)
        pygame.draw.rect(screen, GROUND_COLOR, [0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50])

        draw_dino(dino_x, dino_y)
        draw_cactus(cactus_x, cactus_y)

        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Puntuación: {score}", True, (0, 0, 0))
        screen.blit(text, [10, 10])

        if game_over:
            display_message("¡Sos un asno, dedícate a otra cosa!", 50, (0, 0, 0))
            display_message("Presiona SPACE para reiniciar", 30, (0, 0, 0), 50)

        pygame.display.flip()

        if score > 10:
            game_speed += 0.1

        if score > 14:
            dino_y_velocity += 1.3

        clock.tick(45)

    pygame.quit()

game_loop()
