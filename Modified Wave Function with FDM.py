import turtle as t
from time import sleep

# Constants
dim = (1000, 800)
padding = (20, 0)
default_water_level = 300
dx = 2
dt = 0.001
wave_speed = 120
damping = 10
spring = 0.4
wave_coef = pow(wave_speed, 2) * pow(dt, 2) / pow(dx, 2)
damping_coef = -damping * dt
spring_coef = -spring * dt
droplet_mass = 0.1
resistance = 0.5
gravity = -10000
gravity_term = gravity * pow(dt, 2)
resistance_coef = resistance / (2 * droplet_mass)
dropping_coef = pow(1 + resistance_coef * dt, -1)
alpha = 0

# Global State
prev_water_level = [default_water_level for _ in range(dim[0] // dx)]
curr_water_level = [default_water_level for _ in range(dim[0] // dx)]
water_dots: list[dict[str, float]] = []
outer_force_index = -1


def apply_gravity_to_water_dots():
    removals = []
    for water_dot in water_dots:
        tmp = water_dot["curr_y"]
        water_dot["curr_y"] = dropping_coef * (2 * water_dot["curr_y"] - water_dot["prev_y"] + gravity_term + resistance_coef * water_dot["prev_y"] * dt)
        water_dot["prev_y"] = tmp
        if water_dot["curr_y"] < curr_water_level[int(water_dot["curr_x"] / dx)]:
            removals.append(water_dot)
            water_dot_velocity_power = pow(water_dot["prev_y"] - water_dot["curr_y"], 2)
            update_wave(int(water_dot["curr_x"] / dx), -1400000 * water_dot_velocity_power)
    for removal in removals:
        water_dots.remove(removal)


def update_wave(force_index: int = -1, force_coef: float = 0):
    # left end; \partial u / \partial x is considered to be 0
    for i in range(len(curr_water_level)):
        if (i == force_index):
            _update_at_middle(i, force_coef)
        else:
            _update_at_middle(i, 0)


def _update_at_middle(index: int, force_coef: float):
    global wave_coef, damping_coef, curr_water_level, prev_water_level, default_water_level
    curr = curr_water_level[index]
    prev = prev_water_level[index]
    outer_force = force_coef * pow(dt, 2)
    if index == 0:
        wave_term = curr_water_level[2] - 2 * curr_water_level[1] + curr_water_level[0]
    elif index == len(curr_water_level) - 1:
        wave_term = curr_water_level[-3] - 2 * curr_water_level[-2] + curr_water_level[-1]
    else:
        wave_term = curr_water_level[index + 1] - 2 * curr + curr_water_level[index - 1]
    curr_water_level[index] = alpha * curr_water_level[index] + (1 - alpha) * (2 * curr - prev +  wave_coef * wave_term +\
        damping_coef * (curr - prev) + spring_coef * (curr - default_water_level) + outer_force)
    prev_water_level[index] = curr


def render_wave():
    global dx, curr_water_level
    t.pu()
    t.goto(0, curr_water_level[0])
    t.pd()
    t.pensize(1.2)
    for i in range(1, len(curr_water_level)):
        t.goto(dx * i, curr_water_level[i])
    t.pu()


def render_drops():
    global water_dots
    t.pensize(1)
    for water_dot in water_dots:
        t.pu()
        t.goto(water_dot["curr_x"], water_dot["curr_y"])
        t.pd()
        t.circle(2)
        t.pu()


def simulation_loop():
    global dt, outer_force_index
    t.clear()
    update_wave()
    apply_gravity_to_water_dots()
    if outer_force_index != -1:
        outer_force_index = -1
    render_wave()
    render_drops()
    t.ontimer(simulation_loop, int(dt * 1000))


def drop_water_dot(x, y):
    global water_dots, curr_water_level
    if (x // dx < 0 or x // dx > len(curr_water_level)):
        return
    water_dots.append({"curr_x": x, "curr_y": y, "prev_y": y})


if __name__ == "__main__":
    t.tracer(0, 0)
    t.setup(dim[0] - 2 * padding[0], dim[1] - 2 * padding[1])
    t.setworldcoordinates(padding[0], padding[1], dim[0] - padding[0], dim[1] - padding[1])
    simulation_loop()
    t.onscreenclick(drop_water_dot)
    t.mainloop()