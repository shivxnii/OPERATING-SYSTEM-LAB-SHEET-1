import os
import time
import subprocess

# ------------------------------
# Task 1: Process Creation Utility
# ------------------------------
def task1_process_creation(n=3):
    print(f"\n[TASK 1] Creating {n} child processes...\n")
    pids = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # Child process
            print(f"Child {i+1}:")
            print(f"  PID     = {os.getpid()}")
            print(f"  Parent  = {os.getppid()}")
            print(f"  Message = Hello from child {i+1}!\n")
            os._exit(0)
        else:
            pids.append(pid)
    # Parent waits for all
    for pid in pids:
        finished_pid, status = os.waitpid(pid, 0)
        print(f"Parent: Child {finished_pid} finished (status={status})")
    print("\nAll child processes completed.\n")


# --------------------------------------
# Task 2: Command Execution Using exec()
# --------------------------------------
def task2_command_exec(commands=None):
    print("\n[TASK 2] Executing commands from child processes using execvp()\n")
    if commands is None:
        commands = [["ls", "-l"], ["date"], ["ps", "aux"]]

    for i, cmd in enumerate(commands):
        pid = os.fork()
        if pid == 0:
            # Child replaces itself with command execution
            print(f"Child {i+1} executing command: {' '.join(cmd)}")
            try:
                os.execvp(cmd[0], cmd)
            except Exception as e:
                print(f"Error executing {cmd[0]}: {e}")
                os._exit(1)
        else:
            os.waitpid(pid, 0)
    print("\nAll commands executed by child processes.\n")


# ---------------------------------
# Task 3: Zombie & Orphan Processes
# ---------------------------------
def task3_zombie_and_orphan():
    print("\n[TASK 3] Demonstrating Zombie and Orphan Processes\n")

    # ---- Zombie demonstration ----
    pid = os.fork()
    if pid == 0:
        print(f"[Zombie Child] PID={os.getpid()} exiting immediately...")
        os._exit(0)
    else:
        print(f"[Parent] Created zombie child PID={pid}, sleeping 5 seconds...")
        time.sleep(5)
        # During this sleep, zombie will exist
        os.waitpid(pid, 0)
        print(f"[Parent] Reaped zombie child {pid}")

    # ---- Orphan demonstration ----
    pid = os.fork()
    if pid == 0:
        print(f"[Orphan Child] PID={os.getpid()} started. Parent={os.getppid()}")
        print("[Orphan Child] Sleeping for 5 seconds (parent will exit)...")
        time.sleep(5)
        print(f"[Orphan Child] Now adopted by init (new parent={os.getppid()})")
        os._exit(0)
    else:
        print(f"[Parent] Exiting before child {pid} finishes (to orphan it).")
        os._exit(0)  # parent exits early to create orphan


# ------------------------------------------------------
# Task 4: Inspecting Process Info from /proc/[pid]
# ------------------------------------------------------
def task4_inspect_proc(pid):
    print(f"\n[TASK 4] Inspecting process info for PID={pid}\n")

    try:
        with open(f"/proc/{pid}/status") as f:
            lines = f.readlines()
            for line in lines:
                if any(keyword in line for keyword in ["Name:", "State:", "VmRSS:"]):
                    print(line.strip())
    except Exception as e:
        print(f"Error reading /proc/{pid}/status: {e}")

    try:
        exe = os.readlink(f"/proc/{pid}/exe")
        print(f"Executable Path: {exe}")
    except Exception as e:
        print(f"Error reading exe: {e}")

    try:
        fds = os.listdir(f"/proc/{pid}/fd")
        print(f"Open File Descriptors: {fds}")
    except Exception as e:
        print(f"Error reading fds: {e}")


# ------------------------------------------------------
# Task 5: Process Prioritization using nice()
# ------------------------------------------------------
def cpu_intensive_task(limit=10000000):
    s = 0
    for i in range(limit):
        s += i % 7
    return s

def task5_prioritization(children=3):
    print(f"\n[TASK 5] Creating {children} CPU-intensive child processes with different priorities\n")
    for i in range(children):
        pid = os.fork()
        if pid == 0:
            nice_val = i * 5  # Different nice levels: 0, 5, 10, ...
            try:
                os.nice(nice_val)
            except PermissionError:
                print(f"Child {i+1}: Insufficient permission to change nice value.")
            start = time.time()
            cpu_intensive_task(3000000)
            end = time.time()
            print(f"Child {i+1} PID={os.getpid()} nice={nice_val} duration={end-start:.3f}s")
            os._exit(0)
    # Parent waits for all children
    for _ in range(children):
        os.wait()


# ------------------------------------------------------
# Main Driver
# ------------------------------------------------------
def main():
    print("\n========= ENCS351: Process Management Lab =========\n")
    print("1. Task 1 - Process Creation")
    print("2. Task 2 - Command Execution using exec()")
    print("3. Task 3 - Zombie & Orphan Processes")
    print("4. Task 4 - Inspect Process Info (/proc)")
    print("5. Task 5 - Process Prioritization\n")

    choice = input("Select a task (1–5): ")

    if choice == "1":
        n = int(input("Enter number of child processes: "))
        task1_process_creation(n)
    elif choice == "2":
        task2_command_exec()
    elif choice == "3":
        task3_zombie_and_orphan()
    elif choice == "4":
        pid = input("Enter PID to inspect: ")
        task4_inspect_proc(pid)
    elif choice == "5":
        task5_prioritization()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
