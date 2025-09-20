import pygame
import json
import sys
import time
import random
import os  

# Inicialização
pygame.init()
pygame.mixer.init()

# Função para localizar arquivos no .exe ou .py
def resource_path(relative_path):
    """Retorna o caminho absoluto de arquivos mesmo no exe"""
    try:
        # PyInstaller cria pasta temporária _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Agora carregue os arquivos usando resource_path
with open(resource_path("src/story.json"), "r", encoding="utf-8") as f:
    story = json.load(f)

# Configurações da janela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Dark Fate")

# Fontes
try:
    font = pygame.font.Font(resource_path("fonts/RobotoMono-Bold.ttf"), 28)  # Fonte de terror
except:
    font = pygame.font.SysFont("arial", 28)
option_font = pygame.font.SysFont("arial", 26)
tip_font = pygame.font.SysFont("arial", 20)

# Cores
WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)
RED = (200, 40, 40)
TEXT_BG = (10, 10, 10, 200)
HOVER_BG = (50, 50, 50, 200)
GLOW_COLOR = (255, 0, 0)

# Texto com margem
TEXT_WIDTH = WIDTH - 200
current_node = "intro_life"

# Música de fundo
try:
    pygame.mixer.music.load(resource_path("sound/trilha_suspense.mp3"))
    pygame.mixer.music.set_volume(0.08)
    pygame.mixer.music.play(-1)
except:
    print("Não foi possível carregar a trilha sonora.")

# Funções
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_text_left(surface, text, y=300, font_to_use=font, max_width=TEXT_WIDTH, bg_color=None, margin_left=100):
    lines = wrap_text(text, font_to_use, max_width)
    total_height = len(lines) * 32
    if bg_color:
        s = pygame.Surface((max_width + 20, total_height + 20), pygame.SRCALPHA)
        s.fill(bg_color)
        surface.blit(s, (margin_left - 10, y - 10))
    for i, line in enumerate(lines):
        # Sombra 3D
        for dx, dy in [(2,2),(1,1),(0,0)]:
            shadow_surf = font_to_use.render(line, True, BLACK)
            surface.blit(shadow_surf, (margin_left+dx, y + i*32 + dy))
        rendered = font_to_use.render(line, True, WHITE)
        surface.blit(rendered, (margin_left, y + i*32))

def draw_particles(surface, num=40):
    for _ in range(num):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(1,3)
        alpha = random.randint(40,100)
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (180,180,180,alpha), (radius,radius), radius)
        surface.blit(s, (x,y))

def play_warning(sound_file):
    try:
        sound = pygame.mixer.Sound(resource_path(sound_file))
        sound.set_volume(0.05)
        sound.play()
    except:
        print("Não foi possível tocar o som:", sound_file)

def draw_options(surface, options, start_y):
    option_rects = []
    spacing = 15
    for i, option in enumerate(options):
        lines = wrap_text(option["text"], option_font, TEXT_WIDTH)
        option_height = len(lines) * 32 + 10
        line_width = max([option_font.size(line)[0] for line in lines])
        bg_width = line_width + 30
        y = start_y + sum([len(wrap_text(o["text"], option_font, TEXT_WIDTH)) * 32 + spacing for o in options[:i]])
        x = (WIDTH - bg_width) // 2
        mx, my = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, bg_width, option_height)
        bg = HOVER_BG if rect.collidepoint(mx, my) else TEXT_BG
        s = pygame.Surface((bg_width, option_height), pygame.SRCALPHA)
        s.fill(bg)
        surface.blit(s, (x, y))
        if rect.collidepoint(mx,my):
            pygame.draw.rect(surface, GLOW_COLOR, rect, 2, border_radius=5)
        for li, line in enumerate(lines):
            shadow = option_font.render(line, True, BLACK)
            surface.blit(shadow, (x+5+1, y+li*32+1))
            text_render = option_font.render(line, True, WHITE)
            surface.blit(text_render, (x+5, y+li*32))
        option_rects.append((rect, option))
    return option_rects

def start_screen():
    alpha = 0
    while True:
        screen.fill(DARK_GRAY)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,alpha))
        screen.blit(overlay,(0,0))
        draw_particles(screen, 20)
        # Nome do jogo 3D
        title = "Dark Fate"
        title_surf = font.render(title, True, WHITE)
        for offset in range(5,0,-1):
            shadow = font.render(title, True, BLACK)
            screen.blit(shadow, (WIDTH//2 - title_surf.get_width()//2 + offset, HEIGHT//3 + offset))
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, HEIGHT//3))
        
        start_rect = pygame.Rect(WIDTH//2-120, HEIGHT//2-10, 240,50)
        exit_rect = pygame.Rect(WIDTH//2-120, HEIGHT//2+60,240,50)
        mx,my = pygame.mouse.get_pos()
        pygame.draw.rect(screen, RED if start_rect.collidepoint(mx,my) else (70,70,70), start_rect, border_radius=5)
        pygame.draw.rect(screen, RED if exit_rect.collidepoint(mx,my) else (70,70,70), exit_rect, border_radius=5)
        start_text = option_font.render("Começar", True, WHITE)
        exit_text = option_font.render("Sair", True, WHITE)
        screen.blit(start_text,(WIDTH//2 - start_text.get_width()//2, HEIGHT//2+5))
        screen.blit(exit_text,(WIDTH//2 - exit_text.get_width()//2, HEIGHT//2+65))
        
        pygame.display.flip()
        alpha = min(120, alpha + 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mx,my):
                    return
                elif exit_rect.collidepoint(mx,my):
                    pygame.quit()
                    sys.exit()

# Rodar menu
start_screen()

# Loop principal
running = True
while running:
    screen.fill(DARK_GRAY)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,150))
    screen.blit(overlay,(0,0))
    draw_particles(screen, 30)
    
    node = story[current_node]
    
    # História à esquerda
    draw_text_left(screen, node["text"], y=250, font_to_use=font, max_width=TEXT_WIDTH, bg_color=TEXT_BG, margin_left=100)
    
    tip_surf = tip_font.render("Use o mouse para escolher", True, WHITE)
    tip_bg = pygame.Surface((tip_surf.get_width()+20, tip_surf.get_height()+10), pygame.SRCALPHA)
    tip_bg.fill((40,40,40,180))
    screen.blit(tip_bg, (50, HEIGHT-70))
    screen.blit(tip_surf, (60, HEIGHT-60))
    
    option_rects = draw_options(screen, node.get("options", []), start_y=HEIGHT//2+100)
    
    exit_rect = pygame.Rect(WIDTH-150, HEIGHT-70, 130,50)
    mx,my = pygame.mouse.get_pos()
    pygame.draw.rect(screen, RED if exit_rect.collidepoint(mx,my) else (100,0,0), exit_rect, border_radius=5)
    exit_text = option_font.render("Sair", True, WHITE)
    screen.blit(exit_text, (WIDTH-110, HEIGHT-60))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            for rect, option in option_rects:
                if rect.collidepoint(mx,my):
                    if "warning" in option:
                        screen.fill(DARK_GRAY)
                        draw_text_left(screen, option["warning"], y=250, font_to_use=font, max_width=TEXT_WIDTH, bg_color=TEXT_BG, margin_left=100)
                        pygame.display.flip()
                        if "sound" in option:
                            play_warning(option["sound"])
                        time.sleep(3)
                    current_node = option["next"]
            if exit_rect.collidepoint(mx,my):
                pygame.quit()
                sys.exit()
