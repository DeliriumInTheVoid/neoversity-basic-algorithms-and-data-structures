class Stack:
  def __init__(self):
    self.stack = []

  # Додавання елемента до стеку
  def push(self, item):
    self.stack.append(item)

  # Видалення елемента зі стеку
  def pop(self):
    if len(self.stack) < 1:
      return None
    return self.stack.pop()

  # Перевірка, чи стек порожній
  def is_empty(self):
    return len(self.stack) == 0

  # Перегляд верхнього елемента стеку без його видалення
  def peek(self):
    if not self.is_empty():
      return self.stack[-1]
    return None


def check_delimiters(sequence: str) -> str:
    opening:str = "({["
    closing:str = ")}]"
    matching_pairs:dict[str, str] = {')': '(', '}': '{', ']': '['}

    stack: Stack = Stack()

    for char in sequence:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty() or stack.peek() != matching_pairs[char]:
                return "Несиметрично"
            stack.pop()

    return "Симетрично" if stack.is_empty() else "Несиметрично"
