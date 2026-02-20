import time
import gevent
from classic.gevent_runner.runner import GreenletRunner


def print_numbers():
    count = 0
    while True:
        count += 1
        print(f"[Numbers Task] Count: {count}")
        gevent.sleep(2)


def print_timestamp():
    while True:
        current_time = time.strftime("%H:%M:%S")
        print(f"[Timestamp Task] Current time: {current_time}")
        gevent.sleep(3)


def print_heartbeat():
    while True:
        print(f"[Heartbeat Task] System is alive!")
        gevent.sleep(5)


def main():
    print("Starting GreenletRunner with 3 concurrent tasks...")
    print("Press Ctrl+C to stop all tasks\n")
    
    # Create a runner instance
    runner = GreenletRunner()
    
    # Add tasks to the runner
    runner.add(print_numbers, print_timestamp, print_heartbeat)
    
    # Start the main loop (blocks until SIGTERM or SIGINT)
    # This will run indefinitely until interrupted
    runner.run()
    
    print("\nAll tasks stopped gracefully.")


if __name__ == "__main__":
    main()
