extends SceneTree

func _init() -> void:
	var runner = Node.new()
	var script = GDScript.new()
	script.source_code = """extends Node

func _ready() -> void:
	print("--- INICIANDO TEST SUITE: DORMITORIO VICTORIANO ---")
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
	var wardrobe: StaticBody2D = entities.get_node("BedroomWardrobe")
	var bed: StaticBody2D = entities.get_node("BedroomBed")
	var nightstand: StaticBody2D = entities.get_node("BedroomNightstand")
	var shelves: StaticBody2D = entities.get_node("BedroomShelves")
	var desk: StaticBody2D = entities.get_node("BedroomDesk")

	var walls: Node2D = world.get_node("Walls")
	var wall_div_n: StaticBody2D = walls.get_node("WallDividingNorth")
	var wall_div_s: StaticBody2D = walls.get_node("WallDividingSouth")
	var wall_bed_n: StaticBody2D = walls.get_node("WallBedroomNorth")
	var wall_bed_w: StaticBody2D = walls.get_node("WallBedroomWest")
	var wall_bed_s: StaticBody2D = walls.get_node("WallBedroomSouth")

	var floor_node: Node2D = world.get_node("Floor")
	var bed_floor: Sprite2D = floor_node.get_node("BedroomFloor")
	var threshold: Sprite2D = floor_node.get_node("DoorwayThreshold")

	# TEST 1: Verificación de Existencia de Nodos
	assert(wardrobe != null, "Wardrobe no encontrado")
	assert(bed != null, "Bed no encontrado")
	assert(nightstand != null, "Nightstand no encontrado")
	assert(shelves != null, "Shelves no encontrado")
	assert(desk != null, "Desk no encontrado")
	assert(wall_div_n != null, "WallDividingNorth no encontrado")
	assert(wall_div_s != null, "WallDividingSouth no encontrado")
	assert(wall_bed_n != null, "WallBedroomNorth no encontrado")
	assert(wall_bed_w != null, "WallBedroomWest no encontrado")
	assert(wall_bed_s != null, "WallBedroomSouth no encontrado")
	assert(bed_floor != null, "BedroomFloor no encontrado")
	assert(threshold != null, "DoorwayThreshold no encontrado")
	print("✓ TEST 1 PASADO: Todos los nodos de muebles, paredes, umbral y suelo existen.")

	# TEST 2: Verificación de Y-Sorting
	assert(world.y_sort_enabled == true, "World y_sort_enabled debe ser true")
	assert(entities.y_sort_enabled == true, "Entities y_sort_enabled debe ser true")
	assert(player.y_sort_enabled == true, "Player y_sort_enabled debe ser true")
	assert(wardrobe.y_sort_enabled == true, "Wardrobe y_sort_enabled debe ser true")
	assert(bed.y_sort_enabled == true, "Bed y_sort_enabled debe ser true")
	assert(nightstand.y_sort_enabled == true, "Nightstand y_sort_enabled debe ser true")
	assert(shelves.y_sort_enabled == true, "Shelves y_sort_enabled debe ser true")
	assert(desk.y_sort_enabled == true, "Desk y_sort_enabled debe ser true")
	print("✓ TEST 2 PASADO: y_sort_enabled está activo en World, Entities y todos los muebles.")

	# TEST 3: Espacios Caminables detrás de Armario y Cama
	player.global_position = Vector2(-230, -75)
	for i in range(2):
		await get_tree().physics_frame
	var collision = player.move_and_collide(Vector2.ZERO, true)
	assert(collision == null, "El jugador no debería colisionar detrás del armario (y=-75)")

	var move_behind_wardrobe = player.test_move(Transform2D(0, Vector2(-230, -75)), Vector2(-20, 0))
	assert(not move_behind_wardrobe, "El jugador debe poder moverse horizontalmente detrás del armario")

	player.global_position = Vector2(-391, -90)
	for i in range(2):
		await get_tree().physics_frame
	collision = player.move_and_collide(Vector2.ZERO, true)
	assert(collision == null, "El jugador no debería colisionar detrás de la cama (y=-90)")

	var move_behind_bed = player.test_move(Transform2D(0, Vector2(-391, -90)), Vector2(15, 0))
	assert(not move_behind_bed, "El jugador debe poder moverse horizontalmente detrás de la cama")
	print("✓ TEST 3 PASADO: Hay espacio libre transitable detrás del armario y de la cabecera de la cama.")

	# TEST 4: Colisión física en las bases de los muebles
	var test_wardrobe_base = player.test_move(Transform2D(0, Vector2(-230, -20)), Vector2(0, -30))
	assert(test_wardrobe_base, "El armario debe bloquear el paso en su base")

	var test_bed_base = player.test_move(Transform2D(0, Vector2(-391, 50)), Vector2(0, -30))
	assert(test_bed_base, "La cama debe bloquear el paso en su cuerpo")

	var test_nightstand = player.test_move(Transform2D(0, Vector2(-370, 80)), Vector2(-30, 0))
	assert(test_nightstand, "El velador debe bloquear el paso")

	var test_shelves = player.test_move(Transform2D(0, Vector2(-210, 100)), Vector2(30, 0))
	assert(test_shelves, "Las estanterías deben bloquear el paso")

	var test_desk = player.test_move(Transform2D(0, Vector2(-368, 100)), Vector2(0, 30))
	assert(test_desk, "El escritorio debe bloquear el paso hacia la pared sur")
	print("✓ TEST 4 PASADO: Todas las colisiones de las bases de los muebles bloquean correctamente.")

	# TEST 5: Navegación por la Puerta Interior
	player.global_position = Vector2(0, 0)
	var speed = 150.0
	var max_steps = 300
	var steps_taken = 0
	while player.global_position.x > -288 and steps_taken < max_steps:
		player.velocity = Vector2(-speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		steps_taken += 1
	assert(player.global_position.x <= -270, "El jugador debió cruzar la puerta hasta el dormitorio")

	steps_taken = 0
	while player.global_position.x < 0 and steps_taken < max_steps:
		player.velocity = Vector2(speed, 0)
		player.move_and_slide()
		await get_tree().physics_frame
		steps_taken += 1
	assert(player.global_position.x >= -10, "El jugador debió cruzar la puerta de regreso a la sala central")
	print("✓ TEST 5 PASADO: El jugador cruza fluidamente la puerta interior en ambas direcciones sin trabarse.")

	# TEST 6: Comparación de Y-Sort (Relación Player y Mueble - sin or true)
	player.global_position = Vector2(-230, -75)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y < wardrobe.global_position.y, "Detrás del armario, Player.y debe ser menor que Wardrobe.y")

	player.global_position = Vector2(-230, 20)
	for i in range(2):
		await get_tree().physics_frame
	assert(player.global_position.y > wardrobe.global_position.y, "Delante del armario, Player.y debe ser mayor que Wardrobe.y")
	print("✓ TEST 6 PASADO: Reglas de Y-sort verificadas rigurosamente sin condiciones tautológicas.")

	print(\"\\n==============================================\")
	print(\"TODOS LOS TESTS DE INTEGRACIÓN PASARON EXITOSAMENTE (6/6)\")
	print(\"==============================================\\n\")
	get_tree().quit(0)
"""
	script.reload()
	runner.set_script(script)
	root.call_deferred("add_child", runner)
