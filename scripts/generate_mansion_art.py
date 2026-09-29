import os, zlib, struct, math

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

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def blend(c1, c2, factor):
    """Linearly blend two colors."""
    f = max(0.0, min(1.0, factor))
    return (
        clamp(c1[0] * (1.0 - f) + c2[0] * f),
        clamp(c1[1] * (1.0 - f) + c2[1] * f),
        clamp(c1[2] * (1.0 - f) + c2[2] * f),
        c1[3] if len(c1) == 4 else 255
    )

# Common Palette Constants
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
BURGUNDY_HI = (145, 38, 55)
BURGUNDY_MD = (95, 22, 35)
BURGUNDY_DK = (55, 12, 18)
TEAL_HIGH   = (38, 78, 68)
TEAL_MID    = (24, 52, 44)
TEAL_DARK   = (15, 34, 28)
TEAL_DEEP   = (10, 22, 18)
SHADOW_SOFT = (10, 6, 4, 110)
SHADOW_HARD = (6, 4, 2, 170)

# ==============================================================================
# 1. POLISHED DARK PARQUET FLOOR (32x32) - True Interlocking Planks & Bevel Depth
# ==============================================================================
floor = [[MAHOG_MID for _ in range(32)] for _ in range(32)]
for y in range(32):
    plank_row = y // 8
    py = y % 8
    for x in range(32):
        # Staggered vertical joints every 16 px, offset by row
        x_shift = (plank_row % 2) * 16
        px = (x + x_shift) % 32
        
        # Horizontal bevel joint (bottom of plank)
        if py == 7:
            floor[y][x] = MAHOG_DEEP
        elif py == 0:
            # Top highlight catch on beveled wood edge
            floor[y][x] = MAHOG_HIGH
        # Vertical joint between planks
        elif px == 31:
            floor[y][x] = MAHOG_DEEP
        elif px == 0:
            floor[y][x] = (85, 50, 30)
        else:
            # Rich natural grain variations
            grain = (x * 7 + y * 13) % 9
            if grain in (0, 1):
                floor[y][x] = (80, 48, 28)
            elif grain in (4, 5):
                floor[y][x] = (65, 36, 20)
            elif grain == 8:
                floor[y][x] = (92, 56, 34)
            else:
                floor[y][x] = MAHOG_MID

save_png('assets/mansion/wood_floor.png', 32, 32, floor)

# ==============================================================================
# 2. GRAND ORNATE VICTORIAN RUG (160x128) - Multi-Layered Relief & Drop Shadow
# ==============================================================================
rug = [[CLR for _ in range(160)] for _ in range(128)]

for y in range(128):
    for x in range(160):
        # Outer soft contact drop shadow onto parquet floor (2-3px radius)
        if y < 2 or y > 125 or x < 2 or x > 157:
            # Outer shadow blur
            d_edge = min(y, 127 - y, x, 159 - x)
            if d_edge == 1:
                rug[y][x] = (15, 10, 8, 80)
            elif d_edge == 0:
                rug[y][x] = (15, 10, 8, 40)
            continue
        
        # Tassels / Fringe along top and bottom (y in 2..4 and 123..125)
        if y in (2, 125):
            rug[y][x] = (235, 210, 150, 255) if x % 3 != 0 else (120, 95, 50, 200)
        elif y in (3, 124):
            rug[y][x] = (180, 145, 85, 255) if x % 3 != 0 else (80, 60, 30, 255)
        elif y in (4, 123):
            rug[y][x] = (50, 30, 15, 255) # Dark binding stitch
        # Outer Gold Piping Frame
        elif y in (5, 122) or x in (3, 156):
            rug[y][x] = GOLD_DARK
        elif y in (6, 121) or x in (4, 155):
            rug[y][x] = GOLD_HIGH
        elif y in (7, 120) or x in (5, 154):
            rug[y][x] = GOLD_MID
        # Wide Burgundy Velvet Border with Gold Filigree (rows 8..18, cols 6..16 & symmetric)
        elif y < 19 or y > 108 or x < 17 or x > 142:
            # Determine border layer
            bd = min(y - 7, 120 - y, x - 5, 154 - x)
            if bd in (1, 9):
                rug[y][x] = BURGUNDY_DK
            elif bd in (2, 8):
                rug[y][x] = GOLD_MID if (x + y) % 4 == 0 else BURGUNDY_MD
            elif bd in (4, 5, 6):
                # Baroque gold scroll weave
                if (x % 8 in (2, 3) and y % 8 in (2, 3)) or ((x + y) % 6 == 0):
                    rug[y][x] = GOLD_HIGH if (x + y) % 2 == 0 else GOLD_MID
                else:
                    rug[y][x] = BURGUNDY_MD if (x * y) % 3 != 0 else BURGUNDY_HI
            else:
                rug[y][x] = BURGUNDY_MD
        # Inner Gold Border Frame with shadow
        elif y in (19, 108) or x in (17, 142):
            rug[y][x] = GOLD_HIGH
        elif y in (20, 107) or x in (18, 141):
            rug[y][x] = GOLD_DARK
        elif y in (21, 106) or x in (19, 140):
            rug[y][x] = TEAL_DEEP # Inner shadow drop
        else:
            # Main Inner Field: Deep Emerald Velvet
            dx = abs(x - 80)
            dy = abs(y - 64)
            # Center baroque medallion (ellipse roughly 44x30)
            dist_med = (dx / 38.0)**2 + (dy / 25.0)**2
            if dist_med < 0.15:
                # Medallion inner core: gold star crest
                rug[y][x] = GOLD_HIGH if (dx <= 3 or dy <= 3) else BURGUNDY_HI
            elif dist_med < 0.35:
                # Ruby velvet inner ring
                rug[y][x] = BURGUNDY_MD if (x + y) % 3 != 0 else GOLD_MID
            elif dist_med < 0.65:
                # Emerald transition with gold filigree rays
                if (x + y) % 5 == 0 or (x - y) % 5 == 0:
                    rug[y][x] = GOLD_HIGH
                else:
                    rug[y][x] = TEAL_MID
            elif dist_med < 0.95:
                # Heavy gold baroque outer wreath
                rug[y][x] = GOLD_HIGH if (x * y) % 2 == 0 else GOLD_MID
            elif dist_med < 1.08:
                rug[y][x] = TEAL_DEEP # Outer drop shadow of medallion
            else:
                # 4 Ornate corner brackets (top-left, top-right, etc.)
                cx = min(x - 21, 139 - x)
                cy = min(y - 21, 105 - y)
                if cx + cy < 24:
                    if (cx + cy) in (8, 16, 22):
                        rug[y][x] = GOLD_HIGH
                    elif (cx + cy) in (9, 17):
                        rug[y][x] = GOLD_MID
                    elif (cx * cy) % 4 == 0:
                        rug[y][x] = BURGUNDY_MD
                    else:
                        rug[y][x] = TEAL_MID
                else:
                    # Luxurious emerald velvet field with subtle diamond damask quilting
                    if (x + y) % 10 in (0, 1) or (x - y) % 10 in (0, 1):
                        rug[y][x] = (30, 64, 54) # Subtle damask diamond sheen
                    else:
                        grain = (x * 11 + y * 17) % 7
                        if grain == 0:
                            rug[y][x] = (16, 38, 31)
                        elif grain == 3:
                            rug[y][x] = (26, 56, 48)
                        else:
                            rug[y][x] = TEAL_MID

save_png('assets/mansion/victorian_rug.png', 160, 128, rug)

# Carpet center & border tiles for compatibility
carpet_center = [[TEAL_MID for _ in range(32)] for _ in range(32)]
for y in range(32):
    for x in range(32):
        if (x + y) % 8 == 0:
            carpet_center[y][x] = (32, 68, 58)
        elif (x * 7 + y * 11) % 5 == 0:
            carpet_center[y][x] = (18, 42, 34)
save_png('assets/mansion/carpet_center.png', 32, 32, carpet_center)

carpet_border = [row[:] for row in carpet_center]
for y in range(4):
    for x in range(32):
        carpet_border[y][x] = GOLD_HIGH if (x + y) % 2 == 0 else GOLD_MID
save_png('assets/mansion/carpet_border_top.png', 32, 32, carpet_border)

# ==============================================================================
# 3. VICTORIAN WALL (32x48) - 3D Crown Cornice, Damask Wallpaper & Relief Boiserie
# ==============================================================================
wall = [[CLR for _ in range(32)] for _ in range(48)]

for y in range(48):
    for x in range(32):
        if y == 0:
            wall[y][x] = (55, 90, 80) # Ceiling junction highlight
        elif y in (1, 2):
            wall[y][x] = (35, 65, 56) # Crown molding top face
        elif y == 3:
            wall[y][x] = (18, 36, 30) # Crown molding undercut shadow
        elif y < 22:
            # Damask Teal Wallpaper with 3D embossed vertical pinstripes & fleur-de-lis
            is_stripe = (x % 8 in (0, 1))
            is_damask = ((x % 8 == 4) and (y % 8 in (1, 2, 3))) or ((x + y) % 6 == 0 and y % 4 == 0)
            if is_stripe:
                wall[y][x] = (34, 70, 60) if x % 8 == 0 else (28, 58, 50)
            elif is_damask:
                wall[y][x] = (36, 74, 64) # Highlighted damask motif
            else:
                wall[y][x] = (22, 46, 39)
        elif y == 22: # Chair rail top bevel highlight
            wall[y][x] = (125, 80, 50)
        elif y in (23, 24): # Chair rail body
            wall[y][x] = (82, 46, 26)
        elif y == 25: # Chair rail deep drop shadow below
            wall[y][x] = (32, 16, 8)
        elif y < 44:
            # Wainscoting (Boiserie) Panels with 3D Inset Bevels
            # Stile / Rail frame around panels: panel is x=3..13 and x=19..29
            in_panel_x = (3 <= x <= 13) or (19 <= x <= 29)
            in_panel_y = (28 <= y <= 41)
            if in_panel_x and in_panel_y:
                # 3D Inset molding: Light from top-left
                if y == 28 or x in (3, 19):
                    wall[y][x] = (24, 12, 6) # Top & Left inner groove (shadow)
                elif y == 41 or x in (13, 29):
                    wall[y][x] = (95, 58, 34) # Bottom & Right inner edge (highlight)
                else:
                    # Raised inner wood panel
                    wall[y][x] = (62, 34, 19) if (x * y) % 5 != 0 else (70, 40, 23)
            else:
                # Outer stile / rail frame
                if x in (0, 16):
                    wall[y][x] = (42, 22, 12) # Vertical stile seam
                elif x in (1, 17):
                    wall[y][x] = (85, 48, 28) # Vertical stile highlight
                else:
                    wall[y][x] = (54, 30, 16)
        elif y in (44, 45): # Heavy carved baseboard molding
            wall[y][x] = (78, 44, 25) if y == 44 else (42, 22, 12)
        else: # Floor contact shadow
            wall[y][x] = (20, 10, 5)

save_png('assets/mansion/wall_victorian.png', 32, 48, wall)

# ==============================================================================
# 4. CHIMENEA / FIREPLACE (64x48) - Deep 3D Cavern Hearth, Fire & Mantel Objects
# ==============================================================================
fp = [[CLR for _ in range(64)] for _ in range(48)]

# Ground contact shadow (rows 46-47, x=6..57)
for x in range(6, 58):
    fp[46][x] = (12, 8, 6, 140)
    fp[47][x] = (8, 5, 3, 80)

# Hearth Stone Apron extending on floor (rows 42-45, x=6..57)
for y in range(42, 46):
    for x in range(6, 58):
        if y == 42:
            fp[y][x] = (100, 95, 90) # Highlight stone edge
        elif y == 45:
            fp[y][x] = (45, 42, 40) # Shadow stone bottom
        elif (x - 6) % 12 == 0:
            fp[y][x] = (35, 32, 30) # Stone tile joints
        else:
            fp[y][x] = (70, 66, 62) if (x + y) % 3 == 0 else (60, 56, 52)

# Outer Stone Columns & Mantle Frame (x=6..16 and x=47..57, y=8..42)
for y in range(8, 42):
    for x in range(6, 58):
        # Pillars on sides
        is_pillar = (x < 17 or x > 46)
        is_lintel = (y < 18)
        if is_pillar or is_lintel:
            # Stone texture with 3D bevel
            if x in (6, 47): # Left edge of pillar (light)
                fp[y][x] = (110, 102, 95)
            elif x in (16, 57): # Right edge of pillar (shadow)
                fp[y][x] = (38, 35, 32)
            elif y in (8, 9): # Lintel top highlight
                fp[y][x] = (105, 98, 90)
            elif y in (16, 17): # Lintel arch bottom shadow
                fp[y][x] = (32, 28, 25)
            elif (x + y) % 7 == 0:
                fp[y][x] = (80, 74, 68) # Stone texture
            else:
                fp[y][x] = (65, 60, 55)

# Classical Decorative Relief Carving on Lintel (y=11..15, x=22..41)
for y in range(11, 16):
    for x in range(22, 42):
        if y in (11, 15) or x in (22, 41):
            fp[y][x] = (40, 36, 32)
        elif (x + y) % 3 == 0:
            fp[y][x] = GOLD_MID
        else:
            fp[y][x] = (85, 78, 70)

# Deep 3D Cavernous Firebox Recess (y=18..42, x=17..47)
for y in range(18, 42):
    for x in range(17, 47):
        # Left angled receding firebrick wall (x=17..22)
        if x < 23:
            depth_shade = (x - 16) * 4
            fp[y][x] = (25 + depth_shade, 16 + depth_shade, 12 + depth_shade)
        # Right angled receding firebrick wall (reflecting fire glow! x=41..46)
        elif x > 40:
            dist_fire = (47 - x)
            fp[y][x] = (65 + dist_fire * 8, 28 + dist_fire * 4, 14)
        # Deep back soot wall (x=23..40)
        else:
            # Dark soot fading to black
            if y < 24:
                fp[y][x] = (12, 8, 6) # Top cavern shadow
            elif (x + y) % 4 == 0:
                fp[y][x] = (28, 16, 12) # Faint brick texture
            else:
                fp[y][x] = (18, 10, 8)

# Wrought-Iron Fire Grate & Andirons (y=36..41, x=22..42)
for x in range(22, 43):
    if x in (23, 41): # Tall brass andiron finials
        fp[33][x] = GOLD_HIGH
        fp[34][x] = GOLD_MID
        fp[35][x] = (60, 45, 20)
        fp[36][x] = (20, 20, 20)
    if x % 3 == 0 and 37 <= y <= 40:
        fp[38][x] = (40, 40, 40)
        fp[39][x] = (20, 20, 20)

# Burning Logs with Glowing Embers & Living Flame Core (y=26..41, x=24..40)
# Dark charred oak logs
for x in range(24, 41):
    fp[39][x] = (35, 18, 10)
    fp[40][x] = (20, 10, 5)
    fp[37][x] = (45, 22, 12) if 26 <= x <= 38 else fp[37][x]

# Crackling Glowing Coals & Embers (y=38..41, x=26..38)
for y in range(38, 42):
    for x in range(26, 39):
        if (x + y) % 2 == 0:
            fp[y][x] = (255, 140, 30) # Brilliant orange ember
        else:
            fp[y][x] = (200, 45, 15)  # Crimson glowing coal

# Fiery Flame Tongues (y=26..37, x=27..37)
for y in range(26, 38):
    spread = int(math.sin((37 - y) / 11.0 * math.pi) * 5.5) + 1
    for dx in range(-spread, spread + 1):
        fx = 32 + dx
        if 25 <= fx <= 39:
            dist_core = abs(dx)
            if y > 32 and dist_core <= 1:
                fp[y][fx] = (255, 255, 210) # White-hot flame heart
            elif y > 29 and dist_core <= 2:
                fp[y][fx] = (255, 215, 60)  # Bright golden fire
            elif dist_core <= spread - 1:
                fp[y][fx] = (255, 125, 20)  # Vibrant orange flame
            else:
                fp[y][fx] = (210, 45, 15)   # Outer crimson lick

# Top Mantel Shelf with 3D Depth (rows 0..8, x=2..61)
for y in range(9):
    for x in range(2, 62):
        if y == 0:
            fp[y][x] = (130, 85, 55) # Top bevel highlight of polished mahogany
        elif y in (1, 2, 3):
            # Top surface of the mantel shelf receding in 3D perspective!
            grain = (x * 5 + y * 7) % 6
            fp[y][x] = (95, 55, 34) if grain == 0 else (80, 45, 26)
        elif y == 4:
            fp[y][x] = (140, 95, 60) # Front edge highlight catch
        elif y in (5, 6):
            fp[y][x] = (70, 38, 22)  # Front face of mantel shelf
        elif y in (7, 8):
            fp[y][x] = (28, 14, 8)   # Heavy drop shadow cast onto stone below

# Objects Resting on the Mantel Shelf:
# Center Antique Brass Carriage Clock (x=28..35, y=0..4)
for cy in range(0, 5):
    for cx in range(28, 36):
        if cy == 0:
            fp[cy][cx] = GOLD_HIGH if cx in (31, 32) else GOLD_MID # Top handle finial
        elif cy in (1, 2, 3):
            if cx in (28, 35) or cy == 1:
                fp[cy][cx] = GOLD_MID # Brass housing
            elif cx in (31, 32) and cy == 2:
                fp[cy][cx] = (30, 30, 30) # Clock hands
            else:
                fp[cy][cx] = (245, 240, 225) # White enamel clock dial
        elif cy == 4:
            fp[cy][cx] = GOLD_DARK # Brass clock base

# Left Candlestick with Wax & Flame (x=10..14, y=0..4)
fp[0][12] = (255, 230, 110) # Candle flame tip
fp[1][12] = (255, 140, 30)  # Flame base
fp[2][12] = (240, 235, 220) # White candle wax
fp[3][12] = (220, 215, 200) # Wax cylinder with drip
fp[4][11] = GOLD_MID; fp[4][12] = GOLD_HIGH; fp[4][13] = GOLD_MID # Brass candle base

# Right Candlestick with Wax & Flame (x=49..53, y=0..4)
fp[0][51] = (255, 230, 110) # Candle flame tip
fp[1][51] = (255, 140, 30)  # Flame base
fp[2][51] = (240, 235, 220) # White candle wax
fp[3][51] = (220, 215, 200) # Wax cylinder with drip
fp[4][50] = GOLD_MID; fp[4][51] = GOLD_HIGH; fp[4][52] = GOLD_MID # Brass candle base

save_png('assets/mansion/fireplace.png', 64, 48, fp)

# ==============================================================================
# 5. GRAND VICTORIAN BOOKCASE (64x64) - 3D Crown, Deep Recesses, Books & Cabinets
# ==============================================================================
bc = [[CLR for _ in range(64)] for _ in range(64)]

# Floor contact shadow (rows 62-63, x=2..61)
for x in range(2, 62):
    bc[62][x] = (15, 8, 4, 150)
    bc[63][x] = (10, 5, 2, 80)

# Outer Frame & Fluted Side Columns (x=2..7 and x=56..61, y=0..62)
for y in range(62):
    for x in range(2, 62):
        if x < 8 or x > 55:
            # Pillar 3D shading
            if x in (2, 56):
                bc[y][x] = MAHOG_DEEP # Outer contour line
            elif x in (3, 57):
                bc[y][x] = MAHOG_HIGH # Left specular rim
            elif x in (6, 60):
                bc[y][x] = (50, 28, 16) # Right fluted shadow
            elif x in (7, 61):
                bc[y][x] = MAHOG_DEEP # Inner shadow into shelf cavity
            else:
                bc[y][x] = MAHOG_MID

# Top Carved Cornice Pediment with 3D Depth (rows 0..6, x=0..63)
for y in range(7):
    for x in range(64):
        if y == 0:
            bc[y][x] = (135, 88, 55) # Top rim highlight
        elif y in (1, 2):
            bc[y][x] = (95, 56, 34)  # Top sloping surface of crown
        elif y == 3:
            bc[y][x] = GOLD_HIGH if (x % 4 in (0, 1)) else GOLD_MID # Carved dentil molding
        elif y in (4, 5):
            bc[y][x] = MAHOG_MID
        elif y == 6:
            bc[y][x] = (24, 12, 6)   # Deep drop shadow over top shelf

# Middle Counter Ledge dividing Shelves & Cabinets (rows 42..45, x=2..61)
for y in range(42, 46):
    for x in range(2, 62):
        if y == 42:
            bc[y][x] = MAHOG_HIGH # Highlighted ledge
        elif y == 43:
            bc[y][x] = (90, 52, 30) # Ledge surface
        elif y == 44:
            bc[y][x] = MAHOG_MID
        elif y == 45:
            bc[y][x] = MAHOG_DEEP # Shadow under ledge

# 3 Shelves Cavity (rows 7..42, x=8..55)
# Deep ambient shadow back wall
for y in range(7, 42):
    for x in range(8, 56):
        bc[y][x] = (24, 14, 9) if (x + y) % 4 != 0 else (18, 10, 6)

# Shelf Boards (horizontal mahogany planks with 3D bevels)
# Shelf 1 board: rows 18-19, Shelf 2 board: rows 30-31
for s_y in (18, 30):
    for x in range(8, 56):
        bc[s_y][x] = MAHOG_HIGH     # Lit shelf edge
        bc[s_y + 1][x] = MAHOG_DEEP # Underside shelf shadow

# Rich Leather Books on Shelves with varied heights, colors & gold tooling
import random
random.seed(333)

def draw_books(start_y, shelf_board_y):
    x = 9
    colors = [
        (BURGUNDY_HI, BURGUNDY_MD, GOLD_HIGH), # Crimson Tome
        ((35, 75, 140), (20, 45, 90), GOLD_HIGH), # Royal Blue Encyclopedia
        ((30, 85, 50), (18, 55, 30), GOLD_HIGH),  # Emerald Folio
        (GOLD_MID, GOLD_DARK, (255, 230, 140)),    # Gilded Grimoire
        ((110, 60, 30), (70, 35, 18), GOLD_HIGH), # Brown Leather Journal
        ((75, 30, 75), (45, 18, 45), GOLD_HIGH),   # Velvet Plum Book
    ]
    while x < 54:
        # Occasionally leave an empty space or place a curio object
        if x == 28 and start_y == 7: # Golden brass hourglass on shelf 1
            for hy in range(start_y + 3, shelf_board_y):
                bc[hy][29] = GOLD_MID; bc[hy][30] = GOLD_HIGH; bc[hy][31] = GOLD_MID
            bc[shelf_board_y - 1][28] = GOLD_DARK; bc[shelf_board_y - 1][32] = GOLD_DARK
            x += 6
            continue
        elif x == 36 and start_y == 19: # Rolled parchment scroll on shelf 2
            for sy in range(start_y + 4, shelf_board_y):
                bc[sy][37] = (240, 230, 200); bc[sy][38] = (210, 195, 160)
            bc[start_y + 6][37] = BURGUNDY_HI; bc[start_y + 6][38] = BURGUNDY_HI # Red tie ribbon
            x += 4
            continue

        book_w = random.choice([2, 3, 4])
        book_h = random.choice([8, 9, 10, 11])
        c_hi, c_md, c_gold = random.choice(colors)
        top_y = shelf_board_y - book_h

        # Leaning book at the end of shelf?
        if x > 49 and random.random() < 0.6:
            for dy in range(book_h):
                bx = x + int(dy * 0.3)
                by = shelf_board_y - dy - 1
                if 8 <= bx < 55 and start_y <= by < shelf_board_y:
                    bc[by][bx] = c_hi
                    if bx + 1 < 55: bc[by][bx + 1] = c_md
            break

        for bx in range(x, min(x + book_w, 55)):
            for by in range(top_y, shelf_board_y):
                if by == top_y:
                    bc[by][bx] = (240, 230, 200) # Top exposed paper pages
                elif bx == x:
                    bc[by][bx] = c_hi # Spine highlight
                elif bx == x + book_w - 1:
                    bc[by][bx] = c_md # Spine shadow
                elif by in (top_y + 2, top_y + 4, shelf_board_y - 3):
                    bc[by][bx] = c_gold # Gold spine rib
                else:
                    bc[by][bx] = c_md
        x += book_w

draw_books(7, 18)   # Shelf 1 (top)
draw_books(19, 30)  # Shelf 2 (middle)
draw_books(31, 42)  # Shelf 3 (bottom)

# Lower Cabinet Raised-Panel Doors (rows 46..61, x=8..55)
# Two paneled doors (Door 1: x=9..30, Door 2: x=33..54)
for d_start in (9, 33):
    d_end = d_start + 21
    for y in range(46, 61):
        for x in range(d_start, d_end + 1):
            # Outer door frame
            if y in (46, 60) or x in (d_start, d_end):
                bc[y][x] = (45, 24, 13)
            # Inset panel (x=d_start+3..d_end-3, y=49..57)
            elif (d_start + 3 <= x <= d_end - 3) and (49 <= y <= 57):
                if y == 49 or x == d_start + 3:
                    bc[y][x] = (28, 14, 7)   # Inset top/left shadow
                elif y == 57 or x == d_end - 3:
                    bc[y][x] = MAHOG_HIGH    # Inset bottom/right highlight
                else:
                    # Raised inner panel
                    bc[y][x] = (75, 42, 24) if (x + y) % 3 != 0 else (82, 46, 26)
            else:
                bc[y][x] = (62, 34, 19)

    # Brass Keyhole & Teardrop Handles
    hx = d_end - 2 if d_start == 9 else d_start + 2
    bc[52][hx] = GOLD_HIGH
    bc[53][hx] = GOLD_MID
    bc[54][hx] = (30, 20, 10) # Drop shadow of handle

# Bottom Plinth Base (rows 60..62, x=2..61)
for x in range(2, 62):
    bc[61][x] = MAHOG_HIGH
    bc[62][x] = MAHOG_DEEP

save_png('assets/mansion/bookcase.png', 64, 64, bc)

# ==============================================================================
# 6. VINTAGE CANOPY / CARVED BED (48x64) - 3D Curved Quilt, Fluffy Pillows & Posts
# ==============================================================================
bed = [[CLR for _ in range(48)] for _ in range(64)]

# Floor contact shadow under bed frame (rows 61-63, x=3..44)
for x in range(3, 45):
    bed[61][x] = (15, 8, 4, 150)
    bed[62][x] = (10, 5, 2, 100)
    bed[63][x] = (8, 4, 2, 40)

# Carved Mahogany Headboard (rows 0..15, x=4..43)
for y in range(16):
    for x in range(4, 44):
        # Top arch crest
        dx = abs(x - 23.5)
        arch_limit = 2 + int((dx / 20.0)**2 * 6)
        if y < arch_limit:
            continue
        if y == arch_limit:
            bed[y][x] = MAHOG_HIGH # Carved crest top highlight
        elif x in (4, 5, 42, 43): # Stately corner bedposts
            bed[y][x] = MAHOG_HIGH if x in (5, 42) else MAHOG_DEEP
        elif y in (arch_limit + 1, 14):
            bed[y][x] = (50, 28, 16)
        elif (x % 6 == 0):
            bed[y][x] = (35, 18, 10) # Fluted vertical headboard carvings
        else:
            bed[y][x] = MAHOG_MID

# Golden Finials on Top of Headboard Posts (rows 0..2, x=4..6 and x=41..43)
for fx in (5, 42):
    bed[0][fx] = GOLD_HIGH
    bed[1][fx - 1] = GOLD_MID; bed[1][fx] = GOLD_HIGH; bed[1][fx + 1] = GOLD_MID
    bed[2][fx] = GOLD_DARK

# Two Luxurious Plump Down Pillows with Creases (rows 12..22, x=7..40)
for p_idx, (px1, px2) in enumerate([(7, 22), (25, 40)]):
    for y in range(12, 23):
        for x in range(px1, px2 + 1):
            # Rounded pillow contour
            ed_x = min(x - px1, px2 - x)
            ed_y = min(y - 12, 22 - y)
            if ed_x == 0 or ed_y == 0:
                bed[y][x] = (180, 175, 165) # Pillow seam
            elif ed_x == 1 or ed_y == 1:
                bed[y][x] = (220, 215, 205) # Pillow edge
            else:
                # Plump pillow center with soft indentation
                if x == (px1 + px2) // 2 and y in (16, 17):
                    bed[y][x] = (205, 198, 188) # Indent shadow
                elif ed_y >= 3 and ed_x >= 3:
                    bed[y][x] = (255, 252, 245) # Fluffy white highlight
                else:
                    bed[y][x] = (240, 235, 228)

# Crisp White Turned-Down Linen Sheet Fold (rows 21..25, x=6..41)
for y in range(21, 26):
    for x in range(6, 42):
        if y == 21:
            bed[y][x] = (190, 185, 175) # Shadow under pillows
        elif y == 22:
            bed[y][x] = (255, 255, 250) # Bright crisp linen fold edge
        elif y in (23, 24):
            bed[y][x] = (245, 240, 230) if x % 4 != 0 else GOLD_MID # Embroidered trim
        elif y == 25:
            bed[y][x] = (160, 150, 140) # Shadow cast onto quilt below

# Volumetric Quilted Emerald Velvet Duvet (rows 25..54, x=4..43)
for y in range(25, 55):
    for x in range(4, 44):
        # Rounded 3D curvature: highlights along the center ridge, shadow rolling down sides
        dist_center = abs(x - 23.5) / 19.5 # 0.0 at center, 1.0 at edge
        # Quilt Diamond Tufting Geometry
        is_tuft_node = ((x + y) % 6 == 0 and (x - y) % 6 == 0)
        is_seam_line = ((x + y) % 6 in (0, 1) or (x - y) % 6 in (0, 1))

        # Base emerald tones shaded by 3D cylinder curvature
        if dist_center > 0.85:
            base_col = (12, 28, 22) # Steep side drop
        elif dist_center > 0.6:
            base_col = (18, 42, 34)
        elif dist_center < 0.3:
            base_col = (34, 76, 62) # Center top highlight ridge
        else:
            base_col = (26, 58, 48)

        if is_tuft_node:
            bed[y][x] = (10, 22, 18) # Tufting button depression
        elif is_seam_line:
            bed[y][x] = (base_col[0] - 6, base_col[1] - 8, base_col[2] - 6)
        else:
            # Highlight puffy pillowing inside diamond
            bed[y][x] = (clamp(base_col[0] + 8), clamp(base_col[1] + 12), clamp(base_col[2] + 10))

# Folded Wine-Red Velvet Throw Runner Across Bottom (rows 41..52, x=4..43)
for y in range(41, 53):
    for x in range(4, 44):
        dist_center = abs(x - 23.5) / 19.5
        if y in (41, 52): # Gold embroidered border trim
            bed[y][x] = GOLD_HIGH if (x + y) % 2 == 0 else GOLD_MID
        elif y == 42:
            bed[y][x] = BURGUNDY_HI # Top highlight of folded throw
        elif dist_center > 0.85:
            bed[y][x] = BURGUNDY_DK # Side drape shadow
        elif dist_center < 0.3:
            bed[y][x] = BURGUNDY_HI if (x + y) % 4 == 0 else BURGUNDY_MD
        else:
            bed[y][x] = BURGUNDY_MD

# Carved Mahogany Footboard with Turned Posts (rows 53..62, x=3..44)
for y in range(53, 62):
    for x in range(3, 45):
        if x in (3, 4, 43, 44): # Corner footboard posts
            if y == 53:
                bed[y][x] = GOLD_HIGH # Brass post cap
            elif x in (4, 43):
                bed[y][x] = MAHOG_HIGH
            else:
                bed[y][x] = MAHOG_DEEP
        else: # Footboard horizontal carved rail
            if y == 54:
                bed[y][x] = MAHOG_HIGH # Top rail highlight
            elif y in (55, 56):
                bed[y][x] = MAHOG_MID
            elif y in (57, 58):
                bed[y][x] = (60, 32, 18) if x % 6 != 0 else GOLD_MID # Inset rosettes
            elif y == 59:
                bed[y][x] = MAHOG_DEEP # Rail bottom shadow
            else:
                bed[y][x] = (30, 15, 8)

save_png('assets/mansion/vintage_bed.png', 48, 64, bed)

# ==============================================================================
# 7. MESA DE NOCHE / NIGHTSTAND (32x40) - 3D Box, Beveled Drawers & Brass Lamp
# ==============================================================================
ns = [[CLR for _ in range(32)] for _ in range(40)]

# Ground contact shadow under legs (rows 38-39, x=4..27)
for x in (5, 6, 7, 24, 25, 26):
    ns[38][x] = (12, 6, 3, 140)
    ns[39][x] = (8, 4, 2, 70)

# Nightstand Wooden Body (rows 18..38, x=5..26)
# Top Surface with 3D Depth (rows 18..23, depth = 6 px!)
for y in range(18, 24):
    for x in range(5, 27):
        if y == 18:
            ns[y][x] = MAHOG_HIGH # Back rim
        elif y in (19, 20, 21):
            # Polished mahogany tabletop
            grain = (x * 7 + y * 11) % 5
            ns[y][x] = (95, 55, 34) if grain == 0 else (82, 46, 26)
        elif y == 22:
            ns[y][x] = (130, 85, 52) # Beveled front edge highlight catch
        elif y == 23:
            ns[y][x] = MAHOG_DEEP # Shadow under tabletop lip

# Objects on Tabletop: Antique Brass Skeleton Key & Golden Coins
# Skeleton Key (x=7..11, y=19..21)
ns[19][8] = GOLD_HIGH; ns[19][9] = GOLD_HIGH; ns[19][10] = GOLD_HIGH # Ring
ns[20][10] = GOLD_HIGH; ns[21][10] = GOLD_HIGH # Shaft
ns[21][11] = GOLD_HIGH # Tooth

# Gold Sovereign Coins (x=21..24, y=19..21)
ns[19][22] = GOLD_HIGH; ns[19][23] = GOLD_MID
ns[20][21] = GOLD_HIGH; ns[20][22] = GOLD_HIGH; ns[20][23] = GOLD_MID
ns[21][22] = GOLD_DARK; ns[21][23] = GOLD_DARK

# Drawers Front Face (rows 24..35, x=5..26)
# Drawer 1: rows 24..28, Drawer 2: rows 30..34
for d_y in (24, 30):
    for y in range(d_y, d_y + 5):
        for x in range(6, 26):
            if y == d_y or x == 6:
                ns[y][x] = (105, 62, 38) # Drawer top/left bevel highlight
            elif y == d_y + 4 or x == 25:
                ns[y][x] = (35, 18, 10)  # Drawer bottom/right bevel shadow
            else:
                ns[y][x] = (68, 38, 22)
    # Brass Handle in center of drawer
    ns[d_y + 2][15] = GOLD_HIGH; ns[d_y + 2][16] = GOLD_HIGH
    ns[d_y + 3][15] = (30, 20, 10) # Handle drop shadow

# Divider between drawers & bottom base
for x in range(5, 27):
    ns[29][x] = MAHOG_DEEP
    ns[35][x] = MAHOG_HIGH
    ns[36][x] = MAHOG_DEEP

# 4 Carved Cabriole Legs (rows 36..38, x=5..8 and x=23..26)
for y in range(36, 39):
    for x in (5, 6, 25, 26):
        ns[y][x] = MAHOG_HIGH if x in (6, 25) else MAHOG_DEEP

# Vintage Bedside Lamp with Bell Fabric Shade & Brass Pedestal (rows 1..17, centered x=16)
# Brass Finial on top
ns[1][15] = GOLD_HIGH; ns[1][16] = GOLD_MID

# Fluted Bell Fabric Shade with Warm 3D Cylinder Lighting (rows 2..11, x=10..22)
for y in range(2, 12):
    # Bell curve expands downward
    w_half = 2 + int((y - 2) * 0.45)
    for dx in range(-w_half, w_half + 1):
        lx = 15 + dx
        if 9 <= lx <= 23:
            dist_u = (dx + w_half) / (2.0 * w_half) # 0.0 left to 1.0 right
            if y == 11:
                # Scalloped bottom fringe / bead trim
                ns[y][lx] = GOLD_HIGH if dx % 2 == 0 else (255, 240, 190)
            elif y == 2:
                ns[y][lx] = (200, 150, 70) # Top shade rim
            elif dist_u < 0.25:
                ns[y][lx] = (220, 175, 90) # Left rim shadow
            elif dist_u < 0.55:
                ns[y][lx] = (255, 250, 215) # Intense warm fabric highlight
            elif dist_u < 0.85:
                ns[y][lx] = (255, 230, 150) # Warm amber translucent core
            else:
                ns[y][lx] = (210, 160, 80)  # Right shadow

# Turned Brass Pedestal Base (rows 12..18, x=13..18)
for y in range(12, 19):
    if y in (12, 13): # Brass neck under shade
        ns[y][15] = BRASS_LGT; ns[y][16] = BRASS_MID
    elif y in (14, 15): # Bulbous turned baluster
        ns[y][14] = BRASS_LGT; ns[y][15] = (255, 235, 140); ns[y][16] = BRASS_MID; ns[y][17] = BRASS_DARK
    elif y in (16, 17): # Round flared pedestal foot
        for bx in range(13, 19):
            ns[y][bx] = (255, 230, 130) if bx in (14, 15) else BRASS_MID

save_png('assets/mansion/nightstand_lamp.png', 32, 40, ns)

# ==============================================================================
# 8. ESCRITORIO DE ESTUDIO / DESK (64x36) - 16px Deep Desktop, Inlay & Banker Lamp
# ==============================================================================
desk = [[CLR for _ in range(64)] for _ in range(36)]

# Floor contact shadow under pedestals (rows 34-35, x=3..60)
for x in range(3, 61):
    if x < 23 or x > 40: # Under pedestals
        desk[34][x] = (12, 6, 3, 150)
        desk[35][x] = (8, 4, 2, 80)
    else: # Under kneehole
        desk[35][x] = (8, 4, 2, 40)

# Large Desktop Surface with 3D Depth (rows 1..18, x=2..61, depth = 17 px!)
for y in range(1, 19):
    for x in range(2, 62):
        if y == 1:
            desk[y][x] = MAHOG_HIGH # Back rim highlight
        elif y == 17:
            desk[y][x] = (135, 88, 54) # Front beveled edge highlight catch
        elif y == 18:
            desk[y][x] = MAHOG_DEEP # Drop shadow under desktop overhang
        elif x in (2, 3, 60, 61) or y in (2, 3, 15, 16):
            # Rich Mahogany Wood Perimeter Frame
            grain = (x * 7 + y * 11) % 6
            desk[y][x] = (92, 54, 32) if grain == 0 else (78, 44, 25)
        elif x in (4, 59) or y in (4, 14):
            # Gilded Filigree Tooling Border around Leather Inlay
            desk[y][x] = GOLD_HIGH if (x + y) % 3 == 0 else GOLD_MID
        else:
            # Luxurious Dark Emerald Green Leather Writing Blotter Inlay!
            if (x * 13 + y * 7) % 11 == 0:
                desk[y][x] = (22, 52, 42)
            else:
                desk[y][x] = (16, 42, 34)

# Desktop Objects:
# Left: Victorian Banker's Lamp with Green Glass Hood (x=6..18, y=2..14)
# Curved brass gooseneck
desk[11][12] = BRASS_MID; desk[12][12] = BRASS_LGT
desk[13][11] = BRASS_LGT; desk[13][12] = BRASS_MID; desk[13][13] = BRASS_DARK
desk[14][10] = BRASS_MID; desk[14][11] = BRASS_LGT; desk[14][12] = BRASS_MID; desk[14][13] = BRASS_DARK
desk[15][10] = BRASS_DARK; desk[15][11] = BRASS_MID; desk[15][12] = BRASS_DARK # Brass base

# Emerald-Green Glass Hood with Specular Reflection (x=6..18, y=3..8)
for hy in range(3, 9):
    for hx in range(6, 19):
        if hy == 3: # Top glass highlight reflection
            desk[hy][hx] = (110, 240, 160) if 8 <= hx <= 15 else (30, 130, 80)
        elif hy in (4, 5):
            desk[hy][hx] = (15, 100, 60) if 7 <= hx <= 16 else (10, 65, 40)
        elif hy == 6:
            desk[hy][hx] = (10, 75, 45)
        elif hy in (7, 8): # Bottom rim & glowing bulb
            desk[hy][hx] = (255, 235, 140) if 9 <= hx <= 14 else (40, 140, 80)

# Center: Open Antiquarian Manuscript Letter & Quill (x=24..39, y=5..14)
for py in range(5, 14):
    for px in range(25, 39):
        if px == 31: # Center page fold
            desk[py][px] = (180, 170, 150)
        elif (py in (5, 13) or px in (25, 38)):
            desk[py][px] = (210, 200, 175) # Page edges
        elif py % 2 == 1 and 26 <= px <= 37 and px != 31:
            desk[py][px] = (60, 45, 35) # Handwritten ink text lines!
        else:
            desk[py][px] = (245, 238, 218) # Aged cream parchment

# Crimson Wax Seal on Letter
desk[11][35] = BURGUNDY_HI; desk[11][36] = BURGUNDY_MD; desk[12][35] = BURGUNDY_HI; desk[12][36] = BURGUNDY_MD

# Antique Brass Inkpot & White Feather Quill (x=22..25, y=3..10)
desk[9][23] = (30, 30, 30); desk[10][23] = BRASS_LGT; desk[10][24] = BRASS_MID # Inkwell
desk[4][21] = (255, 255, 250) # Quill tip
desk[5][21] = (245, 240, 230); desk[5][22] = (255, 255, 250)
desk[6][22] = (240, 235, 220); desk[7][22] = (230, 225, 210)
desk[8][23] = (210, 200, 180) # Quill shaft entering inkpot

# Right: Leather Research Journal with Brass Corner Brackets (x=44..55, y=5..13)
for jy in range(5, 14):
    for jx in range(44, 56):
        is_corner = (jx in (44, 45, 54, 55) and jy in (5, 6, 12, 13))
        if is_corner:
            desk[jy][jx] = GOLD_HIGH if (jx + jy) % 2 == 0 else GOLD_MID
        elif jx == 44:
            desk[jy][jx] = (140, 40, 50) # Book spine highlight
        elif jx == 55:
            desk[jy][jx] = (230, 220, 190) # Exposed pages
        else:
            desk[jy][jx] = (85, 24, 32) # Rich burgundy leather cover

# Desk Front Face: Pedestals & Deep Kneehole Recess (rows 19..34)
# Deep Kneehole Recess (x=23..40, rows 19..34)
for y in range(19, 35):
    for x in range(23, 41):
        if y < 24:
            desk[y][x] = (15, 8, 4) # Top ambient shadow
        elif (x + y) % 5 == 0:
            desk[y][x] = (32, 18, 10) # Modesty panel wood grain
        else:
            desk[y][x] = (22, 12, 6)

# Left Pedestal (x=4..22) & Right Pedestal (x=41..59)
for p_start in (4, 41):
    p_end = p_start + 18
    # 3 Drawers per pedestal
    for d_idx, d_y in enumerate([19, 24, 29]):
        for y in range(d_y, d_y + 4):
            for x in range(p_start + 1, p_end):
                if y == d_y or x == p_start + 1:
                    desk[y][x] = (105, 62, 38) # Bevel highlight
                elif y == d_y + 3 or x == p_end - 1:
                    desk[y][x] = (32, 16, 8)   # Bevel shadow
                else:
                    desk[y][x] = (68, 38, 22)
        # Ornate Brass Bail Handles
        hx = p_start + 9
        desk[d_y + 1][hx - 1] = GOLD_MID; desk[d_y + 1][hx] = GOLD_HIGH; desk[d_y + 1][hx + 1] = GOLD_MID
        desk[d_y + 2][hx] = (30, 20, 10) # Handle drop shadow

    # Base Plinth of Pedestal (rows 33..34)
    for y in range(33, 35):
        for x in range(p_start, p_end + 1):
            desk[y][x] = MAHOG_HIGH if y == 33 else MAHOG_DEEP

save_png('assets/mansion/study_desk.png', 64, 36, desk)

# ==============================================================================
# 9. SILLON / ARMCHAIR (32x36) - 3/4 Perspective, Deep Tufting, Padded Arms & Legs
# ==============================================================================
chair = [[CLR for _ in range(32)] for _ in range(36)]

# Floor contact shadow under legs (rows 34-35, x=4..27)
for x in range(4, 28):
    if x in (5, 6, 7, 24, 25, 26):
        chair[34][x] = (12, 6, 3, 140)
        chair[35][x] = (8, 4, 2, 70)
    else:
        chair[35][x] = (10, 5, 2, 40)

# Curved Mahogany Backrest Top Crest (rows 2..5, x=5..26)
for y in range(2, 6):
    for x in range(5, 27):
        if y == 2:
            chair[y][x] = MAHOG_HIGH if 13 <= x <= 18 else (75, 42, 24) # Carved center crest
        elif y in (3, 4):
            chair[y][x] = MAHOG_MID
        elif y == 5:
            chair[y][x] = MAHOG_DEEP # Shadow under crest

# Padded Wine-Red Velvet Backrest with Diamond Tufting (rows 6..16, x=6..25)
for y in range(6, 17):
    for x in range(6, 26):
        dist_x = abs(x - 15.5) / 10.0
        # Tufting buttons & creases
        is_button = (x in (11, 16, 21) and y in (9, 13))
        is_crease = ((x + y) % 4 == 0)
        if is_button:
            chair[y][x] = (35, 8, 14) # Deep tuft indentation
        elif is_crease:
            chair[y][x] = BURGUNDY_DK
        elif dist_x < 0.4:
            chair[y][x] = BURGUNDY_HI # Center highlight puff
        else:
            chair[y][x] = BURGUNDY_MD

# Padded Velvet Armrests (rows 10..27, Left x=3..8, Right x=23..28)
for y in range(10, 28):
    # Left Armrest (receiving light from top-left)
    for x in range(3, 9):
        if x == 3:
            chair[y][x] = BURGUNDY_DK # Outer edge contour
        elif x == 5:
            chair[y][x] = BURGUNDY_HI # Longitudinal highlight strip on padded arm!
        else:
            chair[y][x] = BURGUNDY_MD

    # Right Armrest (in slight shadow)
    for x in range(23, 29):
        if x == 28:
            chair[y][x] = BURGUNDY_DK
        elif x == 25:
            chair[y][x] = (120, 28, 42) # Softer highlight strip
        else:
            chair[y][x] = BURGUNDY_MD

    # Carved Mahogany Front Scroll Caps on Armrests (rows 25..27)
    for x in (4, 5, 6, 7):
        chair[26][x] = MAHOG_HIGH; chair[27][x] = MAHOG_MID
    for x in (24, 25, 26, 27):
        chair[26][x] = MAHOG_HIGH; chair[27][x] = MAHOG_MID

# Plump Tufted Seat Cushion with 3D Depth (rows 16..27, x=8..23)
for y in range(16, 28):
    for x in range(8, 24):
        dist_c = math.sqrt(((x - 15.5) / 8.0)**2 + ((y - 21.5) / 6.0)**2)
        if y == 16:
            chair[y][x] = (25, 6, 10) # Deep shadow at junction with backrest
        elif y == 27:
            chair[y][x] = BURGUNDY_HI if 11 <= x <= 20 else BURGUNDY_MD # Front rounded cushion lip
        elif dist_c < 0.4:
            chair[y][x] = BURGUNDY_HI # Plump cushion top highlight
        elif dist_c > 0.8:
            chair[y][x] = BURGUNDY_DK # Side compression
        else:
            chair[y][x] = BURGUNDY_MD

# Front Carved Apron & Cabriole Legs (rows 28..34, x=4..27)
for y in range(28, 31):
    for x in range(5, 27):
        if y == 28:
            chair[y][x] = MAHOG_HIGH # Top apron edge
        elif (x in (14, 15, 16, 17)):
            chair[y][x] = GOLD_MID # Center carved acanthus leaf ornament
        else:
            chair[y][x] = MAHOG_MID

# Carved Wooden Cabriole Legs (rows 30..34, x=4..8 and x=23..27)
for y in range(30, 35):
    # Left Leg
    chair[y][5] = MAHOG_DEEP; chair[y][6] = MAHOG_HIGH; chair[y][7] = MAHOG_MID
    # Right Leg
    chair[y][24] = MAHOG_DEEP; chair[y][25] = MAHOG_HIGH; chair[y][26] = MAHOG_MID

save_png('assets/mansion/armchair.png', 32, 36, chair)

# ==============================================================================
# 10. VENTANAL GOTICO / WINDOW (32x48) - Deep Wooden Arch, Curtains & Moonlit Sky
# ==============================================================================
win = [[CLR for _ in range(32)] for _ in range(48)]

for y in range(48):
    for x in range(32):
        # Gothic Pointed Arch Equation
        dx = abs(x - 15.5)
        arch_y = int((dx / 12.0)**1.5 * 14)
        if y < arch_y:
            continue

        # Outer Heavy Mahogany Arch Frame (3-4px thick)
        if y < arch_y + 3 or dx > 11:
            win[y][x] = MAHOG_HIGH if x < 16 else MAHOG_DEEP
        elif y < arch_y + 5 or dx > 9:
            win[y][x] = (45, 24, 14) # Inner frame reveal shadow
        elif dx > 7:
            # Tied-Back Deep Ruby Velvet Drapes / Curtains!
            if (x in (8, 23)) and y in (25, 26):
                win[y][x] = GOLD_HIGH # Gold tie-back tassel rope
            elif (x in (7, 24)):
                win[y][x] = BURGUNDY_HI # Curtain fold highlight
            else:
                win[y][x] = BURGUNDY_MD
        else:
            # Leaded Diamond Glass Panes overlooking Moonlit Night Sky
            is_leaded_lead = ((x + y) % 5 == 0 or (x - y) % 5 == 0)
            if is_leaded_lead:
                win[y][x] = (25, 30, 45) # Dark lead came strip
            else:
                # Night sky gradient (deep indigo to midnight blue)
                # Pale Moon in upper right (x=17..20, y=10..13)
                dist_moon = math.sqrt((x - 18)**2 + (y - 11)**2)
                if dist_moon < 2.5:
                    win[y][x] = (255, 255, 220) # Glowing moon
                elif y > 35:
                    # Dark silhouetted pine tree branches outside
                    win[y][x] = (8, 12, 20) if (x * y) % 3 == 0 else (14, 22, 38)
                else:
                    win[y][x] = (16, 26, 48) if (x + y) % 7 == 0 else (22, 34, 60)

# Window Sill at Bottom (rows 44..47, x=2..29)
for y in range(44, 48):
    for x in range(2, 30):
        if y == 44:
            win[y][x] = MAHOG_HIGH # Sill top edge
        elif y in (45, 46):
            win[y][x] = MAHOG_MID
        else:
            win[y][x] = MAHOG_DEEP # Sill bottom shadow

save_png('assets/mansion/victorian_window.png', 32, 48, win)

# ==============================================================================
# 11. CUADRO AL OLEO / PAINTING (32x32) - Gilded Baroque Frame & Mysterious Canvas
# ==============================================================================
ptg = [[CLR for _ in range(32)] for _ in range(32)]

for y in range(32):
    for x in range(32):
        # Heavy Gilded Baroque Frame with Acanthus Leaves (4px border)
        edge_dist = min(x, 31 - x, y, 31 - y)
        if edge_dist == 0:
            ptg[y][x] = (30, 20, 8) # Outer contour
        elif edge_dist == 1:
            # High-relief gold leaf corner & edge flourishes
            ptg[y][x] = GOLD_HIGH if (x < 16 or y < 16) else GOLD_MID
        elif edge_dist == 2:
            ptg[y][x] = GOLD_MID if (x + y) % 2 == 0 else GOLD_DARK
        elif edge_dist == 3:
            ptg[y][x] = (40, 26, 10) # Inner shadow reveal
        else:
            # Inset Oil Painting: Solitary Figure in Cloak at Twilight Mansion
            cx = x - 4
            cy = y - 4
            if cy < 7:
                # Twilight sky gradient (amber gold to stormy purple)
                ptg[y][x] = (180, 110, 60) if cy > 4 else (90, 50, 75)
            elif cy < 15:
                # Silhouetted mansion on hill & gnarled dead oak tree
                if cx in (15, 16) and cy in (9, 10, 11, 12, 13, 14):
                    # Solitary mysterious figure in top hat / dark cloak
                    ptg[y][x] = (15, 10, 15)
                elif cx in (7, 8, 9) and cy in (8, 9, 10):
                    # Distant glowing mansion window (amber light!)
                    ptg[y][x] = (255, 200, 80)
                elif (cx + cy) % 4 == 0 and cx < 14:
                    ptg[y][x] = (35, 22, 28) # Mansion silhouette
                else:
                    ptg[y][x] = (50, 32, 40)
            else:
                # Foreground dark misty ground
                ptg[y][x] = (28, 20, 22) if (cx * cy) % 3 != 0 else (38, 28, 28)

save_png('assets/mansion/oil_painting.png', 32, 32, ptg)

# ==============================================================================
# 12. UMBRAL DE PUERTA / THRESHOLD (32x72) - Solid Oak Beam & Brass Binder Bars
# ==============================================================================
thresh = [[MAHOG_MID for _ in range(32)] for _ in range(72)]
for y in range(72):
    for x in range(32):
        if y in (0, 1, 70, 71): # Deep door jamb shadows
            thresh[y][x] = (18, 9, 4)
        elif x in (0, 31): # Outer edge grooves
            thresh[y][x] = (28, 14, 7)
        elif x in (1, 30): # Polished Brass Binding Plate
            thresh[y][x] = GOLD_HIGH
        elif x in (2, 29):
            # Screws every 12 pixels along the brass strip
            thresh[y][x] = (60, 42, 15) if y % 12 in (0, 1) else GOLD_MID
        elif y % 12 == 11:
            thresh[y][x] = (32, 18, 9) # Oak board end joints
        elif y % 12 == 0:
            thresh[y][x] = (95, 58, 34) # Board joint highlight
        else:
            grain = (x * 7 + y * 13) % 7
            thresh[y][x] = (78, 44, 25) if grain == 0 else (65, 36, 20)

save_png('assets/mansion/doorway_threshold.png', 32, 72, thresh)

# ==============================================================================
# 13. WARM LIGHT GLOW (64x64)
# ==============================================================================
glow = [[CLR for _ in range(64)] for _ in range(64)]
for y in range(64):
    for x in range(64):
        dist = math.sqrt((x - 31.5)**2 + (y - 31.5)**2)
        if dist < 32.0:
            alpha = int((1.0 - (dist / 32.0))**1.8 * 165)
            glow[y][x] = (255, 210, 120, alpha)

save_png('assets/mansion/light_glow_warm.png', 64, 64, glow)

print('All 13 high-depth, true-perspective Victorian assets generated successfully!')
