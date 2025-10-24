from uagents import Agent, Context
from uagents_core.identity import Identity
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from models import *

import os
from dotenv import load_dotenv
 
load_dotenv()


alice = Agent(name="alice", seed=os.getenv("ALICE_SEED_PHRASE"), port=8001, endpoint=["http://localhost:8001/submit"])

BOB_IDENTITY = Identity.from_seed(seed=str(os.getenv("BOB_SEED_PHRASE")), index=0)
BOB_ADDRESS = BOB_IDENTITY.address

# This is so Alice can regsiter for almanac contract. Almanac costs a little bit of money to register.
fund_agent_if_low(str(alice.wallet.address()))
 
@alice.on_event("startup")
async def introduce_agent(ctx: Context):
    pass

@alice.on_interval(period=5.0)
async def ping_bob(ctx: Context):
    await ctx.send(BOB_ADDRESS, Message(content="Hello this is Alice"))
    ctx.logger.info("Sent message to Bob")

@alice.on_message(model=Message)
async def echo(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Got response: {msg.content}")

if __name__ == "__main__":
    alice.run()
 