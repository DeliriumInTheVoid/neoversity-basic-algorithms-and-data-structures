import turtle

def koch_snowflake(t:turtle.Turtle, order: int, size: float):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(t, order - 1, size / 3)
            t.left(angle)


def draw_snowflake(order: int, size: float):
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-size/2, size/2)
    t.pendown()

    for _ in range(3):
        koch_snowflake(t, order, size)
        t.right(120)

    window.mainloop()
