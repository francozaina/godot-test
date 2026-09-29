import re

with open('scenes/world.tscn', 'r', encoding='utf-8') as f:
    content = f.read()

header_match = re.search(r'^(.*?)(\[node name="World".*)$', content, re.DOTALL)
if not header_match:
    print("Error: Could not parse world.tscn header")
    exit(1)

header = header_match.group(1)
nodes_part = header_match.group(2)

# Parse node blocks cleanly
raw_blocks = re.split(r'\n(?=\[node )', nodes_part)
blocks = []

for block in raw_blocks:
    first_line = block.split('\n')[0]
    name_m = re.search(r'name="([^"]+)"', first_line)
    parent_m = re.search(r'parent="([^"]+)"', first_line)
    if name_m:
        name = name_m.group(1)
        parent = parent_m.group(1) if parent_m else ""
        blocks.append({
            'name': name,
            'parent': parent,
            'block': block.strip()
        })

print(f"Parsed {len(blocks)} node blocks from world.tscn")

def update_parent_in_block(block_str, new_parent):
    lines = block_str.split('\n')
    if 'parent="' in lines[0]:
        lines[0] = re.sub(r'parent="[^"]*"', f'parent="{new_parent}"', lines[0])
    else:
        # Insert parent attribute right after name="..."
        lines[0] = re.sub(r'(name="[^"]*")', rf'\1 parent="{new_parent}"', lines[0])
    lines = [l for l in lines if not l.startswith('top_level = true')]
    return '\n'.join(lines)

out_blocks = []

# 1. World Root
world_b = [b for b in blocks if b['name'] == 'World'][0]
out_blocks.append(world_b['block'])

# 2. Environment (Grass Field)
out_blocks.append('[node name="Environment" type="Node2D" parent="." unique_id=393135298]\nz_index = -1')
for b in blocks:
    if b['name'] == 'GrassField':
        out_blocks.append(update_parent_in_block(b['block'], 'Environment'))

# 3. Trees Container (Tree_0 to Tree_503)
out_blocks.append('[node name="Trees" type="Node2D" parent="." unique_id=1315024014]\ny_sort_enabled = true')
for b in blocks:
    if b['name'].startswith('Tree_'):
        out_blocks.append(update_parent_in_block(b['block'], 'Trees'))

# 4. CentralRoom Container
out_blocks.append('[node name="CentralRoom" type="Node2D" parent="." unique_id=1291725721]\ny_sort_enabled = true')
out_blocks.append('[node name="Floor" type="Node2D" parent="CentralRoom" unique_id=393135299]\nz_index = -1')
for b in blocks:
    if b['name'] == 'MansionRoomFloor':
        out_blocks.append(update_parent_in_block(b['block'], 'CentralRoom/Floor'))

out_blocks.append('[node name="Walls" type="Node2D" parent="CentralRoom" unique_id=1291725723]')
central_wall_names = ["WallNorth", "WallEast", "WallSouthLeft", "WallSouthRight"]
for wname in central_wall_names:
    for b in blocks:
        if b['name'] == wname:
            out_blocks.append(update_parent_in_block(b['block'], 'CentralRoom/Walls'))
        elif b['parent'] == f'Walls/{wname}' or b['parent'].endswith(f'/{wname}'):
            out_blocks.append(update_parent_in_block(b['block'], f'CentralRoom/Walls/{wname}'))

# 5. VictorianRoom Container
out_blocks.append('[node name="VictorianRoom" type="Node2D" parent="." unique_id=1291725722]\ny_sort_enabled = true')
out_blocks.append('[node name="Floor" type="Node2D" parent="VictorianRoom" unique_id=393135300]\nz_index = -1')
for fname in ["MansionSuiteFloor", "VictorianRug", "DoorwayThreshold"]:
    for b in blocks:
        if b['name'] == fname:
            out_blocks.append(update_parent_in_block(b['block'], 'VictorianRoom/Floor'))

out_blocks.append('[node name="Walls" type="Node2D" parent="VictorianRoom" unique_id=1291725724]')
victorian_wall_names = ["WallBedroomNorth", "WallBedroomWest", "WallBedroomSouth", "WallDividingNorth", "WallDividingSouth"]
for wname in victorian_wall_names:
    for b in blocks:
        if b['name'] == wname:
            out_blocks.append(update_parent_in_block(b['block'], 'VictorianRoom/Walls'))
        elif b['parent'] == f'Walls/{wname}' or b['parent'].endswith(f'/{wname}'):
            out_blocks.append(update_parent_in_block(b['block'], f'VictorianRoom/Walls/{wname}'))

out_blocks.append('[node name="Furniture" type="Node2D" parent="VictorianRoom" unique_id=1291725725]\ny_sort_enabled = true')
furniture_names = ["MansionBookcase", "MansionFireplace", "MansionBed", "MansionNightstand", "MansionDesk", "MansionArmchairLeft", "MansionArmchairRight"]
for furn in furniture_names:
    for b in blocks:
        if b['name'] == furn:
            out_blocks.append(update_parent_in_block(b['block'], 'VictorianRoom/Furniture'))

# 6. Player & UI
for b in blocks:
    if b['name'] == 'Player':
        out_blocks.append(update_parent_in_block(b['block'], '.'))
    elif b['name'] == 'UI':
        out_blocks.append(update_parent_in_block(b['block'], '.'))
    elif b['parent'] == 'UI':
        out_blocks.append(update_parent_in_block(b['block'], 'UI'))
    elif b['parent'] == 'UI/HUDPanel' or b['parent'].endswith('HUDPanel'):
        out_blocks.append(update_parent_in_block(b['block'], 'UI/HUDPanel'))

new_content = header + '\n'.join(out_blocks) + '\n'
with open('scenes/world.tscn', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Reorganized world.tscn successfully! Output blocks: {len(out_blocks)}")
