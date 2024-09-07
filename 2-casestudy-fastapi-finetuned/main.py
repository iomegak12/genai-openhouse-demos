import os
import uvicorn
from art import tprint

if __name__ == "__main__":
    try:
        tprint("Stores and Items")

        host = os.environ["UVICORN_HOST"]
        port = int(os.environ["UVICORN_PORT"])

        app = "stores_items.api:app"
        
        uvicorn.run(app, host=host, port=port, reload=True)
    except Exception as error:
        print(f"Error Occurred, Details: {error}")

        raise
