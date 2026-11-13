import py_compile
import glob
import sys
import os

def check_all():
    print("Running Python syntax & bytecode compilation checks...")
    files = glob.glob("backend/**/*.py", recursive=True) + glob.glob("shared/**/*.py", recursive=True)
    errors = 0
    for f in files:
        try:
            py_compile.compile(f, doraise=True)
            print(f"  ✓ {f}")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {f}: {e}")
            errors += 1
            
    if errors > 0:
        print(f"\nFAILED: {errors} syntax/compilation errors found.")
        sys.exit(1)
    else:
        print(f"\nPASSED: All {len(files)} Python files compiled successfully without syntax errors.")

if __name__ == "__main__":
    check_all()
