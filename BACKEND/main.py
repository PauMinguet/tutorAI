import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["src"],
        log_level="info",
    )