import sys
import importlib.metadata
import re
from pathlib import Path

def check_dependencies():
    # Ensure we can find requirements.txt
    base_dir = Path(__file__).resolve().parent.parent
    req_path = base_dir / 'requirements.txt'
    
    if not req_path.exists():
        print(f"[INFO] No requirements.txt found at {req_path}. Skipping check.")
        return True

    try:
        reqs = []
        with open(req_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ';' in line:
                        pkg_part, marker = line.split(';', 1)
                        # Basic marker evaluation
                        if 'win32' in marker and '!=' in marker and sys.platform == 'win32':
                            continue
                        if 'win32' in marker and '==' in marker and sys.platform != 'win32':
                            continue
                        line = pkg_part.strip()
                    
                    pkg = re.split(r'[;=<> \s]', line)[0].strip()
                    if pkg:
                        reqs.append(pkg)

        installed = {d.metadata['Name'].lower() for d in importlib.metadata.distributions()}
        missing = [r for r in reqs if r.lower() not in installed]
        
        if missing:
            print("MISSING_DEPS_FOUND")
            for m in missing:
                print(f"  - {m}")
            return False
        return True
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        return True

if __name__ == "__main__":
    if check_dependencies():
        sys.exit(0)
    else:
        sys.exit(1)
