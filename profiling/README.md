
## Python function timings using cProfile (builtin)

```bash
python -m cProfile script.py
```

## I/O profiling and characterization using Darshan

```
env DARSHAN_ENABLE_NONMPI= LD_PRELOAD=/usr/local/lib/libdarshan.so python script.py
```

