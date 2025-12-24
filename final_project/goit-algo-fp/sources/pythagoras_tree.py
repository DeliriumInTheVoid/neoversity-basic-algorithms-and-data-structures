import math
import turtle
from typing import Literal, Tuple

TreeType = Literal["squares", "binary"]


def init_screen(title: str = "Pythagoras Trees (Turtle)", bg: str = "white") -> Tuple[turtle.Screen, turtle.Turtle]:
    screen = turtle.Screen()
    screen.title(title)
    screen.bgcolor(bg)
    screen.tracer(0, 0)

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pensize(1)

    return screen, t


def _update_bounds(bounds, points):
    minx, maxx, miny, maxy = bounds
    for px, py in points:
        minx = min(minx, px)
        maxx = max(maxx, px)
        miny = min(miny, py)
        maxy = max(maxy, py)
    return minx, maxx, miny, maxy


def _square_corners(x: float, y: float, size: float, heading_deg: float):
    h = math.radians(heading_deg)
    fx, fy = math.cos(h), math.sin(h)  # forward
    lx, ly = math.cos(h + math.pi / 2), math.sin(h + math.pi / 2)  # left (up)

    bl = (x, y)
    br = (x + fx * size, y + fy * size)
    tr = (br[0] + lx * size, br[1] + ly * size)
    tl = (x + lx * size, y + ly * size)
    return bl, br, tr, tl


def _bounds_pythagoras_unit(level: int, angle_deg: float) -> Tuple[float, float, float, float]:
    theta = math.radians(angle_deg)

    def rec(x: float, y: float, size: float, heading: float, lvl: int, bounds):
        if lvl <= 0 or size <= 0:
            return bounds

        corners = _square_corners(x, y, size, heading)
        bounds = _update_bounds(bounds, corners)

        # top-left corner:
        _, _, _, tl = corners
        tlx, tly = tl

        left_size = size * math.cos(theta)
        right_size = size * math.sin(theta)

        left_heading = heading + angle_deg
        right_heading = heading + angle_deg - 90.0

        # apex point = end of left square base
        lh = math.radians(left_heading)
        apex_x = tlx + math.cos(lh) * left_size
        apex_y = tly + math.sin(lh) * left_size

        bounds = rec(tlx, tly, left_size, left_heading, lvl - 1, bounds)
        bounds = rec(apex_x, apex_y, right_size, right_heading, lvl - 1, bounds)
        return bounds

    init = (0.0, 0.0, 0.0, 0.0)
    return rec(0.0, 0.0, 1.0, 0.0, level, init)


def _fit_to_screen(screen: turtle.Screen, bounds_unit, margin: int = 20):
    w = screen.window_width()
    h = screen.window_height()

    minx, maxx, miny, maxy = bounds_unit
    span_x = maxx - minx
    span_y = maxy - miny

    span_x = span_x if span_x != 0 else 1.0
    span_y = span_y if span_y != 0 else 1.0

    usable_w = max(10, w - 2 * margin)
    usable_h = max(10, h - 2 * margin)

    scale = min(usable_w / span_x, usable_h / span_y)

    start_x = (-w / 2 + margin) - minx * scale
    start_y = (-h / 2 + margin) - miny * scale

    return start_x, start_y, scale


def draw_pythagoras_tree_squares(
    t: turtle.Turtle,
    level: int,
    bottom_left: tuple[float, float],
    size: float,
    heading_deg: float = 0.0,
    angle_deg: float = 45.0,
):
    if level <= 0 or size <= 0:
        return

    # draw current square
    t.penup()
    t.goto(bottom_left)
    t.setheading(heading_deg)
    t.pendown()
    for _ in range(4):
        t.forward(size)
        t.left(90)

    corners = _square_corners(bottom_left[0], bottom_left[1], size, heading_deg)
    _, _, _, tl = corners
    tlx, tly = tl

    theta = math.radians(angle_deg)
    left_size = size * math.cos(theta)
    right_size = size * math.sin(theta)

    left_heading = heading_deg + angle_deg
    right_heading = heading_deg + angle_deg - 90.0

    lh = math.radians(left_heading)
    apex_x = tlx + math.cos(lh) * left_size
    apex_y = tly + math.sin(lh) * left_size

    draw_pythagoras_tree_squares(t, level - 1, (tlx, tly), left_size, left_heading, angle_deg)
    draw_pythagoras_tree_squares(t, level - 1, (apex_x, apex_y), right_size, right_heading, angle_deg)


def _bounds_binary_unit(level: int, angle_deg: float, scale: float) -> Tuple[float, float, float, float]:
    """
    Exact bounding box for the binary tree when:
      start=(0,0), heading=90°, branch_len=1
    """
    def rec(x: float, y: float, heading: float, length: float, lvl: int, bounds):
        if lvl <= 0 or length <= 0:
            return bounds

        h = math.radians(heading)
        x2 = x + math.cos(h) * length
        y2 = y + math.sin(h) * length

        bounds = _update_bounds(bounds, [(x, y), (x2, y2)])

        # right branch (t.right(angle))
        bounds = rec(x2, y2, heading - angle_deg, length * scale, lvl - 1, bounds)
        # left branch (t.left(angle*2) from the "right" orientation => heading + angle)
        bounds = rec(x2, y2, heading + angle_deg, length * scale, lvl - 1, bounds)

        return bounds

    init = (0.0, 0.0, 0.0, 0.0)
    return rec(0.0, 0.0, 90.0, 1.0, level, init)


def draw_pythagoras_binary_tree(t: turtle.Turtle, branch_len: float, level: int, angle: float = 45.0, scale: float = 0.7):
    if level == 0:
        return

    t.forward(branch_len)

    t.right(angle)
    draw_pythagoras_binary_tree(t, branch_len * scale, level - 1, angle, scale)

    t.left(angle * 2)
    draw_pythagoras_binary_tree(t, branch_len * scale, level - 1, angle, scale)

    t.right(angle)
    t.backward(branch_len)


def render_tree(tree_type: TreeType, depth: int):
    try:
        screen, t = init_screen()
        t.clear()

        if tree_type == "squares":
            t.color("black")
            angle_deg = 45.0

            bounds_unit = _bounds_pythagoras_unit(depth, angle_deg)
            start_x, start_y, base_size = _fit_to_screen(screen, bounds_unit, margin=20)

            draw_pythagoras_tree_squares(
                t, depth, (start_x, start_y), base_size, heading_deg=0.0, angle_deg=angle_deg
            )

        elif tree_type == "binary":
            t.color("brown")
            angle_deg = 45.0
            scale = 0.7

            bounds_unit = _bounds_binary_unit(depth, angle_deg, scale)
            start_x, start_y, branch_len = _fit_to_screen(screen, bounds_unit, margin=20)

            t.penup()
            t.goto(start_x, start_y)
            t.setheading(90)
            t.pendown()

            draw_pythagoras_binary_tree(t, branch_len, depth, angle=angle_deg, scale=scale)

        else:
            raise ValueError("tree_type must be 'squares' or 'binary'")

        screen.update()
        print("\nVisualization complete! Click on the window to close it.")
        screen.exitonclick()
    except turtle.Terminator:
        # Handle window being closed
        pass
    finally:
        try:
            # Clean up turtle graphics
            turtle.bye()
        except:
            pass


def main():
    tree_type = input("Enter tree type (squares/binary) [binary]: ").strip().lower() or "binary"
    if tree_type not in ("squares", "binary"):
        tree_type = "binary"

    try:
        depth = int(input("Enter recursion depth (1-15) [7]: ").strip() or "7")
    except ValueError:
        depth = 7

    depth = max(1, min(15, depth))
    render_tree(tree_type, depth)


if __name__ == "__main__":
    main()
