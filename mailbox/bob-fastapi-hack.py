import threading
from uagents import Agent, Context 
from uagents_core.identity import Identity
from models import *
from uagents.setup import fund_agent_if_low
from fastapi import FastAPI

import os
from dotenv import load_dotenv
 
load_dotenv()


"""
For mailbox agents, you do NOT define any end point for submission. 
Fetch.ai likely handles this for you under the hood. They probably host their own
servers somewhere which stays up all the time to hold your messages.
"""
bob = Agent(name="bob", seed=os.getenv("BOB_SEED_PHRASE"), port=8000, mailbox=True)

ALICE_IDENTITY = Identity.from_seed(seed=os.getenv("ALICE_SEED_PHRASE"), index=0)
ALICE_ADDRESS = ALICE_IDENTITY.address

"""
We literally only have this because Render does not let you do background tasks on free tier.
This means we cfan't just run Bob directly. We CAN set up a boof FastAPI backend though, so we can
run Bob as a "web app" (aka on free tier)
"""
app = FastAPI()

@app.get("/healthz")
async def health():
    return {"status": "ok"}

fund_agent_if_low(bob.wallet.address())

@bob.on_event("startup")
async def introduce_agent(ctx: Context):
    # front = await bob._message_queue.get()
    pass

"""
FOR MAILBOX AGENTS: This will auto run for each mailbox message.
It seems like unlike AWS SQS, you do NOT need to implement your own polling service.
"""
@bob.on_message(model=Message)
async def pong(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"{msg.content}")
    await ctx.send(ALICE_ADDRESS, Message(content="I receved your message, Alice"))

def run_agent():
    bob.run()

if __name__ == "__main__":
    import uvicorn
    threading.Thread(target=run_agent, daemon=True).start()
    # Hack to get this to work on Render free tier web app hosting
    uvicorn.run(app, host="0.0.0.0", port=4000)
 
