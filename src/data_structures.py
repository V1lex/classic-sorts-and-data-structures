class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next = next_node


class Stack:
    """
    Стек на односвязном списке с поддержкой получения минимума за O(1).
    """

    def __init__(self) -> None:
        self.top = None
        self.size = 0

    def push(self, x: int) -> None:
        current_min = x if self.top is None else min(x, self.top.current_min)
        node = Node(x, self.top)
        node.current_min = current_min
        self.top = node
        self.size += 1

    def pop(self) -> int:
        if self.top is None:
            raise IndexError("Ошибка: pop из пустого стека")
        value = self.top.value
        self.top = self.top.next
        self.size -= 1
        return value

    def peek(self) -> int:
        if self.top is None:
            raise IndexError("Ошибка: peek из пустого стека")
        return self.top.value

    def min(self) -> int:
        if self.top is None:
            raise IndexError("Ошибка: min из пустого стека")
        return self.top.current_min

    def is_empty(self) -> bool:
        return self.top is None

    def __len__(self) -> int:
        return self.size


class Queue:
    """
    Очередь на односвязном списке с операциями O(1).
    """

    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, x: int) -> None:
        node = Node(x, None)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def dequeue(self) -> int:
        if self.head is None:
            raise IndexError("Ошибка: dequeue из пустой очереди")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    def front(self) -> int:
        if self.head is None:
            raise IndexError("Ошибка: front из пустой очереди")
        return self.head.value

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self.size
