import pygame
import sys
import time

# Inicializácia pygame
pygame.init()

# Rozmery okna - fullscreen
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Farby - tmavé a svetlé verzie
COLORS = {
    'zlta': {'dark': (180, 180, 0), 'light': (255, 255, 0)},
    'modra': {'dark': (0, 0, 180), 'light': (0, 150, 255)},
    'zelena': {'dark': (0, 180, 0), 'light': (0, 255, 0)},
    'cervena': {'dark': (180, 0, 0), 'light': (255, 0, 0)}
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Vytvorenie okna (fullscreen)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Farebné kvadranty")

# Pozície kvadrantov: hore ľavo, hore vpravo, dole ľavo, dole vpravo
quadrants = {
    'zlta': (0, 0, WIDTH // 2, HEIGHT // 2),  # hore ľavo
    'modra': (WIDTH // 2, 0, WIDTH // 2, HEIGHT // 2),  # hore vpravo
    'zelena': (0, HEIGHT // 2, WIDTH // 2, HEIGHT // 2),  # dole ľavo
    'cervena': (WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)  # dole vpravo
}

# Definuj poradie rozsvetlenia (naprogramovateľné) - minimálne 30 položiek
# Môže obsahovať aj viacero farieb naraz ako zoznam
sequence = ['zlta', 'modra', 'zelena', 'cervena',
            ['zlta', 'modra'], 'cervena', 'modra', 'zelena',
            'cervena', 'zlta', ['zelena', 'cervena'], 'modra',
            'modra', 'zelena', 'cervena', ['zlta', 'cervena'],
            'zelena', 'cervena', 'zlta', 'modra',
            ['cervena', 'modra'], 'modra', 'zlta', 'zelena',
            'zlta', ['modra', 'zelena'], 'cervena', 'zelena',
            'modra', 'zlta', ['zlta', 'cervena', 'modra'], 'cervena']


def draw_quadrants(active=None):
    """Vykreslí všetky kvadranty, active môže byť jeden kvadrant alebo zoznam"""
    # Ak active je string, preveď ho na zoznam
    if isinstance(active, str):
        active = [active]
    elif active is None:
        active = []

    for color_name, rect in quadrants.items():
        if color_name in active:
            color = COLORS[color_name]['light']
        else:
            color = BLACK  # Vypnuté kvadranty sú čierne

        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()


def check_quit():
    """Skontroluje či užívateľ stlačil ESC"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def show_sequence():
    """Zobrazí celé poradie rozsvetlením kvadrantov v nekonečnej slučke"""
    while True:
        for item in sequence:
            # Skontroluj ESC pred rozsvietením
            if check_quit():
                return True

            # Rozsvieti kvadrant/kvadranty
            draw_quadrants(active=item)

            # Počkaj 1 sekundu, ale kontroluj ESC každých 50ms
            for _ in range(20):  # 20 x 50ms = 1000ms
                if check_quit():
                    return True
                pygame.time.wait(50)

            # Skontroluj ESC pred zhasnutím
            if check_quit():
                return True

            # Zhasni (vráť na čiernu)
            draw_quadrants()

            # Krátka pauza medzi kvadrantmi, tiež kontroluj ESC
            for _ in range(6):  # 6 x 50ms = 300ms
                if check_quit():
                    return True
                pygame.time.wait(50)


def main():
    clock = pygame.time.Clock()
    running = True
    started = False

    # Úvodná obrazovka
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    # Spustí sekvenciu v nekonečnej slučke
                    quit_requested = show_sequence()
                    if quit_requested:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not started and running:
            # Vykreslí základné kvadranty
            draw_quadrants()

            # Vykreslí inštrukcie
            text = font.render("Stlač MEDZERNÍK pre štart", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            # Pridaj čierny obdĺžnik ako pozadie pre text
            background_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, WHITE, background_rect, 2)

            screen.blit(text, text_rect)

            # Zobraz sekvenciu ako text
            seq_display = []
            for item in sequence:
                if isinstance(item, list):
                    seq_display.append('+'.join(item))
                else:
                    seq_display.append(item)

            seq_text = small_font.render(f"Sekvencia: {' -> '.join(seq_display[:10])}...", True, WHITE)
            seq_rect = seq_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            seq_bg = seq_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, seq_bg)
            pygame.draw.rect(screen, WHITE, seq_bg, 2)
            screen.blit(seq_text, seq_rect)

            # Pridaj info o nekonečnej slučke
            loop_text = small_font.render("(Sekvencia sa opakuje donekonečna - ESC ukončí)", True, WHITE)
            loop_rect = loop_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            loop_bg = loop_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, loop_bg)
            pygame.draw.rect(screen, WHITE, loop_bg, 2)
            screen.blit(loop_text, loop_rect)

            pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()