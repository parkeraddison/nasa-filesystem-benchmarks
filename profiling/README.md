
## Python function timings using cProfile (builtin)

```bash
python -m cProfile -o out.profile script.py
```

Analyze with `python -i analyze-cprofile.py out.profile`.

See:
- https://docs.python.org/3/library/profile.html

## I/O profiling and characterization using Darshan

```
env DARSHAN_ENABLE_NONMPI= LD_PRELOAD=/usr/local/lib/libdarshan.so python script.py
```

Analyze with `python -i analyze-darshan.py`
