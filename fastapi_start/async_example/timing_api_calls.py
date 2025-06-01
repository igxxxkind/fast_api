import uvicorn
from main import app
import asyncio
from httpx import AsyncClient
import time
# to define a function to run the server
def run_server():
    uvicorn.run(app, port=8000, log_level="error")
# define the start of the server as a context manager
from contextlib import contextmanager
from multiprocessing import Process
@contextmanager
def run_server_in_process():
    p=Process(target=run_server)
    p.start()
    time.sleep(2)
    print("Server is running in a separate process")
    yield
    p.terminate()

# define a function that makes N concurrent requests to the specific endpoint
async def make_requests_to_endpoint(n: int, path: str):
    async with AsyncClient(base_url = "http://localhost:8000") as client:
            tasks = (client.get(path, timeout=float("Inf")) for _ in range(n)) 
            await asyncio.gather(*tasks)

async def main(n: int = 10):
    with run_server_in_process():
        begin = time.time()
        await make_requests_to_endpoint(n, "/sync")
        end = time.time()
        print(f"Time take to make {n} requests "
              f"to sync endpoint: {end - begin} seconds")
        
        begin = time.time()
        await make_requests_to_endpoint(n, "/async")
        end = time.time()
        print(f"Time to make {n} requests "
              f"to async endpoint: {end - begin} seconds")
        
if __name__ == "__main__":
    asyncio.run(main(n=100))