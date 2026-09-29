import re

with open('scenes/world.tscn', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update/Add ExtResources
new_ext_resources = """[ext_resource type="Texture2D" path="res://assets/central_room/wall_lobby.png" id="18_wall_lobby"]
[ext_resource type="Texture2D" path="res://assets/central_room/lobby_rug.png" id="19_lobby_rug"]
[ext_resource type="PackedScene" path="res://scenes/central_room/grandfather_clock.tscn" id="20_clock_scene"]
[ext_resource type="PackedScene" path="res://scenes/central_room/hall_console_table.tscn" id="21_console_scene"]
[ext_resource type="PackedScene" path="res://scenes/central_room/coat_rack.tscn" id="22_coatrack_scene"]
[ext_resource type="PackedScene" path="res://scenes/central_room/lobby_settee.tscn" id="23_settee_scene"]
[ext_resource type="PackedScene" path="res://scenes/central_room/statue_pedestal.tscn" id="24_pedestal_scene"]
"""

if 'id="18_wall_lobby"' not in content:
    content = content.replace(
        '[ext_resource type="PackedScene" path="res://scenes/mansion/armchair.tscn" id="17_armchair_scene"]\n',
        '[ext_resource type="PackedScene" path="res://scenes/mansion/armchair.tscn" id="17_armchair_scene"]\n' + new_ext_resources
    )

# 2. Update/Add SubResources for lobby wall collision shapes
new_sub_resources = """[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_lobby_n"]
size = Vector2(512, 32)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_lobby_s"]
size = Vector2(224, 32)

"""

if 'RectangleShape2D_wall_lobby_n' not in content:
    content = content.replace(
        '[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_h"]',
        new_sub_resources + '[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_h"]'
    )

# 3. New CentralRoom Section
new_central_room = """[node name="CentralRoom" type="Node2D" parent="." unique_id=1291725721]
y_sort_enabled = true

[node name="Floor" type="Node2D" parent="CentralRoom" unique_id=393135299]
z_index = -1

[node name="MansionRoomFloor" type="Sprite2D" parent="CentralRoom/Floor" unique_id=956366044]
texture_filter = 1
texture_repeat = 2
position = Vector2(96, 0)
texture = ExtResource("2_wood")
region_enabled = true
region_rect = Rect2(-256, -160, 512, 320)

[node name="LobbyRug" type="Sprite2D" parent="CentralRoom/Floor" unique_id=956366045]
texture_filter = 1
position = Vector2(96, 6)
texture = ExtResource("19_lobby_rug")

[node name="EntranceThreshold" type="Sprite2D" parent="CentralRoom/Floor" unique_id=956366046]
texture_filter = 1
position = Vector2(96, 144)
scale = Vector2(2, 0.444)
texture = ExtResource("8_threshold")

[node name="Walls" type="Node2D" parent="CentralRoom" unique_id=1291725723]

[node name="WallNorth" type="StaticBody2D" parent="CentralRoom/Walls" unique_id=1821737748]
position = Vector2(96, -144)

[node name="Sprite2D" type="Sprite2D" parent="CentralRoom/Walls/WallNorth" unique_id=1198503647]
texture_filter = 1
texture_repeat = 2
position = Vector2(0, -8)
texture = ExtResource("18_wall_lobby")
region_enabled = true
region_rect = Rect2(0, 0, 512, 48)

[node name="CollisionShape2D" type="CollisionShape2D" parent="CentralRoom/Walls/WallNorth" unique_id=1662387455]
shape = SubResource("RectangleShape2D_wall_lobby_n")

[node name="WallEast" type="StaticBody2D" parent="CentralRoom/Walls" unique_id=823610046]
position = Vector2(336, 0)

[node name="Sprite2D" type="Sprite2D" parent="CentralRoom/Walls/WallEast" unique_id=257972486]
texture_filter = 1
texture_repeat = 2
texture = ExtResource("18_wall_lobby")
region_enabled = true
region_rect = Rect2(0, 0, 32, 256)

[node name="CollisionShape2D" type="CollisionShape2D" parent="CentralRoom/Walls/WallEast" unique_id=1111622326]
shape = SubResource("RectangleShape2D_wall_v")

[node name="WallSouthLeft" type="StaticBody2D" parent="CentralRoom/Walls" unique_id=409425926]
position = Vector2(-48, 144)

[node name="Sprite2D" type="Sprite2D" parent="CentralRoom/Walls/WallSouthLeft" unique_id=950733935]
texture_filter = 1
texture_repeat = 2
texture = ExtResource("18_wall_lobby")
region_enabled = true
region_rect = Rect2(0, 0, 224, 32)

[node name="CollisionShape2D" type="CollisionShape2D" parent="CentralRoom/Walls/WallSouthLeft" unique_id=242128855]
shape = SubResource("RectangleShape2D_wall_lobby_s")

[node name="WallSouthRight" type="StaticBody2D" parent="CentralRoom/Walls" unique_id=1195014382]
position = Vector2(240, 144)

[node name="Sprite2D" type="Sprite2D" parent="CentralRoom/Walls/WallSouthRight" unique_id=1112187860]
texture_filter = 1
texture_repeat = 2
texture = ExtResource("18_wall_lobby")
region_enabled = true
region_rect = Rect2(0, 0, 224, 32)

[node name="CollisionShape2D" type="CollisionShape2D" parent="CentralRoom/Walls/WallSouthRight" unique_id=350598223]
shape = SubResource("RectangleShape2D_wall_lobby_s")

[node name="Furniture" type="Node2D" parent="CentralRoom" unique_id=1291725726]
y_sort_enabled = true

[node name="LobbyClock" parent="CentralRoom/Furniture" unique_id=2001001 instance=ExtResource("20_clock_scene")]
position = Vector2(20, -120)

[node name="LobbyConsole" parent="CentralRoom/Furniture" unique_id=2001002 instance=ExtResource("21_console_scene")]
position = Vector2(96, -120)

[node name="LobbyStatueRight" parent="CentralRoom/Furniture" unique_id=2001003 instance=ExtResource("24_pedestal_scene")]
position = Vector2(172, -120)

[node name="LobbyStatueLeft" parent="CentralRoom/Furniture" unique_id=2001004 instance=ExtResource("24_pedestal_scene")]
position = Vector2(-90, -120)

[node name="LobbyCoatRack" parent="CentralRoom/Furniture" unique_id=2001005 instance=ExtResource("22_coatrack_scene")]
position = Vector2(144, 120)

[node name="LobbySettee" parent="CentralRoom/Furniture" unique_id=2001006 instance=ExtResource("23_settee_scene")]
position = Vector2(260, 0)
"""

# Replace the old CentralRoom block
pattern = r'\[node name="CentralRoom" type="Node2D" parent="\." unique_id=1291725721\].*?(?=\[node name="VictorianRoom")'
content = re.sub(pattern, new_central_room + '\n', content, flags=re.DOTALL)

with open('scenes/world.tscn', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Central Room into grand Victorian Lobby in scenes/world.tscn!")
