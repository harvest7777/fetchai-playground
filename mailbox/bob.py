from uagents import Agent, Context 
from uagents_core.identity import Identity
from models import *
from uagents.setup import fund_agent_if_low

import os
from dotenv import load_dotenv
 
load_dotenv()


"""
For mailbox agents, you do NOT define any end point for submission. 
Fetch.ai likely handles this for you under the hood. They probably host their own
servers somewhere which stays up all the time to hold your messages.
"""
bob = Agent(name="bob", seed=os.getenv("BOB_SEED_PHRASE"), port=8000, mailbox=True)

ALICE_IDENTITY = Identity.from_seed(seed=str(os.getenv("ALICE_SEED_PHRASE")), index=0)
ALICE_ADDRESS = ALICE_IDENTITY.address

fund_agent_if_low(str(bob.wallet.address()))

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

if __name__ == "__main__":
    bob.run()
 
