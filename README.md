# Setup

```bash
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install .
```

# Run Lexico

```bash
(env) $ python main.py lexico [Path to pascal source file] 
```

Example:
```bash
(env) $ python main.py lexico ./pascal_sources/Test4.pas  
```

# Run a single module

```bash
(env) $ python -m compiler.lexico
```

# Test

```bash
(env) $ pytest
```
