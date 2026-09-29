import os, zlib, struct, math

os.makedirs('assets/central_room', exist_ok=True)

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

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

# Palette
GOLD_HIGH   = (245, 215, 120)
GOLD_MID    = (190, 145, 55)
GOLD_DARK   = (115, 80, 25)
BRASS_LGT   = (230, 200, 110)
BRASS_MID   = (175, 135, 50)
BRASS_DARK  = (100, 70, 20)
MAHOG_HIGH  = (115, 72, 45)
MAHOG_MID   = (75, 42, 24)
MAHOG_DARK  = (45, 22, 12)
MAHOG_DEEP  = (25, 12, 6)
BURGUNDY_HI = (150, 40, 55)
BURGUNDY_MD = (95, 22, 35)
BURGUNDY_DK = (55, 12, 18)
TEAL_HIGH   = (38, 78, 68)
TEAL_MID    = (24, 52, 44)
TEAL_DARK   = (15, 34, 28)
TEAL_DEEP   = (10, 22, 18)
MARBLE_WHITE= (245, 245, 242)
MARBLE_VEIN = (180, 185, 188)
MARBLE_SHD  = (140, 145, 150)

# ==============================================================================
# 1. POLISHED DARK PARQUET WOOD FLOOR (32x32) - Identical to Victorian Room
# ==============================================================================
floor = [[MAHOG_MID for _ in range(32)] for _ in range(32)]
for y in range(32):
    plank_row = y // 8
    py = y % 8
    for x in range(32):
        x_shift = (plank_row % 2) * 16
        px = (x + x_shift) % 32
        if py == 7:
            floor[y][x] = MAHOG_DEEP
        elif py == 0:
            floor[y][x] = MAHOG_HIGH
        elif px == 31:
            floor[y][x] = MAHOG_DEEP
        elif px == 0:
            floor[y][x] = (85, 50, 30)
        else:
            grain = (x * 7 + y * 13) % 9
            if grain in (0, 1):
                floor[y][x] = (80, 48, 28)
            elif grain in (4, 5):
                floor[y][x] = (65, 36, 20)
            elif grain == 8:
                floor[y][x] = (92, 56, 34)
            else:
                floor[y][x] = MAHOG_MID

save_png('assets/central_room/wood_floor.png', 32, 32, floor)

# ==============================================================================
# 2. VICTORIAN LOBBY WALL (32x48) - Royal Burgundy Damask & Relief Boiserie
# ==============================================================================
wall = [[CLR for _ in range(32)] for _ in range(48)]
for y in range(48):
    for x in range(32):
        if y == 0:
            wall[y][x] = (70, 35, 45) # Ceiling molding highlight
        elif y in (1, 2):
            wall[y][x] = (45, 18, 26) # Crown molding
        elif y == 3:
            wall[y][x] = (22, 8, 12)  # Undercut shadow
        elif y < 22:
            # Royal Burgundy Wallpaper with 3D embossed gold pinstripes & damask crests
            is_stripe = (x % 8 in (0, 1))
            is_damask = ((x % 8 == 4) and (y % 8 in (1, 2, 3))) or ((x + y) % 6 == 0 and y % 4 == 0)
            if is_stripe:
                wall[y][x] = (115, 32, 45) if x % 8 == 0 else (90, 24, 35)
            elif is_damask:
                wall[y][x] = GOLD_MID if (x + y) % 2 == 0 else (135, 42, 56)
            else:
                wall[y][x] = BURGUNDY_MD
        elif y == 22:
            wall[y][x] = (125, 80, 50) # Chair rail top bevel highlight
        elif y in (23, 24):
            wall[y][x] = (82, 46, 26)
        elif y == 25:
            wall[y][x] = (32, 16, 8)   # Chair rail deep shadow
        elif y < 44:
            # Wainscoting panels with 3D relief
            in_panel_x = (3 <= x <= 13) or (19 <= x <= 29)
            in_panel_y = (28 <= y <= 41)
            if in_panel_x and in_panel_y:
                if y == 28 or x in (3, 19):
                    wall[y][x] = (24, 12, 6) # Top/left groove shadow
                elif y == 41 or x in (13, 29):
                    wall[y][x] = (95, 58, 34) # Bottom/right highlight
                else:
                    wall[y][x] = (62, 34, 19) if (x * y) % 5 != 0 else (70, 40, 23)
            else:
                if x in (0, 16):
                    wall[y][x] = (42, 22, 12)
                elif x in (1, 17):
                    wall[y][x] = (85, 48, 28)
                else:
                    wall[y][x] = (54, 30, 16)
        elif y in (44, 45):
            wall[y][x] = (78, 44, 25) if y == 44 else (42, 22, 12)
        else:
            wall[y][x] = (20, 10, 5)

save_png('assets/central_room/wall_lobby.png', 32, 48, wall)

# ==============================================================================
# 3. GRAND LOBBY FOYER RUG (160x128) - Crimson Velvet with Emerald & Gold Medallion
# ==============================================================================
rug = [[CLR for _ in range(160)] for _ in range(128)]
for y in range(128):
    for x in range(160):
        # Soft outer contact shadow onto parquet
        if y < 2 or y > 125 or x < 2 or x > 157:
            d_edge = min(y, 127 - y, x, 159 - x)
            if d_edge == 1:
                rug[y][x] = (15, 10, 8, 80)
            elif d_edge == 0:
                rug[y][x] = (15, 10, 8, 40)
            continue
        
        # Golden Tassels on ends (y=2..4 and 123..125)
        if y in (2, 125):
            rug[y][x] = (235, 210, 150, 255) if x % 3 != 0 else (120, 95, 50, 200)
        elif y in (3, 124):
            rug[y][x] = (180, 145, 85, 255) if x % 3 != 0 else (80, 60, 30, 255)
        elif y in (4, 123):
            rug[y][x] = (50, 30, 15, 255)
        elif y in (5, 122) or x in (3, 156):
            rug[y][x] = GOLD_DARK
        elif y in (6, 121) or x in (4, 155):
            rug[y][x] = GOLD_HIGH
        elif y in (7, 120) or x in (5, 154):
            rug[y][x] = GOLD_MID
        elif y < 19 or y > 108 or x < 17 or x > 142:
            # Emerald border band with gold scrollwork
            bd = min(y - 7, 120 - y, x - 5, 154 - x)
            if bd in (1, 9):
                rug[y][x] = TEAL_DEEP
            elif bd in (2, 8):
                rug[y][x] = GOLD_MID if (x + y) % 4 == 0 else TEAL_MID
            elif bd in (4, 5, 6):
                if (x % 8 in (2, 3) and y % 8 in (2, 3)) or ((x + y) % 6 == 0):
                    rug[y][x] = GOLD_HIGH if (x + y) % 2 == 0 else GOLD_MID
                else:
                    rug[y][x] = TEAL_MID if (x * y) % 3 != 0 else TEAL_HIGH
            else:
                rug[y][x] = TEAL_MID
        elif y in (19, 108) or x in (17, 142):
            rug[y][x] = GOLD_HIGH
        elif y in (20, 107) or x in (18, 141):
            rug[y][x] = GOLD_DARK
        elif y in (21, 106) or x in (19, 140):
            rug[y][x] = BURGUNDY_DK
        else:
            # Rich Crimson Velvet Center Field with Baroque Medallion
            dx = abs(x - 80)
            dy = abs(y - 64)
            dist_med = (dx / 40.0)**2 + (dy / 26.0)**2
            if dist_med < 0.15:
                rug[y][x] = GOLD_HIGH if (dx <= 3 or dy <= 3) else TEAL_HIGH
            elif dist_med < 0.35:
                rug[y][x] = TEAL_MID if (x + y) % 3 != 0 else GOLD_MID
            elif dist_med < 0.65:
                rug[y][x] = GOLD_HIGH if (x + y) % 5 == 0 or (x - y) % 5 == 0 else BURGUNDY_HI
            elif dist_med < 0.95:
                rug[y][x] = GOLD_HIGH if (x * y) % 2 == 0 else GOLD_MID
            elif dist_med < 1.08:
                rug[y][x] = BURGUNDY_DK
            else:
                if (x + y) % 10 in (0, 1) or (x - y) % 10 in (0, 1):
                    rug[y][x] = BURGUNDY_HI
                else:
                    grain = (x * 11 + y * 17) % 7
                    rug[y][x] = (110, 26, 40) if grain == 0 else BURGUNDY_MD

save_png('assets/central_room/lobby_rug.png', 160, 128, rug)

# ==============================================================================
# 4. GRANDFATHER CLOCK (32x64) - Swan-Neck Pediment, Pendulum & Weights
# ==============================================================================
clock = [[CLR for _ in range(32)] for _ in range(64)]

# Floor contact shadow (rows 61..63)
for x in range(6, 26):
    clock[61][x] = (12, 6, 3, 150)
    clock[62][x] = (8, 4, 2, 90)
    clock[63][x] = (5, 2, 1, 40)

# Top Swan-Neck Arch Pediment with Brass Finials (rows 2..9, x=7..24)
clock[2][15] = GOLD_HIGH; clock[2][16] = GOLD_MID # Center brass finial
clock[3][15] = GOLD_HIGH; clock[3][16] = GOLD_MID
for y in range(4, 9):
    for x in range(8, 24):
        dx = abs(x - 15.5)
        if y == 4 and dx > 4:
            clock[y][x] = GOLD_HIGH if x in (8, 23) else MAHOG_HIGH # Side finials
        elif y == 5 and dx > 3:
            clock[y][x] = MAHOG_HIGH
        else:
            clock[y][x] = MAHOG_MID

# Clock Hood & Enamel Dial (rows 9..22, x=7..24)
for y in range(9, 23):
    for x in range(7, 25):
        if x in (7, 24) or y in (9, 22):
            clock[y][x] = MAHOG_HIGH if (x == 7 or y == 9) else MAHOG_DEEP
        else:
            # White Enamel Clock Dial in Brass Bezel
            dx = abs(x - 15.5)
            dy = abs(y - 15.5)
            dist_c = math.sqrt(dx**2 + dy**2)
            if dist_c > 5.5:
                clock[y][x] = GOLD_MID # Brass bezel ring
            elif dist_c > 4.5:
                clock[y][x] = GOLD_HIGH
            elif (x in (15, 16) and 12 <= y <= 16) or (y == 15 and 15 <= x <= 18):
                clock[y][x] = (25, 25, 25) # Black clock hands
            elif dist_c > 3.5 and (x * y) % 3 == 0:
                clock[y][x] = (60, 60, 60) # Roman numeral hour marks
            else:
                clock[y][x] = (248, 246, 238) # Ivory dial face

# Middle Waist / Trunk with Glass Door (rows 23..48, x=9..22)
for y in range(23, 49):
    for x in range(9, 23):
        if x in (9, 22) or y in (23, 48):
            clock[y][x] = MAHOG_HIGH if (x == 9 or y == 23) else MAHOG_DEEP
        elif x in (10, 21) or y in (24, 47):
            clock[y][x] = GOLD_MID # Inner brass door frame
        else:
            # Glass interior with swinging brass pendulum & twin cylindrical weights
            # Dark shadowed mahogany back
            bg_col = (20, 10, 5)
            # Twin brass weights hanging on chains (y=26..38)
            is_chain = (x in (13, 18) and 25 <= y <= 30)
            is_left_weight = (x in (12, 13) and 31 <= y <= 39)
            is_right_weight = (x in (17, 18) and 28 <= y <= 36)
            # Large circular brass pendulum bob (y=39..46, x=14..17)
            dist_pend = math.sqrt((x - 15.5)**2 + (y - 42.5)**2)
            if dist_pend <= 2.8:
                clock[y][x] = (255, 235, 140) if x == 15 else GOLD_MID
            elif is_left_weight or is_right_weight:
                clock[y][x] = GOLD_HIGH if (x in (12, 17)) else GOLD_MID
            elif is_chain:
                clock[y][x] = GOLD_HIGH if y % 2 == 0 else GOLD_DARK
            else:
                # Glass reflection shine (diagonal 1px streak)
                if (x + y) in (36, 48):
                    clock[y][x] = (70, 95, 110) # Glass reflection
                else:
                    clock[y][x] = bg_col

# Lower Base / Plinth with Raised Panel (rows 49..61, x=7..24)
for y in range(49, 62):
    for x in range(7, 25):
        if y in (49, 60, 61) or x in (7, 24):
            clock[y][x] = MAHOG_HIGH if (x == 7 or y == 49) else MAHOG_DEEP
        elif (10 <= x <= 21) and (52 <= y <= 58):
            if y == 52 or x == 10:
                clock[y][x] = MAHOG_DEEP # Inset panel groove
            elif y == 58 or x == 21:
                clock[y][x] = MAHOG_HIGH
            else:
                clock[y][x] = (80, 45, 25) # Raised panel face
        else:
            clock[y][x] = MAHOG_MID

save_png('assets/central_room/grandfather_clock.png', 32, 64, clock)

# ==============================================================================
# 5. HALL CONSOLE TABLE WITH GILDED MIRROR & FLOWERS (64x48)
# ==============================================================================
console = [[CLR for _ in range(64)] for _ in range(48)]

# Floor contact shadow under carved table legs (rows 45..47)
for x in (8, 9, 10, 53, 54, 55):
    console[45][x] = (12, 6, 3, 140)
    console[46][x] = (8, 4, 2, 80)
    console[47][x] = (5, 2, 1, 40)

# Large Baroque Gilded Mirror (rows 2..24, x=16..47)
for y in range(2, 25):
    for x in range(16, 48):
        dx = abs(x - 31.5)
        # Arched top of mirror
        arch_limit = 2 + int((dx / 15.0)**2 * 5)
        if y < arch_limit:
            continue
        # Heavy gilded frame
        is_frame = (y < arch_limit + 3 or y > 21 or dx > 13)
        if is_frame:
            if y == arch_limit or x in (16, 17):
                console[y][x] = GOLD_HIGH
            elif (x + y) % 3 == 0:
                console[y][x] = GOLD_HIGH
            else:
                console[y][x] = GOLD_MID
        else:
            # Polished silvered glass with chandelier reflection
            if (x + y) in (32, 44):
                console[y][x] = (255, 255, 255) # Bright specular reflection gleam
            elif y < 14 and abs(x - 31.5) < 6:
                console[y][x] = (255, 230, 160) # Reflected warm glow
            else:
                console[y][x] = (160, 185, 200) if (x + y) % 4 == 0 else (140, 165, 180)

# Tabletop Marble Slab (rows 24..30, x=6..57)
for y in range(24, 31):
    for x in range(6, 58):
        if y == 24:
            console[y][x] = (255, 255, 255) # White marble front bevel highlight
        elif y in (25, 26, 27):
            # Polished Italian White Carrara Marble with grey veins
            if (x + y * 2) % 17 == 0 or (x - y * 3) % 23 == 0:
                console[y][x] = MARBLE_VEIN # Marble vein
            else:
                console[y][x] = MARBLE_WHITE
        elif y == 28:
            console[y][x] = MARBLE_SHD # Marble edge shadow
        else:
            console[y][x] = MAHOG_DEEP # Table apron shadow

# Objects on Tabletop:
# Silver Candelabra on Left (x=11..17, y=14..25)
# 3 lit candles with flames
for cx in (12, 14, 16):
    console[14][cx] = (255, 220, 100) # Flame tip
    console[15][cx] = (255, 140, 30)  # Flame core
    console[16][cx] = (245, 240, 230) # Candle wax
    console[17][cx] = (235, 230, 220)
# Silver branched arms & stem
console[18][12] = (200, 205, 210); console[18][14] = (220, 225, 230); console[18][16] = (200, 205, 210)
console[19][13] = (220, 225, 230); console[19][14] = (240, 245, 250); console[19][15] = (220, 225, 230)
for sy in range(20, 25):
    console[sy][14] = (240, 245, 250)
console[24][13] = (190, 195, 200); console[24][14] = (230, 235, 240); console[24][15] = (190, 195, 200)

# Crystal Vase with Crimson Roses in Center (x=28..35, y=16..25)
# Red Roses (y=16..20, x=29..34)
for ry in range(16, 21):
    for rx in range(29, 35):
        if (rx + ry) % 2 == 0:
            console[ry][rx] = BURGUNDY_HI
        else:
            console[ry][rx] = (180, 25, 45)
# Green foliage leaves
console[19][28] = (35, 95, 45); console[19][35] = (35, 95, 45)
# Translucent crystal vase (y=21..25, x=30..33)
for vy in range(21, 26):
    for vx in range(30, 34):
        if vx in (30, 33) or vy == 25:
            console[vy][vx] = (210, 235, 245)
        else:
            console[vy][vx] = (140, 185, 205)

# Silver Calling Card Tray on Right (x=46..51, y=24..26)
for sx in range(46, 52):
    console[25][sx] = (230, 235, 240)
    console[26][sx] = (160, 165, 170)

# Table Apron & Carved Mahogany Cabriole Legs (rows 29..45)
for y in range(29, 34):
    for x in range(7, 57):
        if (x in (31, 32)):
            console[y][x] = GOLD_MID # Center carved shell ornament
        else:
            console[y][x] = MAHOG_MID

# Graceful Carved Cabriole Legs (x=8..12 and x=51..55, rows 33..45)
for y in range(33, 46):
    # Left Leg
    console[y][8] = MAHOG_DEEP; console[y][9] = MAHOG_HIGH; console[y][10] = MAHOG_MID
    # Right Leg
    console[y][53] = MAHOG_DEEP; console[y][54] = MAHOG_HIGH; console[y][55] = MAHOG_MID

save_png('assets/central_room/hall_console_table.png', 64, 48, console)

# ==============================================================================
# 6. BENTWOOD COAT & HAT RACK WITH UMBRELLA STAND (32x56)
# ==============================================================================
rack = [[CLR for _ in range(32)] for _ in range(56)]

# Contact shadow (rows 53..55, x=9..22)
for x in range(9, 23):
    rack[53][x] = (12, 6, 3, 140)
    rack[54][x] = (8, 4, 2, 80)
    rack[55][x] = (4, 2, 1, 30)

# Bentwood Central Pole (rows 4..53, x=15..16)
for y in range(4, 53):
    rack[y][15] = MAHOG_HIGH; rack[y][16] = MAHOG_DEEP

# Top Curved Brass Pegs & Finial (rows 2..10, x=8..23)
rack[2][15] = GOLD_HIGH; rack[2][16] = GOLD_MID # Top finial
# Curved pegs left & right
rack[4][10] = GOLD_HIGH; rack[5][11] = GOLD_HIGH; rack[6][12] = GOLD_MID
rack[4][21] = GOLD_HIGH; rack[5][20] = GOLD_HIGH; rack[6][19] = GOLD_MID

# Hanging Silk Top Hat on Left Peg (x=7..13, y=5..12)
for hy in range(5, 13):
    for hx in range(7, 14):
        if hy == 12: # Hat brim
            rack[hy][hx] = (18, 18, 22) if hx in (7, 13) else (35, 35, 42)
        elif hy == 11: # Hat band in burgundy silk
            rack[hy][hx] = BURGUNDY_HI
        else: # Crown of top hat
            if hx in (8, 9):
                rack[hy][hx] = (50, 50, 60) # Top hat sheen
            else:
                rack[hy][hx] = (22, 22, 26)

# Hanging Wool Overcoat on Right (x=16..24, y=10..32)
for cy in range(10, 33):
    w_coat = 3 + int((cy - 10) * 0.2)
    for cx in range(16, 16 + w_coat):
        if cx == 17:
            rack[cy][cx] = (55, 48, 44) # Wool fold highlight
        elif cx == 16 + w_coat - 1 or cy == 32:
            rack[cy][cx] = (20, 16, 14) # Fold shadow
        else:
            rack[cy][cx] = (38, 32, 28) # Dark charcoal/brown wool

# Oval Center Mirror in Pole (rows 16..26, x=13..18)
for my in range(16, 27):
    for mx in range(13, 19):
        if mx in (13, 18) or my in (16, 26):
            rack[my][mx] = BRASS_MID
        else:
            rack[my][mx] = (210, 230, 240) if (mx + my) % 2 == 0 else (170, 195, 210)

# Lower Umbrella Stand Hoop & Drip Pan (rows 35..53, x=9..22)
# Brass circular retaining ring (rows 36..38, x=9..22)
for x in range(9, 23):
    rack[36][x] = BRASS_LGT if x % 2 == 0 else BRASS_MID
    rack[37][x] = BRASS_MID
    rack[38][x] = BRASS_DARK

# Standing Umbrellas with Curved Wood Handles (x=10..13 and x=18..21, rows 27..50)
# Curved chestnut handle
rack[27][11] = MAHOG_HIGH; rack[27][12] = MAHOG_HIGH
rack[28][10] = MAHOG_HIGH; rack[29][10] = MAHOG_MID; rack[30][11] = MAHOG_HIGH
for uy in range(31, 51):
    rack[uy][12] = (15, 38, 28) # Folded dark green silk umbrella body
    rack[uy][19] = (25, 12, 18) # Folded dark wine umbrella body

# Bottom Drip Pan (rows 49..53, x=8..23)
for y in range(50, 54):
    for x in range(8, 24):
        if y == 50:
            rack[y][x] = BRASS_LGT
        elif y == 53 or x in (8, 23):
            rack[y][x] = BRASS_DARK
        else:
            rack[y][x] = BRASS_MID

save_png('assets/central_room/coat_rack.png', 32, 56, rack)

# ==============================================================================
# 7. VICTORIAN LOBBY DOUBLE SETTEE / SOFA (64x36) - Rich Tufted Wine Velvet
# ==============================================================================
settee = [[CLR for _ in range(64)] for _ in range(36)]

# Floor contact shadow under legs (rows 33..35)
for x in (5, 6, 7, 31, 32, 56, 57, 58):
    settee[33][x] = (12, 6, 3, 140)
    settee[34][x] = (8, 4, 2, 80)
    settee[35][x] = (4, 2, 1, 40)

# Curved Mahogany Backrest Top Crest (rows 2..6, x=4..59)
for y in range(2, 7):
    for x in range(4, 60):
        # Two rounded back lobes
        dx1 = abs(x - 18.5)
        dx2 = abs(x - 45.5)
        lobe_d = min(dx1, dx2)
        if y == 2 and lobe_d < 6:
            settee[y][x] = GOLD_HIGH if (x in (18, 19, 45, 46)) else MAHOG_HIGH
        elif y in (3, 4):
            settee[y][x] = MAHOG_MID
        elif y in (5, 6):
            settee[y][x] = MAHOG_DEEP

# Tufted Wine-Red Velvet Double Backrest (rows 6..16, x=5..58)
for y in range(6, 17):
    for x in range(5, 59):
        is_button = (x in (12, 18, 24, 39, 45, 51) and y in (9, 13))
        is_crease = ((x + y) % 4 == 0)
        if is_button:
            settee[y][x] = (35, 8, 14) # Tuft depression
        elif is_crease:
            settee[y][x] = BURGUNDY_DK
        elif (x + y) % 5 == 0:
            settee[y][x] = BURGUNDY_HI
        else:
            settee[y][x] = BURGUNDY_MD

# Padded Rolled Armrests (rows 10..27, Left x=3..8, Right x=55..60)
for y in range(10, 28):
    for x in range(3, 9):
        if x == 3: settee[y][x] = BURGUNDY_DK
        elif x == 5: settee[y][x] = BURGUNDY_HI
        else: settee[y][x] = BURGUNDY_MD
    for x in range(55, 61):
        if x == 60: settee[y][x] = BURGUNDY_DK
        elif x == 58: settee[y][x] = (120, 28, 42)
        else: settee[y][x] = BURGUNDY_MD

# Front Scroll Mahogany Arm Caps (rows 25..27)
for x in (4, 5, 6, 7): settee[26][x] = MAHOG_HIGH; settee[27][x] = MAHOG_MID
for x in (56, 57, 58, 59): settee[26][x] = MAHOG_HIGH; settee[27][x] = MAHOG_MID

# Plump Double Seat Cushion (rows 16..27, x=9..54)
for y in range(16, 28):
    for x in range(9, 55):
        if y == 16:
            settee[y][x] = (25, 6, 10)
        elif y == 27:
            settee[y][x] = BURGUNDY_HI if (13 <= x <= 25 or 38 <= x <= 50) else BURGUNDY_MD
        elif (x in (31, 32)):
            settee[y][x] = BURGUNDY_DK # Center cushion seam
        elif (x + y) % 6 == 0:
            settee[y][x] = BURGUNDY_HI
        else:
            settee[y][x] = BURGUNDY_MD

# Front Apron & 4 Carved Legs (rows 28..34)
for y in range(28, 31):
    for x in range(6, 58):
        if y == 28:
            settee[y][x] = MAHOG_HIGH
        elif x in (18, 31, 45):
            settee[y][x] = GOLD_MID # Carved gold ornaments
        else:
            settee[y][x] = MAHOG_MID

# Legs (Left, Middle, Right)
for y in range(30, 35):
    for lx in (5, 31, 56):
        settee[y][lx] = MAHOG_DEEP; settee[y][lx + 1] = MAHOG_HIGH; settee[y][lx + 2] = MAHOG_MID

save_png('assets/central_room/lobby_settee.png', 64, 36, settee)

# ==============================================================================
# 8. CLASSICAL MARBLE BUST ON CARVED PEDESTAL (32x48)
# ==============================================================================
bust = [[CLR for _ in range(32)] for _ in range(48)]

# Floor contact shadow (rows 45..47)
for x in range(7, 25):
    bust[45][x] = (12, 6, 3, 140)
    bust[46][x] = (8, 4, 2, 80)
    bust[47][x] = (4, 2, 1, 30)

# Sculpted White Marble Bust (rows 2..20, x=9..22)
# Marble Head & Classical Hair Curls (rows 2..11, x=11..20)
for y in range(2, 12):
    for x in range(11, 21):
        dx = abs(x - 15.5)
        if y <= 5: # Hair curls
            bust[y][x] = MARBLE_WHITE if (x + y) % 2 == 0 else (210, 215, 220)
        elif y in (6, 7): # Forehead & eyes
            if y == 7 and x in (13, 17):
                bust[y][x] = (130, 135, 140) # Eye recesses
            elif x in (15, 16):
                bust[y][x] = (255, 255, 255) # Nose bridge highlight
            else:
                bust[y][x] = MARBLE_WHITE if x < 16 else (225, 230, 235)
        elif y == 8: # Nose tip & cheeks
            bust[y][x] = (255, 255, 255) if x in (15, 16) else (220, 225, 230)
        elif y in (9, 10): # Lips & chin
            bust[y][x] = (170, 175, 180) if y == 9 and x in (15, 16) else MARBLE_WHITE
        else: # Neck
            bust[y][x] = (180, 185, 190)

# Classical Draped Toga Shoulders & Chest (rows 12..20, x=9..22)
for y in range(12, 21):
    w_toga = 4 + int((y - 12) * 0.4)
    for x in range(15 - w_toga, 16 + w_toga):
        if (x + y) % 3 == 0:
            bust[y][x] = (255, 255, 255) # Toga fold highlight
        elif (x - y) % 4 == 0:
            bust[y][x] = (160, 165, 172) # Fold shadow
        else:
            bust[y][x] = (225, 230, 235)

# Small Marble Socle/Pedestal Base (rows 20..22, x=13..18)
for y in range(20, 23):
    for x in range(13, 19):
        bust[y][x] = (255, 255, 255) if y == 20 else (175, 180, 185)

# Fluted Mahogany Pedestal Column (rows 23..45, x=8..23)
# Column Capital (rows 23..26, x=7..24)
for y in range(23, 27):
    for x in range(7, 25):
        if y == 23: bust[y][x] = (135, 88, 55) # Top ledge highlight
        elif y == 26: bust[y][x] = MAHOG_DEEP
        else: bust[y][x] = MAHOG_MID

# Fluted Column Shaft (rows 27..40, x=9..22)
for y in range(27, 41):
    for x in range(9, 23):
        # Vertical fluting channels (shadow, highlight, body)
        flute = (x - 9) % 3
        if x in (9, 10):
            bust[y][x] = MAHOG_HIGH # Left side highlight
        elif x in (21, 22):
            bust[y][x] = MAHOG_DEEP # Right side shadow
        elif flute == 0:
            bust[y][x] = (40, 20, 10) # Flute groove shadow
        elif flute == 1:
            bust[y][x] = (95, 55, 32) # Flute ridge highlight
        else:
            bust[y][x] = MAHOG_MID

# Column Base Plinth (rows 41..45, x=7..24)
for y in range(41, 46):
    for x in range(7, 25):
        if y == 41: bust[y][x] = MAHOG_HIGH
        elif y == 45: bust[y][x] = MAHOG_DEEP
        else: bust[y][x] = MAHOG_MID

save_png('assets/central_room/statue_pedestal.png', 32, 48, bust)

print('All 8 Central Room Lobby assets generated successfully!')
