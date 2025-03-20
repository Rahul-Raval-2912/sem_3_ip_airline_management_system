from collections import deque

class AirlineQueue:
    def __init__(self):
        """Initialize the queue using deque for efficient operations."""
        self.queue = deque()

    def enqueue(self, item):
        """Add an item to the end of the queue.
        Args:
            item (any): The item to be added to the queue.
        """
        self.queue.append(item)
        print(f"Added to queue: {item}")

    def dequeue(self):
        """Remove and return the item from the front of the queue.
        Returns:
            any: The item removed from the queue.
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        item = self.queue.popleft()
        print(f"Removed from queue: {item}")
        return item

    def peek(self):
        """View the item at the front of the queue without removing it.
        Returns:
            any: The item at the front of the queue.
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue.")
        return self.queue[0]

    def is_empty(self):
        """Check if the queue is empty.
        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0

    def size(self):
        """Get the number of items in the queue.
        Returns:
            int: The size of the queue.
        """
        return len(self.queue)

    def display(self):
        """Display all items in the queue."""
        print("Current Queue:", list(self.queue))

# Example usage
if __name__ == "__main__":
    airline_queue = AirlineQueue()

    # Add passengers to the queue
    airline_queue.enqueue("Passenger 1")
    airline_queue.enqueue("Passenger 2")
    airline_queue.enqueue("Passenger 3")

    # Display the queue
    airline_queue.display()

    # Serve passengers
    airline_queue.dequeue()
    airline_queue.display()

    # Peek at the next passenger
    print("Next in queue:", airline_queue.peek())

    # Check the size of the queue
    print("Queue size:", airline_queue.size())

    # Check if the queue is empty
    print("Is queue empty?:", airline_queue.is_empty())
