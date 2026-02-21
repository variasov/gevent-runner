import time
import gevent
from gevent import monkey

monkey.patch_all()

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
    """Daemon task - will be stopped when all non-daemon tasks complete."""
    while True:
        print(f"[Heartbeat Task - DAEMON] System is alive!")
        gevent.sleep(5)


def print_status():
    """Background monitoring daemon task."""
    while True:
        print(f"[Status Monitor - DAEMON] Monitoring system...")
        gevent.sleep(7)


def main():
    print("Starting GreenletRunner with 2 regular tasks and 2 daemon tasks...")
    print("Press Ctrl+C to stop all tasks\n")
    
    # Create a runner instance
    runner = GreenletRunner()
    
    # Add regular (non-daemon) tasks
    # These tasks need to complete for the runner to finish
    runner.add(print_numbers, print_timestamp)
    
    # Add daemon tasks - these will run in background
    # They will be automatically stopped when all non-daemon tasks finish
    runner.add(print_heartbeat, print_status, daemon=True)
    
    # Start the main loop (blocks until SIGTERM or SIGINT)
    # This will run indefinitely until interrupted
    runner.run()
    
    print("\nAll tasks stopped gracefully.")


if __name__ == "__main__":
    main()
