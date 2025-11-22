from uagents import Agent, Context 
from uagents.agent import Address
from uagents_core.identity import Identity
from models import *
from uagents.setup import fund_agent_if_low
from cosmpy.aerial.client import LedgerClient, NetworkConfig

import os
from dotenv import load_dotenv
 
load_dotenv()

ledger_client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())

# One thing to note: you can do network = "mainnet" if you want it to be discoverable
bob = Agent(name="bob", seed=os.getenv("BOB_SEED_PHRASE") or "", port=8000, endpoint="http://localhost:8000/submit")

ALICE_IDENTITY = Identity.from_seed(seed=os.getenv("ALICE_SEED_PHRASE") or "", index=0)
ALICE_ADDRESS = ALICE_IDENTITY.address

"""
Another way to fund Bob is through the Dorado faucet.
https://explore-dorado.fetch.ai/

Just need to click 'Get Funds' and paste Bob's WALLET address.
These addresses seem to be generated from your see phrase just like BTC. So best to keep them safe.
"""
fund_agent_if_low(str(bob.wallet.address()))

@bob.on_event("startup")
async def introduce_agent(ctx: Context):
    current_balacne = ledger_client.query_bank_balance(Address(str(bob.wallet.address())))
    ctx.logger.info(f"Bob's current balance: {current_balacne}")
    pass

"""
This messaging syntax is similar to FastAPI where you can pass a pydantic model
to define the shape of the body and response 
"""
@bob.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
 
    # Send the payment
    transaction = ledger_client.send_tokens( 
        Address(msg.wallet_address), msg.amount, msg.denom, bob.wallet
    )
 
    # Send the tx hash so alice can confirm
    await ctx.send(ALICE_ADDRESS, TransactionInfo(tx_hash=transaction.tx_hash))

if __name__ == "__main__":
    bob.run()
 