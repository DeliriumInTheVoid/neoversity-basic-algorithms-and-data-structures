from typing import Dict, List

def hanoi_tower(n: int, source: str, target: str, auxiliary: str, rods: Dict[str, List[int]]):
    if n == 1:
        disk = rods[source].pop()
        rods[target].append(disk)
        print(f"Перемістити диск з {source} на {target}: {disk}")
        print(f"Проміжний стан: {rods}")
        return
    hanoi_tower(n - 1, source, auxiliary, target, rods)
    disk = rods[source].pop()
    rods[target].append(disk)
    print(f"Перемістити диск з {source} на {target}: {disk}")
    print(f"Проміжний стан: {rods}")
    hanoi_tower(n - 1, auxiliary, target, source, rods)
