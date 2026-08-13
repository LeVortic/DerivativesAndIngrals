# Calculus Tool

An educational Python project that parses mathematical expressions into syntax trees and demonstrates symbolic differentiation, symbolic integration, numerical integration, and comparison with SymPy.

> This is a learning project, not a replacement for a computer algebra system. Symbolic integration supports a limited set of patterns.

## Features

- Tokenizes expressions and builds an abstract syntax tree
- Evaluates expressions for a supplied value of `x`
- Applies common symbolic differentiation and integration rules
- Approximates definite integrals with Simpson's rule
- Provides a Tkinter desktop interface
- Compares results with SymPy

## Requirements

- Python 3.10 or newer
- Tkinter (usually included with Python)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
```

## Usage

Launch the GUI:

```bash
python -m calculus_tool
```

Expressions use explicit operators, for example:

```text
x^2 + 2*x + 1
sin(2*x)
3*x*cos(x)
```

Run the tests:

```bash
pytest
```

## Project layout

- `src/calculus_tool/`: maintained parser, calculus engines, SymPy adapter, and GUI
- `tests/`: automated correctness checks
- `legacy/`: the earlier string-based prototype retained for reference

## Known limitations

The symbolic integrator recognizes selected textbook patterns and does not perform general-purpose algebraic normalization. Results should be checked before being used in consequential work.

## License

No license has been selected yet. Add a `LICENSE` file before inviting reuse or contributions.
