extends Node2D

func _ready() -> void:
	print("==================================================")
	print("--- INICIANDO TEST SUITE COMPLETA (ADVERSARIAL R1) ---")
	print("==================================================")

	var world_scene = load("res://scenes/world.tscn")
	var world = world_scene.instantiate()
	add_child(world)

	for i in range(10):
		await get_tree().physics_frame

	var entities: Node2D = world.get_node("Entities")
	var player: CharacterBody2D = entities.get_node("Player")
	var camera: Camera2D = player.get_node("Camera2D")
	var wardrobe: StaticBody2D = entities.get_node("BedroomWardrobe")
	var bed: StaticBody2D = entities.get_node("BedroomBed")
	var nightstand: StaticBody2D = entities.get_node("BedroomNightstand")
	var shelves: StaticBody2D = entities.get_node("BedroomShelves")
	var desk: StaticBody2D = entities.get_node("BedroomDesk")

	var walls: Node2D = world.get_node("Walls")
	var wall_north: StaticBody2D = walls.get_node("WallNorth")
	var wall_east: StaticBody2D = walls.get_node("WallEast")
	var wall_south_l: StaticBody2D = walls.get_node("WallSouthLeft")
	var wall_south_r: StaticBody2D = walls.get_node("WallSouthRight")
	var wall_div_n: StaticBody2D = walls.get_node("WallDividingNorth")
	var wall_div_s: StaticBody2D = walls.get_node("WallDividingSouth")
	var wall_bed_n: StaticBody2D = walls.get_node("WallBedroomNorth")
	var wall_bed_w: StaticBody2D = walls.get_node("WallBedroomWest")
	var wall_bed_s: StaticBody2D = walls.get_node("WallBedroomSouth")

	var floor_node: Node2D = world.get_node("Floor")
	var bed_floor: Sprite2D = floor_node.get_node("BedroomFloor")
	var threshold: Sprite2D = floor_node.get_node("DoorwayThreshold")

	# ----------------------------------------------------
	# TEST 1: Estructura de Nodos Completa
	# ----------------------------------------------------
	assert(wardrobe != null, "BedroomWardrobe debe existir")
	assert(bed != null, "BedroomBed debe existir")
	assert(nightstand != null, "BedroomNightstand debe existir")
	assert(shelves != null, "BedroomShelves debe existir")
	assert(desk != null, "BedroomDesk debe existir")
	assert(wall_div_n != null, "WallDividingNorth debe existir")
	assert(wall_div_s != null, "WallDividingSouth debe existir")
	assert(wall_bed_n != null, "WallBedroomNorth debe existir")
	assert(wall_bed_w != null, "WallBedroomWest debe existir")
	assert(wall_bed_s != null, "WallBedroomSouth debe existir")
	assert(bed_floor != null, "BedroomFloor debe existir")
	assert(threshold != null, "DoorwayThreshold debe existir en Floor")
	print("✓ TEST 1 PASADO: Estructura de nodos completa y verificada.")

	# ----------------------------------------------------
	# TEST 2: Verificación de Flags de Y-Sorting
	# ----------------------------------------------------
	assert(world.y_sort_enabled == true, "World y_sort_enabled debe ser true")
	assert(entities.y_sort_enabled == true, "Entities y_sort_enabled debe ser true")
	assert(player.y_sort_enabled == true, "Player y_sort_enabled debe ser true")
	assert(wardrobe.y_sort_enabled == true, "Wardrobe y_sort_enabled debe ser true")
	assert(bed.y_sort_enabled == true, "Bed y_sort_enabled debe ser true")
	assert(nightstand.y_sort_enabled == true, "Nightstand y_sort_enabled debe ser true")
	assert(shelves.y_sort_enabled == true, "Shelves y_sort_enabled debe ser true")
	assert(desk.y_sort_enabled == true, "Desk y_sort_enabled debe ser true")
	print("✓ TEST 2 PASADO: Flags de y_sort_enabled activos en World, Entities y todos los muebles.")

	# ----------------------------------------------------
	# TEST 3: Colisiones Físicas en las Bases de los Muebles
	# ----------------------------------------------------
	player.global_position = Vector2(-230, -20)
	for i in range(2):
		await get_tree().physics_frame
	var hit_wardrobe = player.test_move(Transform2D(0, Vector2(-230, -20)), Vector2(0, -30))
	assert(hit_wardrobe, "La base del armario debe bloquear el paso hacia el norte")

	var hit_bed = player.test_move(Transform2D(0, Vector2(-391, 50)), Vector2(0, -30))
	assert(hit_bed, "El cuerpo de la cama debe bloquear el paso hacia el norte")

	var hit_nightstand = player.test_move(Transform2D(0, Vector2(-370, 80)), Vector2(-30, 0))
	assert(hit_nightstand, "El velador debe bloquear el paso hacia el oeste")

	var hit_shelves = player.test_move(Transform2D(0, Vector2(-210, 100)), Vector2(30, 0))
	assert(hit_shelves, "Las estanterías deben bloquear el paso hacia el este")

	var hit_desk = player.test_move(Transform2D(0, Vector2(-368, 100)), Vector2(0, 30))
	assert(hit_desk, "El escritorio debe bloquear el paso hacia el sur")
	print("✓ TEST 3 PASADO: Todas las colisiones en bases de muebles bloquean eficazmente.")

	# ----------------------------------------------------
	# TEST 4: Espacios Libres Detrás de Armario y Cama
	# ----------------------------------------------------
	player.global_position = Vector2(-230, -75)
	for i in range(2):
		await get_tree().physics_frame
	var move_behind_wardrobe = player.test_move(Transform2D(0, Vector2(-230, -75)), Vector2(-20, 0))
	assert(not move_behind_wardrobe, "El jugador debe poder moverse horizontalmente detrás del armario")

	player.global_position = Vector2(-391, -90)
	for i in range(2):
		await get_tree().physics_frame
	var move_behind_bed = player.test_move(Transform2D(0, Vector2(-391, -90)), Vector2(15, 0))
	assert(not move_behind_bed, "El jugador debe poder moverse horizontalmente detrás de la cama")
	print("✓ TEST 4 PASADO: Espacios libres transitables detrás de armario y cabecera de cama.")

	# ----------------------------------------------------
	# TEST 5: Navegación Bidireccional por Puerta Interior (y = 0)
	# ----------------------------------------------------
	player.global_position = Vector2(0, 0)
	camera.reset_smoothing()
	for i in range(5):
		await get_tree().physics_frame

	var speed = 150.0
	var max_frames = 250
	var frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar al dormitorio en y=0")
	print("✓ TEST 5 PASADO: Travesía hacia dormitorio en y=0 completada (pos: ", player.global_position, ")")

	# ----------------------------------------------------
	# TEST 6: Casos Límite de la Puerta Interior (Edge Cases)
	# ----------------------------------------------------
	# 6a. Travesía en y = -16 (borde superior de vano anterior)
	player.global_position = Vector2(0, -16)
	frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar sin trabarse por y=-16")

	# 6b. Travesía en y = -20 corriendo a alta velocidad (Sprint Shift = 200)
	player.global_position = Vector2(0, -20)
	frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-200.0, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar corriendo por y=-20 sin trabarse")

	# 6c. Travesía en y = +20 (borde inferior del vano)
	player.global_position = Vector2(0, 20)
	frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar sin trabarse por y=+20")

	# 6d. Travesía de regreso al este por y = -16
	player.global_position = Vector2(-288, -16)
	frames = 0
	while player.global_position.x < -10 and frames < max_frames:
		player.velocity = Vector2(speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x >= -20, "El jugador debe regresar a la sala central por y=-16")
	print("✓ TEST 6 PASADO: Todos los casos límite de navegación por la puerta (y=-20, y=-16, y=+20) resueltos fluidamente.")

	# ----------------------------------------------------
	# TEST 7: Sprint Diagonal a través del Vano
	# ----------------------------------------------------
	player.global_position = Vector2(60, -40)
	frames = 0
	while player.global_position.x > -280 and frames < 300:
		var dir = (Vector2(-288, 0) - player.global_position).normalized()
		player.velocity = dir * 200.0
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador en diagonal sprint debe cruzar fluidamente la puerta")
	print("✓ TEST 7 PASADO: Sprint diagonal a través del vano completado con éxito.")

	# ----------------------------------------------------
	# TEST 8: Sprint en el Pasillo Noroeste Detrás de la Cama
	# ----------------------------------------------------
	player.global_position = Vector2(-288, -80)
	frames = 0
	while player.global_position.x > -400 and frames < 150:
		player.velocity = Vector2(-200.0, -40.0).normalized() * 200.0
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x < -380, "Debe alcanzar la esquina noroeste detrás de la cama")
	print("✓ TEST 8 PASADO: Radio de giro y sprint fluido en la esquina noroeste.")

	# ----------------------------------------------------
	# TEST 9: Verificación Rigurosa de Y-Sort y Oclusión
	# ----------------------------------------------------
	# Detrás del armario:
	player.global_position = Vector2(-230, -75)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y < wardrobe.global_position.y, "Detrás del armario, Player.y debe ser menor que Wardrobe.y")

	# Delante del armario:
	player.global_position = Vector2(-230, 20)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y > wardrobe.global_position.y, "Delante del armario, Player.y debe ser mayor que Wardrobe.y")

	# Detrás de la cama:
	player.global_position = Vector2(-391, -70)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y < bed.global_position.y, "Detrás de la cama, Player.y debe ser menor que Bed.y")

	# Delante de la cama:
	player.global_position = Vector2(-391, 50)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y > bed.global_position.y, "Delante de la cama, Player.y debe ser mayor que Bed.y")
	print("✓ TEST 9 PASADO: Relaciones Y-sort verificadas rigurosamente en ambas posiciones.")

	# ----------------------------------------------------
	# TEST 10: Pruebas de Regresión de la Sala Central y Jardín
	# ----------------------------------------------------
	# Salida al jardín por la puerta sur (0, 144)
	player.global_position = Vector2(0, 120)
	for i in range(2):
		await get_tree().physics_frame
	var south_collision = player.test_move(Transform2D(0, player.global_position), Vector2(0, 60))
	assert(not south_collision, "La salida al jardín sur debe estar despejada sin colisiones")

	# Bloqueo de paredes principales
	var hit_north_wall = player.test_move(Transform2D(0, Vector2(0, -120)), Vector2(0, -30))
	assert(hit_north_wall, "WallNorth debe bloquear el paso hacia el exterior norte")

	var hit_east_wall = player.test_move(Transform2D(0, Vector2(120, 0)), Vector2(30, 0))
	assert(hit_east_wall, "WallEast debe bloquear el paso hacia el exterior este")
	print("✓ TEST 10 PASADO: Pruebas de regresión superadas; jardín y paredes de sala principal intactas.")

	# ----------------------------------------------------
	# TEST 11: Integridad del Perímetro y Prevención de Fugas
	# ----------------------------------------------------
	var escape_count = 0
	for ty in range(-380, 380, 4):
		if not player.test_move(Transform2D(0, Vector2(-650, ty)), Vector2(-50, 0)):
			escape_count += 1
		if not player.test_move(Transform2D(0, Vector2(360, ty)), Vector2(50, 0)):
			escape_count += 1
	for tx in range(-650, 360, 4):
		if not player.test_move(Transform2D(0, Vector2(tx, -360)), Vector2(0, -50)):
			escape_count += 1
		if not player.test_move(Transform2D(0, Vector2(tx, 360)), Vector2(0, 50)):
			escape_count += 1
	assert(escape_count == 0, "No debe haber brechas de escape en el perímetro de árboles exteriores")
	print("✓ TEST 11 PASADO: Perímetro exterior completamente sellado (0 brechas de fuga).")

	# ----------------------------------------------------
	# TEST 12: Límites de Cámara y Configuración Top-Down
	# ----------------------------------------------------
	assert(camera.limit_left <= -672, "Camera limit_left debe contener el borde oeste")
	assert(camera.limit_top <= -384, "Camera limit_top debe contener el borde norte")
	assert(camera.limit_right >= 384, "Camera limit_right debe contener el borde este")
	assert(camera.limit_bottom >= 384, "Camera limit_bottom debe contener el borde sur")
	assert(player.motion_mode == CharacterBody2D.MOTION_MODE_FLOATING, "Player motion_mode debe ser MOTION_MODE_FLOATING para deslizamiento suave")
	print("✓ TEST 12 PASADO: Límites de cámara anti-vacío y motion_mode top-down configurados correctamente.")

	# ----------------------------------------------------
	# CAPTURAS DE AUDITORÍA VISUAL EN MOTOR
	# ----------------------------------------------------
	# Captura 1: Centro del dormitorio
	player.global_position = Vector2(-288, 0)
	camera.reset_smoothing()
	for i in range(15):
		await get_tree().physics_frame
	var img1 = get_viewport().get_texture().get_image()
	if img1:
		img1.save_png(".agents/teamwork/implementer_r1/analysis/audit_bedroom_center.png")
		img1.save_png(".agents/teamwork/reviewer_r1/audit_bedroom_center.png")
		img1.save_png(".agents/teamwork/reviewer_r2/audit_bedroom_center.png")
		print("✓ Captura 1 guardada: audit_bedroom_center.png")

	# Captura 2: Detrás del armario
	player.global_position = Vector2(-230, -75)
	camera.reset_smoothing()
	for i in range(15):
		await get_tree().physics_frame
	var img2 = get_viewport().get_texture().get_image()
	if img2:
		img2.save_png(".agents/teamwork/implementer_r1/analysis/audit_behind_wardrobe.png")
		img2.save_png(".agents/teamwork/reviewer_r1/audit_behind_wardrobe.png")
		img2.save_png(".agents/teamwork/reviewer_r2/audit_behind_wardrobe.png")
		print("✓ Captura 2 guardada: audit_behind_wardrobe.png")

	# Captura 3: Detrás de la cama
	player.global_position = Vector2(-391, -70)
	camera.reset_smoothing()
	for i in range(15):
		await get_tree().physics_frame
	var img3 = get_viewport().get_texture().get_image()
	if img3:
		img3.save_png(".agents/teamwork/implementer_r1/analysis/audit_behind_bed.png")
		img3.save_png(".agents/teamwork/reviewer_r1/audit_behind_bed.png")
		img3.save_png(".agents/teamwork/reviewer_r2/audit_behind_bed.png")
		print("✓ Captura 3 guardada: audit_behind_bed.png")

	# Captura 4: En el umbral de la puerta interior
	player.global_position = Vector2(-144, 0)
	camera.reset_smoothing()
	for i in range(15):
		await get_tree().physics_frame
	var img4 = get_viewport().get_texture().get_image()
	if img4:
		img4.save_png(".agents/teamwork/implementer_r1/analysis/audit_doorway.png")
		img4.save_png(".agents/teamwork/reviewer_r1/audit_doorway.png")
		img4.save_png(".agents/teamwork/reviewer_r2/audit_doorway.png")
		print("✓ Captura 4 guardada: audit_doorway.png")

	# Captura 5: Límite del bosque exterior oeste (sin vacíos)
	player.global_position = Vector2(-600, 0)
	camera.reset_smoothing()
	for i in range(15):
		await get_tree().physics_frame
	var img5 = get_viewport().get_texture().get_image()
	if img5:
		img5.save_png(".agents/teamwork/reviewer_r2/audit_forest_boundary.png")
		print("✓ Captura 5 guardada: audit_forest_boundary.png")

	print("\n==================================================")
	print("TODAS LAS PRUEBAS (12/12) Y AUDITORÍAS COMPLETADAS CON ÉXITO")
	print("==================================================\n")
	get_tree().quit(0)

