import os
import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値:真理値タプル（横、縦）/ 画面内:True 画面外:False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に画面をブラックアウトし、
    泣いているこうかとん画像と「Game Over」を表示する関数。
    
    
    screen (pg.Surface): ゲーム画面のSurface
    """
    font = pg.font.Font(None, 80)  # フォント設定
    gameover_text = font.render("Game Over", True, (255, 255, 255))  # テキスト描画
    gameover_rect = gameover_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    black_overlay = pg.Surface((WIDTH, HEIGHT))
    black_overlay.set_alpha(128)  # 半透明設定
    black_overlay.fill((0, 0, 0))

    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    crying_kk_rect = crying_kk_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(black_overlay, (0, 0))
    screen.blit(crying_kk_img, crying_kk_rect)
    screen.blit(gameover_text, gameover_rect)
    pg.display.update()
    pg.time.wait(5000)  # 5秒間待機


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
