import pytest

from src.data_structures import Queue, Stack


def test_stack_push_pop_min() -> None:
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()
    with pytest.raises(IndexError):
        stack.min()
    stack.push(3)
    stack.push(1)
    stack.push(4)
    assert stack.min() == 1
    assert stack.peek() == 4
    assert stack.pop() == 4
    assert stack.min() == 1
    assert len(stack) == 2
    assert not stack.is_empty()


def test_queue_enqueue_dequeue() -> None:
    queue = Queue()
    assert queue.is_empty()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.front() == 1
    assert queue.dequeue() == 1
    assert queue.front() == 2
    assert len(queue) == 1
    assert not queue.is_empty()
    assert queue.dequeue() == 2
    with pytest.raises(IndexError):
        queue.dequeue()
    with pytest.raises(IndexError):
        queue.front()
