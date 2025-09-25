import subprocess
import os
import urllib.request

def download_module():
    """Download module_RC_DES.so file if not exists"""
    module_url = "https://github.com/Lab2Phys/module_RC_DES/raw/refs/heads/main/module_RC_DES.so"
    module_filename = "module_RC_DES.so"
    
    if not os.path.exists(module_filename):
        print("Downloading module_RC_DES.so...")
        try:
            urllib.request.urlretrieve(module_url, module_filename)
            print("Module downloaded successfully")
        except Exception as e:
            print(f"❌ Failed to download module: {e}")
            return False
    else:
        print("Module already exists")
    return True

def install_latex_minimal():
    """Install minimal LaTeX only if needed"""
    try:
        # Check if pdflatex is already installed
        subprocess.run(['pdflatex', '--version'],
                      check=True, capture_output=True)
        print("LaTeX already installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing minimal LaTeX...")
        try:
            # Install minimal LaTeX packages
            subprocess.run(['apt-get', 'update', '-q'], check=True)
            subprocess.run(['apt-get', 'install', '-y',
                          'texlive-latex-base',
                          'texlive-pictures'], check=True)
            print("LaTeX installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install LaTeX")
            return False

# Download the module first
if not download_module():
    print("Cannot proceed without the required module")
    exit(1)

# Install LaTeX
install_latex_minimal()

import sympy as sp

# Optional circuit diagram URL
circuit_diagram_url = "https://raw.githubusercontent.com/Lab2Phys/Experiment-5/refs/heads/main/Exp5-Figure.tex"

# Circuit Inputs
num_nodes = 7

edges_R = [
    (1, 2, 'R'), (1, 3, 'R'), (1, 6, 'R'),
    (2, 3, 'R'), (2, 5, 'R'), (2, 7, 'R'),
    (3, 4, 'R'), (4, 5, 'R'), (4, 6, 'R'),
    (5, 7, 'R'), (6, 7, 'R')
]
edges_C = [(1, 2, 'C'), (1, 6, 'C'), (2, 7, 'C'), (4, 5, 'C')]

voltage_source_map = {
    (1, 2): -sp.Symbol('e1'),
    (1, 6): sp.Symbol('e2'),
    (2, 7): -sp.Symbol('e3')
}

loops = [
    [1, 3, 4, 6, 1],
    [4, 5, 7, 6, 4],
    [2, 3, 4, 5, 2],
    [1, 2, 3, 1],
    [2, 7, 5, 2]
]

q_branches_map_predefined = {
    'q_1': (1, 6),
    'q_2': (4, 5),
    'q_3': (2, 1),
    'q_4': (7, 2)
}

# Initialize and Run Circuit Analyzer
try:
    from module_RC_DES import CircuitAnalyzer
  
    analyzer = CircuitAnalyzer(
        num_nodes=num_nodes,
        edges_R=edges_R,
        edges_C=edges_C,
        voltage_source_map=voltage_source_map,
        loops=loops,
        q_branches_map_predefined=q_branches_map_predefined,
        circuit_diagram_url=circuit_diagram_url
    )
    print("Displaying user interface:")
    analyzer.run()
except ImportError as e:
    print(f"❌ Error importing module_RC_DES: {e}")
    print("Please ensure the module file is properly downloaded.")
except Exception as e:
    print(f"Error initializing circuit analyzer: {e}")
    import traceback
    traceback.print_exc()