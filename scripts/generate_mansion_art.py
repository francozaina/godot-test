import os, zlib, struct

os.makedirs('assets/mansion', exist_ok=True)

def save_png(filename, width, height, pixels):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    
    raw = bytearray()
    for y in range(height):
        raw.append(0) # filter type 0 (None)
        for x in range(width):
            c = pixels[y][x]
            if len(c) == 3:
                raw.extend([c[0], c[1], c[2], 255])
            else:
                raw.extend(c)
                
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    idat = chunk(b'IDAT', zlib.compress(bytes(raw)))
    iend = chunk(b'IEND', b'')
    with open(filename, 'wb') as f:
        f.write(header + ihdr + idat + iend)

CLR = (0, 0, 0, 0)

# ==============================================================================
# 1. VICTORIAN WALL (32x48)
# Top 24 px: deep teal wallpaper with damask pinstripes
# Middle 4 px: carved dark mahogany rail
# Lower 18 px: vertical dark wood wainscot panels
# Bottom 2 px: baseboard
# ==============================================================================
wall = [[CLR for _ in range(32)] for _ in range(48)]

# Colors
C_TOP_CORNICE = (40, 72, 64)
C_WALL_BASE   = (25, 48, 42)
C_WALL_DARK   = (19, 36, 31)
C_WALL_LIGHT  = (33, 62, 54)
C_RAIL_LIGHT  = (110, 68, 42)
C_RAIL_MID    = (75, 45, 27)
C_RAIL_DARK   = (40, 22, 12)
C_WOOD_BASE   = (55, 32, 19)
C_WOOD_LIGHT  = (72, 43, 26)
C_WOOD_DARK   = (38, 21, 12)
C_BASEBOARD   = (26, 14, 8)

for y in range(48):
    for x in range(32):
        if y < 2:
            wall[y][x] = C_TOP_CORNICE
        elif y < 24: # Teal wallpaper
            if x % 8 in (0, 1): # Subtle elegant vertical stripe
                wall[y][x] = C_WALL_LIGHT
            elif (x + y) % 6 == 0:
                wall[y][x] = C_WALL_DARK
            else:
                wall[y][x] = C_WALL_BASE
        elif y == 24: # Rail highlight
            wall[y][x] = C_RAIL_LIGHT
        elif y == 25: # Rail body
            wall[y][x] = C_RAIL_MID
        elif y == 26: # Rail shadow
            wall[y][x] = C_RAIL_DARK
        elif y < 45: # Wainscoting wood panels
            # Panels every 8 pixels (x%8 == 0 is dark seam, x%8 == 1 is light edge)
            if x % 8 == 0:
                wall[y][x] = C_WOOD_DARK
            elif x % 8 == 1:
                wall[y][x] = C_WOOD_LIGHT
            elif y in (28, 43): # Inset panel horizontal line
                wall[y][x] = C_WOOD_DARK
            else:
                wall[y][x] = C_WOOD_BASE
        elif y < 47: # Baseboard molding
            wall[y][x] = C_WOOD_DARK
        else: # Bottom contact shadow
            wall[y][x] = C_BASEBOARD

save_png('assets/mansion/wall_victorian.png', 32, 48, wall)

# ==============================================================================
# 2. VICTORIAN RUG / CARPET TILE (32x32)
# Rich deep teal textured velvet with antique gold pattern
# ==============================================================================
carpet = [[(22, 44, 38) for _ in range(32)] for _ in range(32)]
import random
random.seed(101)
for y in range(32):
    for x in range(32):
        r = (x * 7 + y * 13) % 11
        if r == 0:
            carpet[y][x] = (16, 34, 29)
        elif r == 3:
            carpet[y][x] = (28, 54, 47)
        elif r == 7:
            carpet[y][x] = (25, 48, 42)

save_png('assets/mansion/carpet_center.png', 32, 32, carpet)

# Carpet with gold border edge (for rugs)
carpet_border = [row[:] for row in carpet]
GOLD_BRIGHT = (195, 155, 65)
GOLD_MID    = (150, 115, 45)
GOLD_DARK   = (90, 65, 25)
for y in range(32):
    for x in range(32):
        # 3px ornate gold border on top
        if y in (1, 2):
            carpet_border[y][x] = GOLD_MID if x % 4 in (0, 1) else GOLD_BRIGHT
        elif y == 0:
            carpet_border[y][x] = GOLD_DARK

save_png('assets/mansion/carpet_border_top.png', 32, 32, carpet_border)

# ==============================================================================
# 2B. GRAND ORNATE VICTORIAN RUG (160x128) - 5x4 tiles
# Rich emerald velvet with baroque gold border, filigree corner brackets, and center medallion
# ==============================================================================
rug = [[(20, 40, 35, 255) for _ in range(160)] for _ in range(128)]
C_FRINGE_LIGHT = (220, 195, 140)
C_FRINGE_DARK  = (140, 110, 60)
C_BURGUNDY_DARK = (70, 20, 30)
C_BURGUNDY_MID  = (110, 30, 45)

for y in range(128):
    for x in range(160):
        # Tassels / Fringe along top and bottom (rows 0-2 and 125-127)
        if y in (0, 127):
            rug[y][x] = C_FRINGE_LIGHT if x % 3 == 0 else (0, 0, 0, 0)
        elif y in (1, 126):
            rug[y][x] = C_FRINGE_DARK if x % 3 == 0 else C_FRINGE_LIGHT
        elif y in (2, 125):
            rug[y][x] = (45, 30, 15) # Dark fringe binding stitch
        # Outer Rug Boundary
        elif y in (3, 124) or x in (2, 157):
            rug[y][x] = GOLD_DARK
        elif y in (4, 123) or x in (3, 156):
            rug[y][x] = GOLD_BRIGHT
        # Ornate Gold & Burgundy Border Band (rows 5..14, cols 4..13 and equivalents)
        elif y < 14 or y >= 114 or x < 14 or x >= 146:
            dist_edge = min(y - 4, 123 - y, x - 3, 156 - x)
            if dist_edge in (2, 7):
                rug[y][x] = GOLD_MID
            elif dist_edge in (3, 6):
                rug[y][x] = GOLD_BRIGHT if (x + y) % 4 == 0 else C_BURGUNDY_MID
            elif dist_edge in (4, 5):
                rug[y][x] = C_BURGUNDY_DARK if (x * y) % 3 == 0 else C_BURGUNDY_MID
            else:
                rug[y][x] = GOLD_DARK
        elif y in (14, 113) or x in (14, 145):
            rug[y][x] = GOLD_BRIGHT # Inner gold piping
        elif y in (15, 112) or x in (15, 144):
            rug[y][x] = GOLD_DARK
        else:
            # Inner field: Deep Emerald Velvet with diamond quilting / damask
            dx = abs(x - 80)
            dy = abs(y - 64)
            # Center baroque medallion (ellipse roughly 36x24)
            ellipse_d = (dx / 32.0)**2 + (dy / 22.0)**2
            if ellipse_d < 0.2:
                rug[y][x] = GOLD_BRIGHT if (x + y) % 2 == 0 else (240, 215, 110)
            elif ellipse_d < 0.4:
                rug[y][x] = C_BURGUNDY_MID if (x + y) % 3 != 0 else GOLD_MID
            elif ellipse_d < 0.7:
                rug[y][x] = (16, 46, 38)
            elif ellipse_d < 0.95:
                rug[y][x] = GOLD_MID if (x + y) % 2 == 0 else GOLD_BRIGHT
            elif ellipse_d < 1.05:
                rug[y][x] = (14, 30, 26)
            else:
                # Field diamond pattern
                if (x + y) % 12 in (0, 1) or (x - y) % 12 in (0, 1):
                    rug[y][x] = (28, 58, 50)
                else:
                    grain = (x * 7 + y * 13) % 11
                    if grain == 0:
                        rug[y][x] = (16, 34, 29)
                    elif grain == 3:
                        rug[y][x] = (25, 52, 45)
                    else:
                        rug[y][x] = (20, 42, 36)

save_png('assets/mansion/victorian_rug.png', 160, 128, rug)

# ==============================================================================
# 3. POLISHED DARK PARQUET FLOOR (32x32)
# ==============================================================================
floor_wood = [[(45, 27, 16) for _ in range(32)] for _ in range(32)]
for y in range(32):
    plank = y // 8
    is_seam_y = (y % 8 == 7)
    for x in range(32):
        if is_seam_y:
            floor_wood[y][x] = (22, 12, 7)
            continue
        offset = (plank % 2) * 16
        if (x + offset) % 32 == 31:
            floor_wood[y][x] = (22, 12, 7)
            continue
        # Wood grain
        grain = (x * 5 + y * 7) % 7
        if grain == 0:
            floor_wood[y][x] = (56, 34, 20)
        elif grain == 3:
            floor_wood[y][x] = (36, 21, 12)

save_png('assets/mansion/wood_floor.png', 32, 32, floor_wood)

# ==============================================================================
# 4. BOOKCASE (64x64) - 2x2 tiles
# Grand dark mahogany bookcase filled with colorful leather books, scrolls, hourglass
# ==============================================================================
bookcase = [[CLR for _ in range(64)] for _ in range(64)]
WOOD_OUT = (24, 13, 8)
WOOD_MID = (65, 38, 22)
WOOD_LGT = (90, 55, 32)
WOOD_SHD = (40, 22, 13)
WOOD_IN  = (28, 16, 10)

# Outer frame
for y in range(2, 63):
    for x in range(3, 61):
        if x in (3, 4, 59, 60) or y in (2, 3, 61, 62):
            bookcase[y][x] = WOOD_OUT
        elif x in (5, 6, 57, 58) or y in (4, 5):
            bookcase[y][x] = WOOD_LGT
        else:
            bookcase[y][x] = WOOD_IN

# Top carved crown / pediment
for x in range(5, 59):
    bookcase[3][x] = WOOD_LGT
    bookcase[2][x] = WOOD_OUT
    bookcase[1][x] = WOOD_OUT if x in (5, 6, 57, 58, 31, 32) else CLR

# Horizontal shelves at y=20, y=36, y=52
shelves_y = [20, 36, 52]
for sy in shelves_y:
    for x in range(6, 58):
        bookcase[sy][x] = WOOD_LGT
        bookcase[sy+1][x] = WOOD_MID
        bookcase[sy+2][x] = WOOD_SHD

# Books on shelves
# Colors of leather bound books
B_RED   = ((160, 40, 45), (120, 25, 30))
B_BLUE  = ((35, 65, 130), (22, 42, 85))
B_GREEN = ((35, 110, 60), (22, 75, 40))
B_BROWN = ((130, 80, 40), (95, 55, 25))
B_GOLD  = ((190, 150, 50), (140, 105, 30))
B_PURP  = ((100, 35, 110), (70, 22, 80))
B_PAGES = (220, 215, 195)

def draw_books(shelf_bottom_y, books_desc):
    # books_desc: list of (width, height, color_pair, slant_offset)
    curr_x = 8
    for bw, bh, (c_l, c_d), slant in books_desc:
        if curr_x + bw > 56: break
        for by in range(shelf_bottom_y - bh, shelf_bottom_y):
            for bx in range(curr_x, curr_x + bw):
                # Slant
                sx = bx + int((shelf_bottom_y - by) * slant)
                if 6 <= sx <= 57:
                    # Spine highlight on left, shadow on right, gold rib in middle
                    if bx == curr_x:
                        bookcase[by][sx] = c_l
                    elif bx == curr_x + bw - 1:
                        bookcase[by][sx] = c_d
                    elif (by - (shelf_bottom_y - bh)) % 4 == 0:
                        bookcase[by][sx] = (220, 185, 80) # Gold rib on spine
                    else:
                        bookcase[by][sx] = c_l
        curr_x += bw + 1

# Top shelf books (shelf at 20, books y=7..19)
draw_books(20, [
    (3, 11, B_RED, 0), (2, 13, B_BLUE, 0), (3, 12, B_GOLD, 0),
    (4, 10, B_GREEN, 0), (3, 13, B_PURP, 0), (2, 11, B_BROWN, 0),
    (3, 14, B_BLUE, 0), (3, 10, B_RED, 0.2), (2, 9, B_GOLD, 0.3),
    (3, 12, B_GREEN, 0), (4, 11, B_BROWN, 0), (2, 13, B_PURP, 0)
])

# Middle shelf books (shelf at 36, books y=23..35)
draw_books(36, [
    (4, 12, B_BLUE, 0), (3, 14, B_RED, 0), (2, 10, B_GOLD, 0),
    (3, 13, B_BROWN, 0), (4, 11, B_GREEN, 0), (2, 9, B_PURP, 0),
    (3, 12, B_RED, 0), (3, 13, B_BLUE, 0), (4, 10, B_GOLD, 0),
    (2, 12, B_GREEN, 0), (3, 14, B_BROWN, 0), (3, 11, B_PURP, 0)
])

# Bottom shelf books (shelf at 52, books y=39..51)
draw_books(52, [
    (4, 13, B_GREEN, 0), (3, 11, B_PURP, 0), (4, 14, B_BROWN, 0),
    (3, 12, B_BLUE, 0), (2, 10, B_RED, 0), (4, 13, B_GOLD, 0),
    (3, 11, B_GREEN, 0), (3, 14, B_PURP, 0), (4, 12, B_BLUE, 0),
    (2, 9, B_BROWN, 0), (3, 13, B_RED, 0)
])

# Base cabinets with decorative panel trims at y=55..61
for y in range(54, 61):
    for x in range(7, 57):
        if x in (7, 31, 32, 56) or y in (54, 60):
            bookcase[y][x] = WOOD_OUT
        elif x in (8, 30, 33, 55) or y == 55:
            bookcase[y][x] = WOOD_LGT
        elif x in (19, 44) and y == 57:
            bookcase[y][x] = GOLD_BRIGHT # Brass keyhole / handle
        else:
            bookcase[y][x] = WOOD_MID

save_png('assets/mansion/bookcase.png', 64, 64, bookcase)

# ==============================================================================
# 5. STUDY DESK (64x36) - 2x1 tiles
# Carved mahogany desk with drawers, open letter, inkwell, quill & banker's lamp
# ==============================================================================
desk = [[CLR for _ in range(64)] for _ in range(36)]

# Desktop surface: y=8..16, x=4..59
for y in range(8, 17):
    for x in range(4, 60):
        if y == 8:
            desk[y][x] = WOOD_LGT
        elif y == 9:
            desk[y][x] = (100, 60, 35) # Wood surface highlight
        elif y in (15, 16):
            desk[y][x] = WOOD_SHD
        elif x in (4, 59):
            desk[y][x] = WOOD_OUT
        else:
            desk[y][x] = WOOD_MID

# Desk pedestals/drawers on left (x=5..19) and right (x=44..58)
for y in range(17, 34):
    for x in range(5, 20):
        if x in (5, 19) or y in (17, 24, 31, 33):
            desk[y][x] = WOOD_OUT
        elif x in (6, 18) or y in (18, 25):
            desk[y][x] = WOOD_LGT
        elif x == 12 and y in (21, 28):
            desk[y][x] = GOLD_BRIGHT # Brass drawer pull
        else:
            desk[y][x] = WOOD_MID
            
    for x in range(44, 59):
        if x in (44, 58) or y in (17, 24, 31, 33):
            desk[y][x] = WOOD_OUT
        elif x in (45, 57) or y in (18, 25):
            desk[y][x] = WOOD_LGT
        elif x == 51 and y in (21, 28):
            desk[y][x] = GOLD_BRIGHT # Brass drawer pull
        else:
            desk[y][x] = WOOD_MID

# Desktop items:
# 1. Vintage Banker's Lamp / Brass Lamp on the left (x=9..15, y=0..8)
LAMP_GRN_LGT = (55, 175, 95)
LAMP_GRN_MID = (30, 115, 60)
LAMP_GRN_DRK = (18, 65, 35)
BRASS_LGT    = (240, 205, 80)
BRASS_MID    = (185, 140, 45)

# Lamp brass stand
for y in range(3, 9):
    desk[y][12] = BRASS_LGT
desk[8][11] = BRASS_MID; desk[8][13] = BRASS_MID # Base
desk[7][10] = BRASS_LGT; desk[7][14] = BRASS_LGT
# Emerald glass shade
for x in range(8, 17):
    desk[1][x] = LAMP_GRN_LGT
    desk[2][x] = LAMP_GRN_MID
    desk[3][x] = (255, 245, 170) if 10 <= x <= 14 else LAMP_GRN_DRK # Warm glow underside

# 2. Open letter / parchment on desk (x=24..34, y=10..14)
for y in range(10, 15):
    for x in range(24, 35):
        if y == 14 or x in (24, 34):
            desk[y][x] = (210, 200, 170)
        elif y == 12 and 26 <= x <= 32 and x % 2 == 0:
            desk[y][x] = (60, 50, 45) # Handwritten cursive text
        elif y == 13 and 26 <= x <= 31 and x % 2 == 1:
            desk[y][x] = (60, 50, 45)
        else:
            desk[y][x] = (245, 238, 215) # Parchment paper

# 3. Inkwell and Feather Quill (x=38..42, y=6..10)
desk[9][39] = (30, 30, 40) # Glass bottle
desk[9][40] = (20, 20, 25)
desk[8][39] = (210, 180, 80) # Brass cap
# White feather quill slanting up-right
desk[7][40] = (235, 235, 245)
desk[6][41] = (245, 245, 255)
desk[5][42] = (245, 245, 255)

# 4. Leather journal with brass clasp (x=46..54, y=10..14)
for y in range(10, 15):
    for x in range(46, 55):
        if x in (46, 54) or y in (10, 14):
            desk[y][x] = (95, 25, 35) # Burgundy leather
        elif x == 50 and y == 12:
            desk[y][x] = BRASS_LGT # Clasp
        else:
            desk[y][x] = (135, 38, 50)

save_png('assets/mansion/study_desk.png', 64, 36, desk)

# ==============================================================================
# 6. VELVET ARMCHAIR (32x36) - 1x1 tile
# Deep wine red / burgundy tufted armchair with dark mahogany wooden frame
# ==============================================================================
chair = [[CLR for _ in range(32)] for _ in range(36)]
V_DRK = (70, 18, 28)
V_MID = (120, 32, 48)
V_LGT = (165, 48, 70)
V_HGT = (200, 75, 100)
T_GOLD = (210, 170, 70) # Brass tuft button

# Backrest (y=2..18, x=6..25)
for y in range(2, 19):
    for x in range(6, 26):
        if y in (2, 3) or x in (6, 25):
            chair[y][x] = V_DRK
        elif (x in (10, 16, 21) and y in (6, 11, 15)):
            chair[y][x] = T_GOLD # Diamond tufting button
        elif (x + y) % 4 == 0:
            chair[y][x] = V_HGT
        else:
            chair[y][x] = V_MID

# Armrests on left (x=3..7) and right (x=24..28) at y=14..26
for y in range(14, 27):
    for x in range(3, 8):
        if x == 3 or y == 14:
            chair[y][x] = WOOD_OUT
        elif x in (4, 5) and y in (15, 16):
            chair[y][x] = WOOD_LGT
        else:
            chair[y][x] = V_MID
            
    for x in range(24, 29):
        if x == 28 or y == 14:
            chair[y][x] = WOOD_OUT
        elif x in (26, 27) and y in (15, 16):
            chair[y][x] = WOOD_LGT
        else:
            chair[y][x] = V_MID

# Seat cushion (y=19..28, x=7..24)
for y in range(19, 29):
    for x in range(7, 25):
        if y in (19, 20):
            chair[y][x] = V_HGT
        elif y in (27, 28):
            chair[y][x] = V_DRK
        else:
            chair[y][x] = V_MID

# Wooden turned legs at bottom (y=29..35)
chair[29][5] = WOOD_MID; chair[30][5] = WOOD_LGT; chair[31][5] = WOOD_OUT; chair[32][5] = WOOD_OUT
chair[29][26] = WOOD_MID; chair[30][26] = WOOD_LGT; chair[31][26] = WOOD_OUT; chair[32][26] = WOOD_OUT

save_png('assets/mansion/armchair.png', 32, 36, chair)

# ==============================================================================
# 7. FIREPLACE (64x48) - 2x1.5 tiles
# Dark carved stone/mahogany fireplace with mantle clock, candlesticks & burning logs
# ==============================================================================
fireplace = [[CLR for _ in range(64)] for _ in range(48)]

# Mantle top shelf: y=4..9, x=4..59
for y in range(4, 10):
    for x in range(4, 60):
        if y == 4:
            fireplace[y][x] = WOOD_LGT
        elif y == 5:
            fireplace[y][x] = (100, 60, 35)
        elif y == 9:
            fireplace[y][x] = WOOD_OUT
        else:
            fireplace[y][x] = WOOD_MID

# Side pillars: left x=8..18, right x=45..55, y=10..45
for y in range(10, 46):
    for x in range(8, 19):
        if x in (8, 18) or y in (10, 45):
            fireplace[y][x] = WOOD_OUT
        elif x == 9 or y == 11:
            fireplace[y][x] = WOOD_LGT
        else:
            fireplace[y][x] = WOOD_MID
            
    for x in range(45, 56):
        if x in (45, 55) or y in (10, 45):
            fireplace[y][x] = WOOD_OUT
        elif x == 46 or y == 11:
            fireplace[y][x] = WOOD_LGT
        else:
            fireplace[y][x] = WOOD_MID

# Inner hearth / firebox: x=19..44, y=10..45
HEARTH_BK = (20, 16, 18)
HEARTH_BR = (38, 28, 30)
for y in range(10, 46):
    for x in range(19, 45):
        if y == 10 or x in (19, 44):
            fireplace[y][x] = (10, 8, 10) # Heavy shadow
        elif (x + y * 2) % 7 == 0:
            fireplace[y][x] = HEARTH_BR # Dark firebricks
        else:
            fireplace[y][x] = HEARTH_BK

# Fire logs & embers (y=34..44, x=24..39)
FIRE_YEL = (255, 235, 90)
FIRE_ORG = (255, 140, 30)
FIRE_RED = (220, 45, 20)
LOG_WOOD = (85, 45, 20)

# Fire logs
for x in range(25, 39):
    fireplace[42][x] = LOG_WOOD
    fireplace[43][x] = (50, 25, 12)
    fireplace[44][x] = (30, 15, 8)

# Glowing flames
for y in range(30, 42):
    for x in range(27, 37):
        dist_c = abs(x - 31.5)
        flame_h = 42 - y
        if flame_h < (10 - dist_c * 2):
            if dist_c < 1.5 and flame_h < 6:
                fireplace[y][x] = FIRE_YEL
            elif dist_c < 3:
                fireplace[y][x] = FIRE_ORG
            else:
                fireplace[y][x] = FIRE_RED

# Mantle Clock in center (x=28..35, y=0..4)
for y in range(0, 5):
    for x in range(28, 36):
        if y == 0 or x in (28, 35):
            fireplace[y][x] = GOLD_DARK
        elif x in (31, 32) and y in (1, 2):
            fireplace[y][x] = (245, 240, 220) # Clock face
        else:
            fireplace[y][x] = GOLD_BRIGHT

# Candlesticks on left (x=12) and right (x=51)
for y in range(0, 4):
    fireplace[y][12] = GOLD_BRIGHT
    fireplace[y][51] = GOLD_BRIGHT
# Candle flames
fireplace[0][12] = FIRE_ORG; fireplace[0][51] = FIRE_ORG

save_png('assets/mansion/fireplace.png', 64, 48, fireplace)

# ==============================================================================
# 8. NOCTURNAL WINDOW (32x48) - 1x1.5 tiles
# Arched Victorian window with moonlit starry sky, curtains & sill potted plant
# ==============================================================================
window = [[CLR for _ in range(32)] for _ in range(48)]

# Curtains (draped teal / wine lace): left x=2..8, right x=23..29
CURT_LGT = (35, 85, 75)
CURT_MID = (24, 60, 52)
CURT_DRK = (15, 38, 33)

# Night sky inside window frame: x=8..23, y=5..36
SKY_NIGHT = (14, 22, 38)
SKY_STARS = (220, 235, 255)
MOON_GLOW = (240, 248, 255)
TREE_SILH = (8, 12, 20)

for y in range(5, 37):
    for x in range(8, 24):
        # Frame wooden divider at x=15, 16 or y=20
        if x in (15, 16) or y == 20:
            window[y][x] = WOOD_OUT
        elif (x - 12)**2 + (y - 10)**2 <= 9: # Full glowing pale moon
            window[y][x] = MOON_GLOW
        elif (x == 20 and y == 8) or (x == 10 and y == 16) or (x == 21 and y == 26):
            window[y][x] = SKY_STARS # Distant stars
        elif y > 28 and ((x - 11) % 4 in (0, 1)):
            window[y][x] = TREE_SILH # Silhouetted tree branches outside
        else:
            window[y][x] = SKY_NIGHT

# Window frame & sill (y=37..43, x=6..25)
for y in range(37, 44):
    for x in range(6, 26):
        if y == 37:
            window[y][x] = WOOD_LGT
        elif y == 43:
            window[y][x] = WOOD_OUT
        else:
            window[y][x] = WOOD_MID

# Draped curtains with folds on the sides
for y in range(2, 38):
    for x in range(2, 9):
        if x in (2, 8): window[y][x] = CURT_DRK
        elif (x + y) % 3 == 0: window[y][x] = CURT_LGT
        else: window[y][x] = CURT_MID
    for x in range(23, 30):
        if x in (23, 29): window[y][x] = CURT_DRK
        elif (x + y) % 3 == 0: window[y][x] = CURT_LGT
        else: window[y][x] = CURT_MID

# Small terracotta flower pot on sill at center (x=13..18, y=32..37)
for y in range(34, 38):
    for x in range(14, 18):
        window[y][x] = (180, 85, 45) # Terracotta pot
# Green plant sprout
window[32][15] = (45, 135, 60); window[32][16] = (65, 175, 80)
window[33][14] = (55, 155, 70); window[33][17] = (45, 135, 60)

save_png('assets/mansion/victorian_window.png', 32, 48, window)

# ==============================================================================
# 9. OIL PAINTING IN ORNATE GOLD FRAME (32x32)
# ==============================================================================
painting = [[CLR for _ in range(32)] for _ in range(32)]

# Golden frame (x=3..28, y=3..28)
for y in range(3, 29):
    for x in range(3, 29):
        if x in (3, 28) or y in (3, 28):
            painting[y][x] = GOLD_DARK
        elif x in (4, 27) or y in (4, 27):
            painting[y][x] = GOLD_BRIGHT
        elif x in (5, 26) or y in (5, 26):
            painting[y][x] = GOLD_MID
        else: # Canvas inside (landscape with mysterious silhouettes)
            if y < 14: # Dusky sky
                painting[y][x] = (45, 65, 85)
            elif y < 20: # Distant misty mountains
                painting[y][x] = (30, 48, 62)
            else: # Dark ground with 2 mysterious cloaked silhouettes
                if (x in (12, 18) and 18 <= y <= 24):
                    painting[y][x] = (15, 18, 25) # Silhouettes
                else:
                    painting[y][x] = (22, 38, 30)

save_png('assets/mansion/oil_painting.png', 32, 32, painting)

# ==============================================================================
# 10. VINTAGE BED (48x64) - 1.5 x 2 tiles
# Antique carved mahogany bed, lattice headboard, teal & gold diamond quilt
# ==============================================================================
bed = [[CLR for _ in range(48)] for _ in range(64)]

# Turned corner posts: left (x=2..5), right (x=42..45)
for y in range(8, 62):
    for x in range(2, 6):
        bed[y][x] = WOOD_MID if x % 2 == 0 else WOOD_LGT
    for x in range(42, 46):
        bed[y][x] = WOOD_MID if x % 2 == 0 else WOOD_LGT

# Headboard with lattice wood pattern (y=8..24, x=6..41)
for y in range(8, 25):
    for x in range(6, 42):
        if y in (8, 9, 23, 24) or x in (6, 41):
            bed[y][x] = WOOD_OUT
        elif (x + y) % 4 == 0 or (x - y) % 4 == 0:
            bed[y][x] = WOOD_LGT # Lattice criss-cross
        else:
            bed[y][x] = (18, 28, 25) # Dark wall showing through lattice

# Fluffy white pillows at head (y=22..29, x=8..39)
for y in range(22, 30):
    for x in range(8, 40):
        if y in (22, 29) or x in (8, 39, 23, 24):
            bed[y][x] = (205, 205, 215)
        else:
            bed[y][x] = (245, 245, 250)

# Diamond quilted duvet (teal & forest green diamonds with gold seam stitching)
for y in range(30, 58):
    for x in range(6, 42):
        # Diamond grid: (x // 6 + y // 6) % 2
        d_val = ((x - 6) // 6 + (y - 30) // 6) % 2
        is_seam = ((x - 6) % 6 == 0) or ((y - 30) % 6 == 0)
        if is_seam:
            bed[y][x] = (180, 145, 55) # Gold stitching
        elif d_val == 0:
            bed[y][x] = (30, 85, 75)   # Rich teal
        else:
            bed[y][x] = (24, 70, 50)   # Forest green

# Open book resting on bed quilt (x=16..28, y=34..42)
for y in range(34, 43):
    for x in range(16, 29):
        if x == 22:
            bed[y][x] = (60, 30, 15) # Spine
        elif y in (34, 42) or x in (16, 28):
            bed[y][x] = (190, 185, 170)
        elif y % 2 == 0 and x not in (17, 21, 23, 27):
            bed[y][x] = (80, 75, 70) # Text lines
        else:
            bed[y][x] = (245, 240, 225) # Cream paper

# Footboard rail at bottom (y=57..62, x=4..43)
for y in range(57, 63):
    for x in range(4, 44):
        if y in (57, 62) or x in (4, 43):
            bed[y][x] = WOOD_OUT
        elif y == 58:
            bed[y][x] = WOOD_LGT
        else:
            bed[y][x] = WOOD_MID

save_png('assets/mansion/vintage_bed.png', 48, 64, bed)

# ==============================================================================
# 11. NIGHTSTAND WITH LAMP & KEYS (32x40) - 1x1 tile
# ==============================================================================
stand = [[CLR for _ in range(32)] for _ in range(40)]

# Nightstand wooden cabinet (y=16..38, x=6..25)
for y in range(16, 39):
    for x in range(6, 26):
        if y in (16, 17, 37, 38) or x in (6, 25):
            stand[y][x] = WOOD_OUT
        elif y in (18, 19):
            stand[y][x] = WOOD_LGT
        elif x == 15 and y == 27:
            stand[y][x] = GOLD_BRIGHT # Keyhole
        elif y in (23, 31):
            stand[y][x] = WOOD_SHD # Drawer divisions
        else:
            stand[y][x] = WOOD_MID

# Vintage Lamp with warm glowing shade (x=11..20, y=2..16)
for y in range(7, 16):
    stand[y][15] = BRASS_LGT; stand[y][16] = BRASS_MID
stand[15][13] = BRASS_MID; stand[15][18] = BRASS_MID # Base

# Warm cream/amber fabric lamp shade (y=2..8, x=10..21)
for y in range(2, 9):
    w_span = (y - 2) + 4
    for dx in range(-w_span, w_span + 1):
        sx = 15 + dx
        if 8 <= sx <= 23:
            if y == 8:
                stand[y][sx] = (255, 235, 150) # Bright rim glow
            elif y == 2 or dx in (-w_span, w_span):
                stand[y][sx] = (210, 160, 70)
            else:
                stand[y][sx] = (255, 242, 190) # Warm translucent fabric

# Antique brass skeleton key & coins on nightstand table (x=8..14, y=17..21)
stand[18][9] = BRASS_LGT; stand[18][10] = BRASS_LGT; stand[18][11] = BRASS_LGT # Key ring
stand[19][11] = BRASS_LGT; stand[20][11] = BRASS_LGT # Key shaft
stand[20][12] = BRASS_LGT # Key teeth
# Golden coins
stand[18][20] = GOLD_BRIGHT; stand[18][21] = GOLD_MID
stand[19][21] = GOLD_BRIGHT; stand[19][22] = GOLD_MID

save_png('assets/mansion/nightstand_lamp.png', 32, 40, stand)

# ==============================================================================
# 12. AMBIENT WARM LIGHT GLOW (64x64) - Radial gradient
# ==============================================================================
glow = [[CLR for _ in range(64)] for _ in range(64)]
import math
for y in range(64):
    for x in range(64):
        dist = math.sqrt((x - 31.5)**2 + (y - 31.5)**2)
        if dist < 32.0:
            alpha = int((1.0 - (dist / 32.0))**1.8 * 160)
            glow[y][x] = (255, 205, 110, alpha)

save_png('assets/mansion/light_glow_warm.png', 64, 64, glow)

# ==============================================================================
# 13. DOORWAY THRESHOLD ARCH (32x72)
# Elegant oak threshold plank with polished brass trims connecting the rooms
# ==============================================================================
thresh = [[(55, 32, 19) for _ in range(32)] for _ in range(72)]
for y in range(72):
    for x in range(32):
        if y in (0, 1, 70, 71): # Dark door jamb shadows
            thresh[y][x] = (24, 13, 8)
        elif x in (0, 31): # Brass binder bars
            thresh[y][x] = GOLD_BRIGHT
        elif x in (1, 30):
            thresh[y][x] = GOLD_DARK
        elif y % 8 == 0:
            thresh[y][x] = (38, 21, 12)
        else:
            thresh[y][x] = (65, 38, 22)

save_png('assets/mansion/doorway_threshold.png', 32, 72, thresh)

print('All 13 handcrafted pixel art assets generated successfully!')
