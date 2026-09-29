extends StaticBody2D

@onready var light: PointLight2D = $PointLight2D
var _time: float = 0.0

func _process(delta: float) -> void:
	_time += delta * 8.0
	if light:
		light.energy = 0.85 + 0.15 * sin(_time) + 0.05 * sin(_time * 2.7)
