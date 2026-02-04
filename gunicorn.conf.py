import multiprocessing

# Bind to port 8000
bind = "0.0.0.0:8000"

# Formula: (2 x number of cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Access and Error logs
accesslog = "-"
errorlog = "-"

# Timeout for long calculations (like distance matrices)
timeout = 120
