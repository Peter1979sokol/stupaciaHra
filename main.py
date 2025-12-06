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


def show_sequence():
    """Zobrazí celé poradie rozsvetlením kvadrantov"""
    for item in sequence:
        # Rozsvieti kvadrant/kvadranty
        draw_quadrants(active=item)
        pygame.time.wait(1000)  # Počkaj 1 sekundu

        # Zhasni (vráť na čiernu)
        draw_quadrants()
        pygame.time.wait(300)  # Krátka pauza medzi kvadrantmi


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
                    show_sequence()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not started:
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

            pygame.display.flip()
        else:
            # Po skončení sekvencie
            draw_quadrants()
            text = font.render("Sekvencia dokončená!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            background_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, WHITE, background_rect, 2)
            screen.blit(text, text_rect)

            restart_text = small_font.render("MEDZERNÍK - znova | ESC - ukončiť", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            restart_bg = restart_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, restart_bg)
            pygame.draw.rect(screen, WHITE, restart_bg, 2)
            screen.blit(restart_text, restart_rect)

            pygame.display.flip()

            # Umožní reštart
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                started = False
                pygame.time.wait(200)  # Krátka pauza aby sa neprekrývali

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()