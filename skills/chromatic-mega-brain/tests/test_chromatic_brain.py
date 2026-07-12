from pathlib import Path
import importlib.util

module_path = Path(__file__).resolve().parents[1] / "scripts" / "chromatic_brain.py"
spec = importlib.util.spec_from_file_location("chromatic_brain", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

def test_architecture_selection():
    colors = module.select_colors("Analyze architecture, security risks and implementation plan")
    assert "WHITE" in colors
    assert "BLUE" in colors
    assert "RED" in colors
    assert "GREEN" in colors

def test_minimum_two_colors():
    colors = module.select_colors("A complex decision")
    assert len(colors) >= 2

def test_maximum_colors():
    colors = module.select_colors("architecture security performance knowledge user constraints implementation evidence", 3)
    assert len(colors) <= 3
