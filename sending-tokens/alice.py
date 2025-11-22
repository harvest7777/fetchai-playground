from uagents import Agent, Context, Model
from uagents.agent import Address
from uagents_core.identity import Identity
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from models import *

import os
from dotenv import load_dotenv
 
load_dotenv()

alice = Agent(name="alice", seed=os.getenv("ALICE_SEED_PHRASE"), port=8001, endpoint=["http://localhost:8001/submit"])

# This is a connection to the blockchain
ledger_client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())

# Lets define some constants
AMOUNT = 10
DENOM = "atestfet" # atestfet is the one you can get from Dorado faucet https://explore-dorado.fetch.ai/

BOB_IDENTITY = Identity.from_seed(seed=os.getenv("BOB_SEED_PHRASE") or "", index=0)
BOB_ADDRESS = BOB_IDENTITY.address

# This is so Alice can regsiter for almanac contract. Almanac costs a little bit of money to register.
# We're using test funds so don't worry about money
fund_agent_if_low(str(alice.wallet.address()))
 
@alice.on_event("startup")
async def introduce_agent(ctx: Context):
    wallet_address: str = str(alice.wallet.address())
    balance = ledger_client.query_bank_all_balances(Address(wallet_address))
    ctx.logger.info(f"Alice's current balance: {balance}")
 

"""
This is how you pay another agent. 
"""
@alice.on_interval(period=10.0)
async def request_funds(ctx: Context):
    ctx.logger.info(f"Trying to request some funds from Bob")
    await ctx.send(
        BOB_ADDRESS,
        PaymentRequest(
            wallet_address=str(alice.wallet.address()), amount=AMOUNT, denom=DENOM
        ),
    )

# On a transaction, the agent gets sent a message with the transaction info. We're just trying to log it 
# if it succeeded.
@alice.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(alice.wallet.address())
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")

if __name__ == "__main__":
    alice.run()
 