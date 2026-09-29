import re

with open('scenes/world.tscn', 'r', encoding='utf-8') as f:
    content = f.read()

pts = []
for m in re.finditer(r'\[node name="(Tree_\d+)"[^\]]*\]\s*position = Vector2\(([^)]+)\)', content):
    name = m.group(1)
    coords = [float(x.strip()) for x in m.group(2).split(',')]
    pts.append((name, coords[0], coords[1]))

xs = [p[1] for p in pts]
ys = [p[2] for p in pts]

print(f"Total trees: {len(pts)}")
print(f"X bounds: min = {min(xs)}, max = {max(xs)}")
print(f"Y bounds: min = {min(ys)}, max = {max(ys)}")

# Let's inspect GrassField region_rect
grass_m = re.search(r'\[node name="GrassField"[^\]]*\][^\[]*region_rect = Rect2\(([^)]+)\)', content)
if grass_m:
    print(f"GrassField region_rect: Rect2({grass_m.group(1)})")
