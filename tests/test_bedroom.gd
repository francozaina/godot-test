extends SceneTree

func _init() -> void:
	var runner = Node.new()
	var script = GDScript.new()
	script.source_code = """extends Node

func _ready() -> void:
	print("--- INICIANDO TEST SUITE: SUITE / ESTUDIO VICTORIANO ---")
	var world_scene: PackedScene = load("res://scenes/world.tscn")
	if not world_scene:
		printerr("ERROR: No se pudo cargar scenes/world.tscn")
		get_tree().quit(1)
		return

	var world: Node2D = world_scene.instantiate()
	add_child(world)

	for i in range(10):
		await get_tree().physics_frame

	var entities: Node2D = world.get_node("Entities")
	var player: CharacterBody2D = entities.get_node("Player")
	var fireplace: StaticBody2D = entities.get_node("MansionFireplace")
	var bookcase: StaticBody2D = entities.get_node("MansionBookcase")
	var bed: StaticBody2D = entities.get_node("MansionBed")
	var nightstand: StaticBody2D = entities.get_node("MansionNightstand")
	var desk: StaticBody2D = entities.get_node("MansionDesk")
	var chair_l: StaticBody2D = entities.get_node("MansionArmchairLeft")
	var chair_r: StaticBody2D = entities.get_node("MansionArmchairRight")

	var walls: Node2D = world.get_node("Walls")
	var wall_div_n: StaticBody2D = walls.get_node("WallDividingNorth")
	var wall_div_s: StaticBody2D = walls.get_node("WallDividingSouth")
	var wall_bed_n: StaticBody2D = walls.get_node("WallBedroomNorth")
	var wall_bed_w: StaticBody2D = walls.get_node("WallBedroomWest")
	var wall_bed_s: StaticBody2D = walls.get_node("WallBedroomSouth")

	var floor_node: Node2D = world.get_node("Floor")
	var suite_floor: Sprite2D = floor_node.get_node("MansionSuiteFloor")
	var rug: Sprite2D = floor_node.get_node("VictorianRug")
	var threshold: Sprite2D = floor_node.get_node("DoorwayThreshold")

	# TEST 1: Verificación de Existencia de Nodos de Arte y Escena
	assert(fireplace != null, "Fireplace no encontrado")
	assert(bookcase != null, "Bookcase no encontrado")
	assert(bed != null, "Bed no encontrado")
	assert(nightstand != null, "Nightstand no encontrado")
	assert(desk != null, "Desk no encontrado")
	assert(chair_l != null, "ArmchairLeft no encontrado")
	assert(chair_r != null, "ArmchairRight no encontrado")
	assert(wall_div_n != null, "WallDividingNorth no encontrado")
	assert(wall_div_s != null, "WallDividingSouth no encontrado")
	assert(wall_bed_n != null, "WallBedroomNorth no encontrado")
	assert(wall_bed_w != null, "WallBedroomWest no encontrado")
	assert(wall_bed_s != null, "WallBedroomSouth no encontrado")
	assert(suite_floor != null, "MansionSuiteFloor no encontrado")
	assert(rug != null, "VictorianRug no encontrado")
	assert(threshold != null, "DoorwayThreshold no encontrado")
	print("✓ TEST 1 PASADO: Todos los muebles victorianos, paredes, alfombra y umbral existen.")

	# TEST 2: Verificación de Y-Sorting
	assert(world.y_sort_enabled == true, "World y_sort_enabled debe ser true")
	assert(entities.y_sort_enabled == true, "Entities y_sort_enabled debe ser true")
	assert(player.y_sort_enabled == true, "Player y_sort_enabled debe ser true")
	assert(fireplace.y_sort_enabled == true, "Fireplace y_sort_enabled debe ser true")
	assert(bookcase.y_sort_enabled == true, "Bookcase y_sort_enabled debe ser true")
	assert(bed.y_sort_enabled == true, "Bed y_sort_enabled debe ser true")
	assert(nightstand.y_sort_enabled == true, "Nightstand y_sort_enabled debe ser true")
	assert(desk.y_sort_enabled == true, "Desk y_sort_enabled debe ser true")
	assert(chair_l.y_sort_enabled == true, "ArmchairLeft y_sort_enabled debe ser true")
	assert(chair_r.y_sort_enabled == true, "ArmchairRight y_sort_enabled debe ser true")
	print("✓ TEST 2 PASADO: y_sort_enabled activo en World, Entities y todos los elementos.")

	# TEST 3: Colisiones de Muebles
	# Test colisión chimenea
	var test_fireplace = player.test_move(Transform2D(0, Vector2(-280, -90)), Vector2(0, -30))
	assert(test_fireplace, "La chimenea debe bloquear al jugador en su base")

	# Test colisión cama
	var test_bed = player.test_move(Transform2D(0, Vector2(-372, 100)), Vector2(0, -35))
	assert(test_bed, "La cama victoriana debe bloquear al jugador")

	# Test colisión escritorio
	var test_desk = player.test_move(Transform2D(0, Vector2(-200, 100)), Vector2(0, -35))
	assert(test_desk, "El escritorio de estudio debe bloquear al jugador")

	# Test colisión sillón
	var test_chair = player.test_move(Transform2D(0, Vector2(-320, -10)), Vector2(0, -30))
	assert(test_chair, "El sillón debe bloquear al jugador")
	print("✓ TEST 3 PASADO: Las colisiones físicas en las bases de los muebles bloquean correctamente.")

	# TEST 4: Navegación Fluida por la Puerta
	player.global_position = Vector2(0, 0)
	var speed = 160.0
	var max_steps = 300
	var steps_taken = 0
	while player.global_position.x > -288 and steps_taken < max_steps:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		steps_taken += 1
	assert(player.global_position.x <= -270, "El jugador debió cruzar la puerta hasta la suite victoriana")

	steps_taken = 0
	while player.global_position.x < 0 and steps_taken < max_steps:
		player.velocity = Vector2(speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		steps_taken += 1
	assert(player.global_position.x >= -10, "El jugador debió cruzar la puerta de regreso a la sala principal")
	print("✓ TEST 4 PASADO: Navegación a través de la puerta fluida en ambos sentidos.")

	# TEST 5: Y-Sort Relativo con Sillón
	player.global_position = Vector2(-320, -60)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y < chair_l.global_position.y, "Detrás del sillón, Player.y debe ser menor")

	player.global_position = Vector2(-320, -10)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y > chair_l.global_position.y, "Delante del sillón, Player.y debe ser mayor")
	print("✓ TEST 5 PASADO: Y-Sorting visual delante y detrás de los objetos comprobado.")

	print(\"\\n==============================================\")
	print(\"TODOS LOS TESTS DE INTEGRACIÓN PASARON EXITOSAMENTE (5/5)\")
	print(\"==============================================\\n\")
	get_tree().quit(0)
"""
	script.reload()
	runner.set_script(script)
	root.call_deferred("add_child", runner)
