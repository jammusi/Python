import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()  # Lock for thread-safety
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Usage
def create_singleton_instance():
    instance = Singleton()
    print(f'Created instance: {instance}')

# Create multiple threads to create instances
threads = []
for _ in range(5):
    thread = threading.Thread(target=create_singleton_instance)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# Ensure only one instance is created
unique_instances = set(Singleton() for _ in range(5))
print(f'Total unique instances: {len(unique_instances)}')
