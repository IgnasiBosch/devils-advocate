#!/usr/bin/env python3

# Serves the purpose of local development. It's run directly with uvicorn (without gunicorn).
import os


if __name__ == "__main__":
    import uvicorn

    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    uvicorn.run(
        "src.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
        workers=int(os.getenv("WEB_CONCURRENCY", 1)),
        reload=True,
        reload_dirs=[f"{BASE_DIR}/src"],
    )
