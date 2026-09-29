import re

# 1. Generate double-layer perimeter tree coordinates for 2048x2048 map
tree_coords = []

# Outer bounds: 992 and 960
# X range from -992 to 992 step 32 (63 trees per line)
xs = [x for x in range(-992, 1024, 32)] # -992 to 992
ys = [y for y in range(-992, 1024, 32)] # -992 to 992

# North double wall (Y = -992 and Y = -960)
for x in xs:
    tree_coords.append((x, -992))
    tree_coords.append((x, -960))

# South double wall (Y = 992 and Y = 960)
for x in xs:
    tree_coords.append((x, 992))
    tree_coords.append((x, 960))

# West double wall (X = -992 and X = -960) for Y from -928 to 928
for y in range(-928, 960, 32):
    tree_coords.append((-992, y))
    tree_coords.append((-960, y))

# East double wall (X = 992 and X = 960) for Y from -928 to 928
for y in range(-928, 960, 32):
    tree_coords.append((992, y))
    tree_coords.append((960, y))

# Extra corner reinforcement trees
corner_extras = [
    (-928, -928), (-928, -960), (-960, -928),
    (928, -928), (928, -960), (960, -928),
    (-928, 928), (928, 928)
]
for c in corner_extras:
    tree_coords.append(c)

print(f"Generated {len(tree_coords)} perimeter tree positions.")

# 2. Update scenes/world.tscn with the new tree positions
with open('scenes/world.tscn', 'r', encoding='utf-8') as f:
    world_content = f.read()

tree_idx = 0
def replace_tree_pos(match):
    global tree_idx
    tname = match.group(1)
    if tree_idx < len(tree_coords):
        tx, ty = tree_coords[tree_idx]
        tree_idx += 1
        return f'[node name="{tname}" parent="Trees" unique_id={match.group(2)} instance=ExtResource("4_tree_scene")]\nposition = Vector2({tx}, {ty})'
    return match.group(0)

new_world_content = re.sub(
    r'\[node name="(Tree_\d+)" parent="Trees" unique_id=(\d+) instance=ExtResource\("4_tree_scene"\)\]\nposition = Vector2\([^)]+\)',
    replace_tree_pos,
    world_content
)

with open('scenes/world.tscn', 'w', encoding='utf-8') as f:
    f.write(new_world_content)

print(f"Updated {tree_idx} trees in scenes/world.tscn to outer map border!")

# 3. Update Camera2D limits in scenes/player.tscn to cover the full 2048x2048 map
with open('scenes/player.tscn', 'r', encoding='utf-8') as f:
    player_content = f.read()

player_content = re.sub(r'limit_left = -\d+', 'limit_left = -1024', player_content)
player_content = re.sub(r'limit_top = -\d+', 'limit_top = -1024', player_content)
player_content = re.sub(r'limit_right = \d+', 'limit_right = 1024', player_content)
player_content = re.sub(r'limit_bottom = \d+', 'limit_bottom = 1024', player_content)

with open('scenes/player.tscn', 'w', encoding='utf-8') as f:
    f.write(player_content)

print("Updated Camera2D limits in scenes/player.tscn to (-1024, -1024, 1024, 1024)!")
