import sys
from pathlib import Path


def parse_tree_and_create(text, base_path="."):
    """
    Parse a text representation of a folder structure and create it on disk.
    Lines starting with # are treated as comments and ignored.
    """
    # Convert base_path to Path object
    base = Path(base_path)
    
    # Keep track of current path and current depth
    path_stack = [base]

    # Process each line
    for line in text.split('\n'):
        # Skip empty lines and comments
        line = line.split('#')[0].rstrip()
        if not line.lstrip():
            continue
            
        # Determine depth
        tree_parts = line.replace('├──', '   ').replace('└──', '   ').replace('│', ' ').replace('|', ' ').split('    ')
        depth = len(tree_parts)

        # Extract the actual name (remove tree characters and strip whitespace)
        name = tree_parts[-1].strip()
        
        # Determine if it's a file (no trailing /)
        is_file = not name.endswith('/')
        if not is_file:
            name = name[:-1]  # Remove trailing slash
            
        # Adjust path stack based on depth
        while len(path_stack) > depth:
            path_stack.pop()
            
        # Create full path
        full_path = path_stack[-1] / name
        
        if is_file:
            # Create empty file
            full_path.touch()
            # print(f"Created file: {full_path}")
        else:
            # Create directory
            full_path.mkdir(parents=True, exist_ok=True)
            path_stack.append(full_path)
            # print(f"Created directory: {full_path}")

# Example usage
if __name__ == "__main__":
    # Example input
    example_structure = """
project/       # Use '#' for comments
    ├──data/   # Folders end with '/'
    ├──src/
    │   ├──main.py
    │   └──utils.py
    ├──tests/
    │   └──test_main.py
    ├──docs/
    │   ├──README.md
    │   └──API.md
    └──requirements.txt
"""
    
    # If input is provided as argument, read from file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            structure = f.read()
            # Create the structure
            parse_tree_and_create(structure)
    else:
        print(f"Provide an input file structured like the following example:\n{example_structure}")
    
