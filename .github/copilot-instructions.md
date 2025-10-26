# Copilot Instructions for all languages

- Use specifc instructions for writing code in different languages based on the code style guides provided.
- All code should be written in a consistent style.
- All code should be written in a way that is easy to read and understand.
- All code should be written in a way that is easy to maintain.
- All code should be written in a way that is easy to test.
- All code should be written in a way that is easy to debug.
- All code should be written in a way that is easy to extend.

When doing commnds in terminal or command line for python, you should run them against the local environment like this:
```pwsh
python .venv/Scripts/activate.ps1 && python -c "import some_module"
```


Write python command line like this:

```pwsh

python -c "import inspect, importlib; m=importlib.import_module('py_gfkdata._common'); print('\n'.join(inspect.getsource(m.get_select_result_data_and_columns).splitlines()[:40]))"

```

And Not like this:

```pwsh

python - << 'PY'
import inspect
import importlib
m = importlib.import_module('py_gfkdata._common')
print('\n'.join(inspect.getsource(m.get_select_result_data_and_columns).splitlines()[:40]))
PY
```
