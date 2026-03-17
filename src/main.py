import json
import math
import random
from pathlib import Path
import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

SAVE_DIR = Path.home() / ".cyber_shield"
SAVE_FILE = SAVE_DIR / "save.json"

BG = (8, 12, 24)
PANEL = (16, 22, 40)
CYAN = (78, 231, 255)
SOFT = (130, 180, 255)
MAGENTA = (255, 91, 194)
GREEN = (120, 255, 160)
RED = (255, 90, 110)
YELLOW = (255, 220, 110)
WHITE = (240, 248, 255)
GRID = (25, 40, 68)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Shield: Kigali Breach")
clock = pygame.time.Clock()

FONT_XL = pygame.font.SysFont("segoeui", 58, bold=True)
FONT_L = pygame.font.SysFont("segoeui", 32, bold=True)
FONT_M = pygame.font.SysFont("segoeui", 24)
FONT_S = pygame.font.SysFont("consolas", 18)

def load_save():
    SAVE_DIR.mkdir(exist_ok=True)
    if SAVE_FILE.exists():
        try:
            return json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"best_score": 0, "last_name": "Player"}

def save_data(data):
    SAVE_DIR.mkdir(exist_ok=True)
    SAVE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

SAVE = load_save()

def glow_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    glow = font.render(text, True, (255, 255, 255))
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        r = glow.get_rect(center=(x+dx, y+dy) if center else (0,0))
        if center:
            screen.blit(glow, r)
    rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
    screen.blit(img, rect)
    return rect

class Button:
    def __init__(self, rect, text, color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
    def draw(self, mouse):
        hovered = self.rect.collidepoint(mouse)
        base = self.color
        border = WHITE if hovered else base
        pygame.draw.rect(screen, PANEL, self.rect, border_radius=16)
        pygame.draw.rect(screen, border, self.rect, 3, border_radius=16)
        glow_text(self.text, FONT_M, WHITE, self.rect.centerx, self.rect.centery)
    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class Particle:
    def __init__(self, x, y, color):
        ang = random.random() * math.tau
        speed = random.uniform(1.0, 4.5)
        self.x, self.y = x, y
        self.vx = math.cos(ang) * speed
        self.vy = math.sin(ang) * speed
        self.life = random.randint(18, 40)
        self.color = color
        self.r = random.randint(2, 5)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)

class Player:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.speed = 5
        self.radius = 18
        self.hp = 100
        self.energy = 100
        self.shield_cd = 0
        self.patch_cd = 0
    def update(self, keys):
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        mag = math.hypot(dx, dy)
        if mag:
            dx, dy = dx / mag, dy / mag
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(40, min(WIDTH - 40, self.x))
        self.y = max(80, min(HEIGHT - 40, self.y))
        self.energy = min(100, self.energy + 0.08)
        self.shield_cd = max(0, self.shield_cd - 1)
        self.patch_cd = max(0, self.patch_cd - 1)
    def draw(self, mx, my):
        ang = math.atan2(my - self.y, mx - self.x)
        p1 = (self.x + math.cos(ang) * 26, self.y + math.sin(ang) * 26)
        p2 = (self.x + math.cos(ang + 2.4) * 18, self.y + math.sin(ang + 2.4) * 18)
        p3 = (self.x + math.cos(ang - 2.4) * 18, self.y + math.sin(ang - 2.4) * 18)
        pygame.draw.circle(screen, (30, 80, 120), (int(self.x), int(self.y)), 28, 2)
        pygame.draw.polygon(screen, CYAN, [p1, p2, p3])
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 4)

class Bullet:
    def __init__(self, x, y, tx, ty, strong=False):
        ang = math.atan2(ty - y, tx - x)
        self.x, self.y = x, y
        speed = 13 if not strong else 9
        self.vx = math.cos(ang) * speed
        self.vy = math.sin(ang) * speed
        self.r = 5 if not strong else 9
        self.dmg = 18 if not strong else 40
        self.color = CYAN if not strong else MAGENTA
    def update(self):
        self.x += self.vx
        self.y += self.vy
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)
    def offscreen(self):
        return not (-20 <= self.x <= WIDTH + 20 and -20 <= self.y <= HEIGHT + 20)

class Enemy:
    def __init__(self, wave):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x, self.y = random.randint(0, WIDTH), -30
        elif edge == "bottom":
            self.x, self.y = random.randint(0, WIDTH), HEIGHT + 30
        elif edge == "left":
            self.x, self.y = -30, random.randint(60, HEIGHT)
        else:
            self.x, self.y = WIDTH + 30, random.randint(60, HEIGHT)
        self.hp = 24 + wave * 4
        self.speed = min(1.7 + wave * 0.08, 4.2)
        self.r = random.randint(14, 24)
        self.color = random.choice([RED, YELLOW, MAGENTA])
    def update(self, px, py):
        ang = math.atan2(py - self.y, px - self.x)
        self.x += math.cos(ang) * self.speed
        self.y += math.sin(ang) * self.speed
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r, 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 6)

class Token:
    def __init__(self):
        self.x = random.randint(80, WIDTH - 80)
        self.y = random.randint(120, HEIGHT - 80)
        self.r = 10
        self.t = 0
    def update(self):
        self.t += 0.12
    def draw(self):
        rr = self.r + int(math.sin(self.t) * 2)
        pygame.draw.circle(screen, GREEN, (self.x, self.y), rr, 2)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 4)

def draw_background(tick):
    screen.fill(BG)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)
    for i in range(16):
        x = (i * 83 + tick * (0.2 + i * 0.03)) % WIDTH
        y = 40 + (i * 37) % HEIGHT
        pygame.draw.circle(screen, (20, 55, 88), (int(x), int(y)), 2)

def hud(player, score, wave, combo, name):
    pygame.draw.rect(screen, PANEL, (20, 16, WIDTH - 40, 52), border_radius=16)
    pygame.draw.rect(screen, CYAN, (20, 16, WIDTH - 40, 52), 2, border_radius=16)

    glow_text(f"Agent: {name}", FONT_S, WHITE, 90, 42)
    glow_text(f"Score: {score}", FONT_S, WHITE, 300, 42)
    glow_text(f"Wave: {wave}", FONT_S, WHITE, 470, 42)
    glow_text(f"Combo: x{combo}", FONT_S, WHITE, 630, 42)

    pygame.draw.rect(screen, (40, 50, 70), (810, 30, 160, 12), border_radius=8)
    pygame.draw.rect(screen, RED, (810, 30, int(160 * max(player.hp, 0) / 100), 12), border_radius=8)
    glow_text("HP", FONT_S, WHITE, 785, 36)

    pygame.draw.rect(screen, (40, 50, 70), (1080, 30, 160, 12), border_radius=8)
    pygame.draw.rect(screen, GREEN, (1080, 30, int(160 * player.energy / 100), 12), border_radius=8)
    glow_text("Energy", FONT_S, WHITE, 1025, 36)

def main_menu():
    name = SAVE.get("last_name", "Player")
    difficulty = "Normal"
    buttons = [
        Button((520, 270, 240, 54), "Start Mission", CYAN),
        Button((520, 340, 240, 54), "Difficulty", MAGENTA),
        Button((520, 410, 240, 54), "Help", GREEN),
        Button((520, 480, 240, 54), "Quit", RED),
    ]
    input_active = False
    tick = 0
    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(tick)
        tick += 1
        glow_text("CYBER SHIELD", FONT_XL, CYAN, WIDTH // 2, 110)
        glow_text("KIGALI BREACH", FONT_L, WHITE, WIDTH // 2, 160)

        pygame.draw.rect(screen, PANEL, (430, 205, 420, 60), border_radius=18)
        pygame.draw.rect(screen, SOFT if input_active else CYAN, (430, 205, 420, 60), 2, border_radius=18)
        glow_text("Agent Name", FONT_S, WHITE, 500, 222, center=False)
        txt = FONT_M.render(name, True, WHITE)
        screen.blit(txt, (458, 232))

        diff_text = f"Difficulty: {difficulty}"
        glow_text(diff_text, FONT_S, YELLOW, WIDTH // 2, 610)

        best = SAVE.get("best_score", 0)
        glow_text(f"Best Score: {best}", FONT_S, GREEN, WIDTH // 2, 645)

        for b in buttons:
            b.draw(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                    elif len(name) < 16 and event.unicode.isprintable():
                        name += event.unicode
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = pygame.Rect(430, 205, 420, 60).collidepoint(event.pos)
                if buttons[0].clicked(event):
                    SAVE["last_name"] = name or "Player"
                    save_data(SAVE)
                    return name or "Player", difficulty
                elif buttons[1].clicked(event):
                    difficulty = {"Easy":"Normal", "Normal":"Hard", "Hard":"Easy"}[difficulty]
                elif buttons[2].clicked(event):
                    help_screen()
                elif buttons[3].clicked(event):
                    return None, None
        pygame.display.flip()
        clock.tick(FPS)

def help_screen():
    tick = 0
    back = Button((40, 40, 150, 48), "Back", CYAN)
    lines = [
        "Defend the grid from breach packets.",
        "Left click = firewall pulse.",
        "Right click = strong patch burst.",
        "Space = shield dash.",
        "Collect green tokens to boost score and recover energy.",
        "Do not let enemies touch you for too long.",
        "Stay alive as waves increase."
    ]
    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(tick); tick += 1
        glow_text("HELP / CONTROLS", FONT_L, CYAN, WIDTH // 2, 100)
        y = 200
        for line in lines:
            glow_text(line, FONT_M, WHITE, WIDTH // 2, y)
            y += 55
        back.draw(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()
            if back.clicked(event):
                return
        pygame.display.flip()
        clock.tick(FPS)

def toggle_fullscreen():
    global screen
    if screen.get_flags() & pygame.FULLSCREEN:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

def game_loop(name, difficulty):
    player = Player()
    bullets = []
    enemies = []
    particles = []
    tokens = [Token()]
    score = 0
    combo = 1
    wave = 1
    spawn_timer = 0
    running = True
    paused = False
    tick = 0

    difficulty_scale = {"Easy": 0.85, "Normal": 1.0, "Hard": 1.18}[difficulty]

    while running:
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    paused = not paused
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE and player.energy >= 35 and player.shield_cd == 0:
                    mx, my = mouse
                    ang = math.atan2(my - player.y, mx - player.x)
                    player.x += math.cos(ang) * 100
                    player.y += math.sin(ang) * 100
                    player.energy -= 35
                    player.shield_cd = 50
                    for _ in range(20):
                        particles.append(Particle(player.x, player.y, CYAN))
            if event.type == pygame.MOUSEBUTTONDOWN and not paused:
                if event.button == 1:
                    bullets.append(Bullet(player.x, player.y, *mouse, strong=False))
                elif event.button == 3 and player.patch_cd == 0 and player.energy >= 22:
                    bullets.append(Bullet(player.x, player.y, *mouse, strong=True))
                    player.energy -= 22
                    player.patch_cd = 25

        if not paused:
            tick += 1
            player.update(keys)

            spawn_timer += 1
            threshold = max(18, int(60 / difficulty_scale) - wave * 2)
            if spawn_timer >= threshold:
                spawn_timer = 0
                enemies.append(Enemy(wave))

            if tick % 600 == 0:
                wave += 1
                tokens.append(Token())

            for b in bullets[:]:
                b.update()
                if b.offscreen():
                    bullets.remove(b)

            for e in enemies[:]:
                e.update(player.x, player.y)
                if math.hypot(e.x - player.x, e.y - player.y) < e.r + player.radius:
                    player.hp -= 0.35 * difficulty_scale
                    if player.hp <= 0:
                        running = False

            for t in tokens:
                t.update()

            for t in tokens[:]:
                if math.hypot(t.x - player.x, t.y - player.y) < t.r + player.radius:
                    score += 80 * combo
                    player.energy = min(100, player.energy + 18)
                    player.hp = min(100, player.hp + 6)
                    combo = min(9, combo + 1)
                    tokens.remove(t)
                    tokens.append(Token())
                    for _ in range(18):
                        particles.append(Particle(t.x, t.y, GREEN))

            for b in bullets[:]:
                for e in enemies[:]:
                    if math.hypot(b.x - e.x, b.y - e.y) < b.r + e.r:
                        e.hp -= b.dmg
                        if b in bullets:
                            bullets.remove(b)
                        for _ in range(7):
                            particles.append(Particle(e.x, e.y, b.color))
                        if e.hp <= 0 and e in enemies:
                            enemies.remove(e)
                            score += 25 * combo
                            combo = min(9, combo + 1)
                            for _ in range(14):
                                particles.append(Particle(e.x, e.y, YELLOW))
                        break

            if tick % 180 == 0:
                combo = max(1, combo - 1)

            for p in particles[:]:
                p.update()
                if p.life <= 0:
                    particles.remove(p)

        draw_background(tick)
        for t in tokens: t.draw()
        for b in bullets: b.draw()
        for e in enemies: e.draw()
        for p in particles: p.draw()
        player.draw(*mouse)
        hud(player, score, wave, combo, name)

        if paused:
            pygame.draw.rect(screen, (0,0,0), (0,0,WIDTH,HEIGHT))
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            screen.blit(s, (0, 0))
            glow_text("PAUSED", FONT_XL, WHITE, WIDTH // 2, HEIGHT // 2 - 30)
            glow_text("Press ESC or P to continue", FONT_M, CYAN, WIDTH // 2, HEIGHT // 2 + 30)

        pygame.display.flip()
        clock.tick(FPS)

    best = SAVE.get("best_score", 0)
    if score > best:
        SAVE["best_score"] = score
        save_data(SAVE)
    game_over(score, SAVE.get("best_score", score), name)

def game_over(score, best, name):
    again = Button((470, 430, 340, 58), "Return to Menu", CYAN)
    tick = 0
    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(tick); tick += 1
        glow_text("SYSTEM BREACHED", FONT_XL, RED, WIDTH // 2, 170)
        glow_text(f"Agent: {name}", FONT_M, WHITE, WIDTH // 2, 290)
        glow_text(f"Score: {score}", FONT_L, YELLOW, WIDTH // 2, 340)
        glow_text(f"Best Score: {best}", FONT_M, GREEN, WIDTH // 2, 385)
        again.draw(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()
            if again.clicked(event):
                return
        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        name, difficulty = main_menu()
        if not name:
            break
        game_loop(name, difficulty)
    pygame.quit()

if __name__ == "__main__":
    main()
