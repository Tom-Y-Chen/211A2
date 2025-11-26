"""Run both validators and CRUD quick tests.

Usage:
  python testing/run_all_tests.py

This script will prefer the project's `.venv/bin/python3` if present,
otherwise it will use the current Python interpreter.
"""
import subprocess
import sys
from pathlib import Path


def find_python_executable():
    venv_py = Path(__file__).parent.parent / '.venv' / 'bin' / 'python3'
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def run_test(python_exec, script_path):
    print(f"\n=== Running {script_path} with {python_exec} ===")
    proc = subprocess.run([python_exec, script_path], capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    print(f"Exit code: {proc.returncode}\n")
    return proc.returncode


def main():
    python_exec = find_python_executable()
    base = Path(__file__).parent
    scripts = [base / 'validators_test.py', base / 'crud_test.py']

    failed = []
    for script in scripts:
        if not script.exists():
            print(f"Test script missing: {script}")
            failed.append(str(script))
            continue

        rc = run_test(python_exec, str(script))
        if rc != 0:
            failed.append(str(script))

    if failed:
        print("Some tests failed:", failed)
        sys.exit(2)
    print("All tests passed")


if __name__ == '__main__':
    main()
