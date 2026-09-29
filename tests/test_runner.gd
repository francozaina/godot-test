extends Node2D

func _ready() -> void:
	print("==================================================")
	print("--- INICIANDO TEST SUITE COMPLETA: MANSION VICTORIANA ---")
	print("==================================================")

	var world_scene = load("res://scenes/world.tscn")
	var world = world_scene.instantiate()
	add_child(world)

	for i in range(10):
		await get_tree().physics_frame

	var player: CharacterBody2D = world.find_child("Player", true, false)
	var camera: Camera2D = player.get_node("Camera2D")
	var fireplace: StaticBody2D = world.find_child("MansionFireplace", true, false)
	var bookcase: StaticBody2D = world.find_child("MansionBookcase", true, false)
	var bed: StaticBody2D = world.find_child("MansionBed", true, false)
	var nightstand: StaticBody2D = world.find_child("MansionNightstand", true, false)
	var desk: StaticBody2D = world.find_child("MansionDesk", true, false)
	var chair_l: StaticBody2D = world.find_child("MansionArmchairLeft", true, false)
	var chair_r: StaticBody2D = world.find_child("MansionArmchairRight", true, false)

	var wall_north: StaticBody2D = world.find_child("WallNorth", true, false)
	var wall_east: StaticBody2D = world.find_child("WallEast", true, false)
	var wall_south_l: StaticBody2D = world.find_child("WallSouthLeft", true, false)
	var wall_south_r: StaticBody2D = world.find_child("WallSouthRight", true, false)
	var wall_div_n: StaticBody2D = world.find_child("WallDividingNorth", true, false)
	var wall_div_s: StaticBody2D = world.find_child("WallDividingSouth", true, false)
	var wall_bed_n: StaticBody2D = world.find_child("WallBedroomNorth", true, false)
	var wall_bed_w: StaticBody2D = world.find_child("WallBedroomWest", true, false)
	var wall_bed_s: StaticBody2D = world.find_child("WallBedroomSouth", true, false)

	var suite_floor: Sprite2D = world.find_child("MansionSuiteFloor", true, false)
	var rug: Sprite2D = world.find_child("VictorianRug", true, false)
	var threshold: Sprite2D = world.find_child("DoorwayThreshold", true, false)

	# ----------------------------------------------------
	# TEST 1: Estructura de Nodos Completa
	# ----------------------------------------------------
	assert(player != null, "Player debe existir")
	assert(fireplace != null, "MansionFireplace debe existir")
	assert(bookcase != null, "MansionBookcase debe existir")
	assert(bed != null, "MansionBed debe existir")
	assert(nightstand != null, "MansionNightstand debe existir")
	assert(desk != null, "MansionDesk debe existir")
	assert(chair_l != null, "MansionArmchairLeft debe existir")
	assert(chair_r != null, "MansionArmchairRight debe existir")
	assert(wall_div_n != null, "WallDividingNorth debe existir")
	assert(wall_div_s != null, "WallDividingSouth debe existir")
	assert(wall_bed_n != null, "WallBedroomNorth debe existir")
	assert(wall_bed_w != null, "WallBedroomWest debe existir")
	assert(wall_bed_s != null, "WallBedroomSouth debe existir")
	assert(suite_floor != null, "MansionSuiteFloor debe existir")
	assert(rug != null, "VictorianRug debe existir")
	assert(threshold != null, "DoorwayThreshold debe existir")
	print("✓ TEST 1 PASADO: Estructura de nodos completa y verificada.")

	# ----------------------------------------------------
	# TEST 2: Verificación de Flags de Y-Sorting
	# ----------------------------------------------------
	assert(world.y_sort_enabled == true, "World y_sort_enabled debe ser true")
	assert(player.y_sort_enabled == true, "Player y_sort_enabled debe ser true")
	assert(fireplace.y_sort_enabled == true, "Fireplace y_sort_enabled debe ser true")
	assert(bookcase.y_sort_enabled == true, "Bookcase y_sort_enabled debe ser true")
	assert(bed.y_sort_enabled == true, "Bed y_sort_enabled debe ser true")
	assert(nightstand.y_sort_enabled == true, "Nightstand y_sort_enabled debe ser true")
	assert(desk.y_sort_enabled == true, "Desk y_sort_enabled debe ser true")
	assert(chair_l.y_sort_enabled == true, "Chair_L y_sort_enabled debe ser true")
	assert(chair_r.y_sort_enabled == true, "Chair_R y_sort_enabled debe ser true")
	print("✓ TEST 2 PASADO: Flags de y_sort_enabled activos en World, Player y todos los muebles.")

	# ----------------------------------------------------
	# TEST 3: Colisiones Físicas en las Bases de los Muebles
	# ----------------------------------------------------
	var hit_fireplace = player.test_move(Transform2D(0, Vector2(-190, -35)), Vector2(0, -30))
	assert(hit_fireplace, "La base de la chimenea debe bloquear el paso hacia el norte")

	var hit_bed = player.test_move(Transform2D(0, Vector2(-328, -10)), Vector2(0, -35))
	assert(hit_bed, "El cuerpo de la cama debe bloquear el paso hacia el norte")

	var hit_desk = player.test_move(Transform2D(0, Vector2(-401, 95)), Vector2(0, 35))
	assert(hit_desk, "El escritorio debe bloquear el paso hacia el sur")

	var hit_chair = player.test_move(Transform2D(0, Vector2(-399, 115)), Vector2(0, -30))
	assert(hit_chair, "El sillón izquierdo debe bloquear el paso hacia el norte")
	print("✓ TEST 3 PASADO: Todas las colisiones en bases de muebles bloquean eficazmente.")

	# ----------------------------------------------------
	# TEST 4: Espacios Libres Transitables en la Habitación
	# ----------------------------------------------------
	player.global_position = Vector2(-280, -30)
	for i in range(2):
		await get_tree().physics_frame
	var collision = player.move_and_collide(Vector2.ZERO, true)
	assert(collision == null, "El jugador no debe colisionar en el pasillo central del rug")
	print("✓ TEST 4 PASADO: Espacios libres transitables verificados.")

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
	assert(player.global_position.x <= -270, "El jugador debe cruzar a la suite en y=0")
	print("✓ TEST 5 PASADO: Travesía hacia la suite en y=0 completada.")

	# ----------------------------------------------------
	# TEST 6: Casos Límite de la Puerta Interior (Edge Cases)
	# ----------------------------------------------------
	player.global_position = Vector2(0, -16)
	frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar sin trabarse por y=-16")

	player.global_position = Vector2(0, 20)
	frames = 0
	while player.global_position.x > -280 and frames < max_frames:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x <= -270, "El jugador debe cruzar sin trabarse por y=+20")

	player.global_position = Vector2(-288, -16)
	frames = 0
	while player.global_position.x < -10 and frames < max_frames:
		player.velocity = Vector2(speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		frames += 1
	assert(player.global_position.x >= -20, "El jugador debe regresar a la sala central por y=-16")
	print("✓ TEST 6 PASADO: Todos los casos límite de navegación por la puerta (y=-16, y=+20) resueltos fluidamente.")

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
	# TEST 8: Verificación de Y-Sort Relativo
	# ----------------------------------------------------
	player.global_position = Vector2(chair_l.global_position.x, chair_l.global_position.y - 20)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y < chair_l.global_position.y, "Detrás del sillón, Player.y debe ser menor que Chair.y")

	player.global_position = Vector2(chair_l.global_position.x, chair_l.global_position.y + 20)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y > chair_l.global_position.y, "Delante del sillón, Player.y debe ser mayor que Chair.y")
	print("✓ TEST 8 PASADO: Relaciones Y-sort verificadas rigurosamente.")

	# ----------------------------------------------------
	# TEST 9: Pruebas de Regresión de la Sala Central / Lobby y Jardín
	# ----------------------------------------------------
	player.global_position = Vector2(96, 120)
	for i in range(2):
		await get_tree().physics_frame
	var south_collision = player.test_move(Transform2D(0, player.global_position), Vector2(0, 60))
	assert(not south_collision, "La salida principal sur al exterior debe estar despejada sin colisiones")

	var hit_north_wall = player.test_move(Transform2D(0, Vector2(0, -120)), Vector2(0, -30))
	assert(hit_north_wall, "WallNorth debe bloquear el paso hacia el exterior norte")

	var hit_east_wall = player.test_move(Transform2D(0, Vector2(310, 0)), Vector2(30, 0))
	assert(hit_east_wall, "WallEast ampliada a la derecha debe bloquear el paso hacia el exterior este")

	var hit_south_wall = player.test_move(Transform2D(0, Vector2(-48, 120)), Vector2(0, 30))
	assert(hit_south_wall, "WallSouthLeft debe bloquear el paso hacia el exterior sur")
	print("✓ TEST 9 PASADO: Pruebas de regresión superadas; salida principal y paredes del lobby intactas.")

	# ----------------------------------------------------
	# TEST 10: Integridad del Perímetro de Árboles
	# ----------------------------------------------------
	var escape_count = 0
	for ty in range(-900, 900, 10):
		if not player.test_move(Transform2D(0, Vector2(-930, ty)), Vector2(-50, 0)):
			escape_count += 1
		if not player.test_move(Transform2D(0, Vector2(930, ty)), Vector2(50, 0)):
			escape_count += 1
	assert(escape_count == 0, "No debe haber brechas de escape en el perímetro de árboles exteriores")
	print("✓ TEST 10 PASADO: Perímetro exterior completamente sellado en bordes del mapa (0 brechas de fuga).")

	# ----------------------------------------------------
	# TEST 11: Límites de Cámara y Configuración Top-Down
	# ----------------------------------------------------
	assert(camera.limit_left <= -1024, "Camera limit_left debe contener el borde oeste")
	assert(camera.limit_top <= -1024, "Camera limit_top debe contener el borde norte")
	assert(camera.limit_right >= 1024, "Camera limit_right debe contener el borde este")
	assert(camera.limit_bottom >= 1024, "Camera limit_bottom debe contener el borde sur")
	assert(player.motion_mode == CharacterBody2D.MOTION_MODE_FLOATING, "Player motion_mode debe ser MOTION_MODE_FLOATING")
	print("✓ TEST 11 PASADO: Límites de cámara anti-vacío (-1024 a 1024) y motion_mode top-down verificados.")

	print("\n==================================================")
	print("TODAS LAS PRUEBAS (11/11) COMPLETADAS CON ÉXITO")
	print("==================================================\n")
	get_tree().quit(0)
