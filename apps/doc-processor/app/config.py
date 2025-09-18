import os
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
