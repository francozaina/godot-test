extends SceneTree

func _init() -> void:
	var runner = Node.new()
	var script = GDScript.new()
	script.source_code = """extends Node

func _ready() -> void:
	print("--- VERIFICANDO ESCENA PRINCIPAL Y REGRESIONES ---")
	var world_scene = load("res://scenes/world.tscn")
	var world = world_scene.instantiate()
	add_child(world)

	for i in range(10):
		await get_tree().physics_frame

	var entities = world.get_node("Entities")
	var player = entities.get_node("Player")
	assert(player.position == Vector2(0, 0), "El jugador debe iniciar en (0, 0)")

	# Verificar paredes principales
	var walls = world.get_node("Walls")
	assert(walls.get_node("WallNorth") != null)
	assert(walls.get_node("WallEast") != null)
	assert(walls.get_node("WallSouthLeft") != null)
	assert(walls.get_node("WallSouthRight") != null)
	assert(walls.get_node("WallDividingNorth") != null)
	assert(walls.get_node("WallDividingSouth") != null)

	# Salida al jardín por la puerta sur (0, 144)
	# Apertura sur está entre -32 y 32. El jugador en x=0 camina hacia y=200
	player.global_position = Vector2(0, 120)
	for i in range(2):
		await get_tree().physics_frame
	var collision = player.test_move(Transform2D(0, player.global_position), Vector2(0, 60))
	assert(not collision, "El jugador debe poder salir al jardín por la puerta sur sin trabarse")
	print("✓ Verificación de salida al jardín sur: OK")

	print("✓ Verificación de regresión: Escena intacta y funcional.")
	get_tree().quit(0)
"""
	script.reload()
	runner.set_script(script)
	root.call_deferred("add_child", runner)
