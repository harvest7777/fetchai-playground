if __name__ == "__main__":
    import requests
    import os
    from dotenv import load_dotenv
    from agent import Request
    from datetime import datetime
    load_dotenv()

    # This is the url of the agent we defined when creating an Agent object in agent.py
    url = f"http://localhost:8000"

    request = Request(timestamp=str(datetime.now()), text="This is from the send_request.py script")
    response = requests.post(url, json=request.model_dump())
    print(response.json())
