import pygame
import random
import sys
import os

# 初始化 pygame
pygame.init()


def _load_chinese_font(size):
    """加载支持中文的字体，绕开 pygame.SysFont 在 Python 3.12 下的 Bug"""
    # Windows 常见中文字体路径
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",      # 微软雅黑
        r"C:\Windows\Fonts\simhei.ttf",    # 黑体
        r"C:\Windows\Fonts\simsun.ttc",    # 宋体
    ]
    for path in candidates:
        if os.path.exists(path):
            return pygame.font.Font(path, size)
    # 都找不到则使用默认字体（中文可能显示方块）
    return pygame.font.Font(None, size)

# ============ 常量配置 ============
CELL_SIZE = 20          # 每个格子的像素大小
GRID_W, GRID_H = 30, 20  # 网格宽高（格子数）
SCREEN_W = CELL_SIZE * GRID_W  # 600
SCREEN_H = CELL_SIZE * GRID_H  # 400
FPS = 10

# 颜色
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GREEN   = (0, 200, 0)
DGREEN  = (0, 155, 0)
RED     = (220, 50, 50)
GRAY    = (40, 40, 40)
GOLD    = (255, 215, 0)

# 方向
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()
        self.font = _load_chinese_font(28)
        self.big_font = _load_chinese_font(48)
        self.reset()

    def reset(self):
        """重置游戏状态"""
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = self._spawn_food()
        self.score = 0
        self.alive = True

    def _spawn_food(self):
        """在不与蛇身重叠的位置生成食物"""
        while True:
            pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
            if pos not in self.snake:
                return pos

    # ---------- 输入处理 ----------
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.alive:
                    key_map = {
                        pygame.K_UP: UP, pygame.K_w: UP,
                        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
                    }
                    if event.key in key_map:
                        new_dir = key_map[event.key]
                        # 禁止 180° 掉头
                        if (new_dir[0] + self.direction[0] != 0 or
                                new_dir[1] + self.direction[1] != 0):
                            self.next_direction = new_dir
                else:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # ---------- 逻辑更新 ----------
    def update(self):
        if not self.alive:
            return
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)

        # 碰墙检测
        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            self.alive = False
            return
        # 碰自身检测
        if new_head in self.snake:
            self.alive = False
            return

        self.snake.insert(0, new_head)

        # 吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    # ---------- 画面渲染 ----------
    def draw(self):
        self.screen.fill(BLACK)

        # 画网格（淡色背景线）
        for x in range(0, SCREEN_W, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_H))
        for y in range(0, SCREEN_H, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_W, y))

        # 画蛇
        for i, (x, y) in enumerate(self.snake):
            color = GREEN if i == 0 else DGREEN
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        # 画食物
        fx, fy = self.food
        food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, food_rect)
        pygame.draw.rect(self.screen, BLACK, food_rect, 1)

        # 画分数
        score_surf = self.font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 5))

        # 游戏结束画面
        if not self.alive:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            go_surf = self.big_font.render("游戏结束", True, GOLD)
            go_rect = go_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 30))
            self.screen.blit(go_surf, go_rect)

            score_surf = self.font.render(f"最终得分: {self.score}", True, WHITE)
            score_rect = score_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 15))
            self.screen.blit(score_surf, score_rect)

            hint_surf = self.font.render("空格键重新开始 / ESC 退出", True, WHITE)
            hint_rect = hint_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 55))
            self.screen.blit(hint_surf, hint_rect)

        pygame.display.flip()

    # ---------- 主循环 ----------
    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
