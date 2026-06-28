# Gunicorn Configuration

You do **not** need a separate Gunicorn configuration file for this project.

The current Dockerfile command is valid and directly configures Gunicorn when the container starts:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "60", "app:app"]
```

This configures Gunicorn to:

- bind to `0.0.0.0:8000`
- use `2` workers
- use `2` threads per worker
- timeout after `60` seconds
- serve the Flask app object from `app.py` as `app:app`

A separate `gunicorn.conf.py` file is optional. It is useful when the command gets long or when you want a cleaner production configuration.

Example `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 2
threads = 2
timeout = 60
```

Then the Dockerfile command could become:

```dockerfile
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

For this project, keeping the Gunicorn settings directly in the Dockerfile is fine. Add `gunicorn.conf.py` only if more settings are needed later or if the Dockerfile should stay cleaner.
