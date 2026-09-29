extends CharacterBody2D

## Velocidad de movimiento normal (caminar)
@export var walk_speed: float = 120.0
## Velocidad de movimiento al correr (manteniendo Shift)
@export var run_speed: float = 200.0
## Si es verdadero, el movimiento es casilla por casilla (como Pokémon original)
## Si es falso, el movimiento es continuo libre y suave con WASD
@export var grid_movement: bool = false
## Tamaño de la cuadrícula en píxeles si grid_movement está activado
@export var tile_size: int = 32

@onready var sprite: Sprite2D = $Sprite2D
@onready var camera: Camera2D = $Camera2D

enum Direction { DOWN, UP, LEFT, RIGHT }
var current_dir: Direction = Direction.DOWN

var anim_timer: float = 0.0

# Variables para modo cuadrícula (Grid-based Pokémon style)
var is_grid_stepping: bool = false
var grid_target_pos: Vector2 = Vector2.ZERO

func _ready() -> void:
	update_sprite_frame(Direction.DOWN, 0)

func _physics_process(delta: float) -> void:
	if grid_movement:
		_process_grid_movement(delta)
	else:
		_process_smooth_movement(delta)

func _get_input_vector() -> Vector2:
	var dir := Vector2.ZERO
	if Input.is_action_pressed("move_right") or Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		dir.x += 1.0
	if Input.is_action_pressed("move_left") or Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		dir.x -= 1.0
	if Input.is_action_pressed("move_down") or Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		dir.y += 1.0
	if Input.is_action_pressed("move_up") or Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		dir.y -= 1.0
	return dir

func _process_smooth_movement(delta: float) -> void:
	var input_vec = _get_input_vector()
	var is_running = Input.is_action_pressed("sprint") or Input.is_key_pressed(KEY_SHIFT)
	var speed = run_speed if is_running else walk_speed

	if input_vec != Vector2.ZERO:
		# Determinar orientación según el eje principal (estilo Pokémon)
		if abs(input_vec.x) > abs(input_vec.y):
			current_dir = Direction.RIGHT if input_vec.x > 0 else Direction.LEFT
		elif input_vec.y != 0:
			current_dir = Direction.DOWN if input_vec.y > 0 else Direction.UP

		# Movimiento normalizado
		velocity = input_vec.normalized() * speed

		# Animación de pasos (1: pie izq, 0: quieto, 2: pie der)
		anim_timer += delta * (10.0 if is_running else 6.0)
		var cycle = int(anim_timer) % 4
		var step_idx = 0
		if cycle == 0:
			step_idx = 1
		elif cycle == 2:
			step_idx = 2
		else:
			step_idx = 0
		update_sprite_frame(current_dir, step_idx)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, speed * delta * 15.0)
		anim_timer = 0.0
		update_sprite_frame(current_dir, 0)

	move_and_slide()

func _process_grid_movement(delta: float) -> void:
	var is_running = Input.is_action_pressed("sprint") or Input.is_key_pressed(KEY_SHIFT)
	var speed = run_speed if is_running else walk_speed

	if is_grid_stepping:
		global_position = global_position.move_toward(grid_target_pos, speed * delta)
		anim_timer += delta * (12.0 if is_running else 8.0)
		var step_idx = (int(anim_timer) % 2) + 1
		update_sprite_frame(current_dir, step_idx)

		if global_position.distance_to(grid_target_pos) < 1.0:
			global_position = grid_target_pos
			is_grid_stepping = false
			update_sprite_frame(current_dir, 0)
	else:
		var input_vec = _get_input_vector()
		if input_vec != Vector2.ZERO:
			var move_dir = Vector2.ZERO
			if abs(input_vec.x) >= abs(input_vec.y):
				move_dir = Vector2(sign(input_vec.x), 0)
				current_dir = Direction.RIGHT if move_dir.x > 0 else Direction.LEFT
			else:
				move_dir = Vector2(0, sign(input_vec.y))
				current_dir = Direction.DOWN if move_dir.y > 0 else Direction.UP

			var target = global_position + move_dir * tile_size
			var test_transform = Transform2D(0, global_position)
			if not test_move(test_transform, move_dir * tile_size):
				grid_target_pos = target
				is_grid_stepping = true
				anim_timer = 0.0
			else:
				update_sprite_frame(current_dir, 0)
		else:
			update_sprite_frame(current_dir, 0)

func update_sprite_frame(dir: Direction, step: int) -> void:
	# Fila 0: DOWN, Fila 1: UP, Fila 2: LEFT, Fila 3: RIGHT
	# Columna 0: Idle, 1: Walk1, 2: Walk2
	sprite.frame = int(dir) * 3 + step
