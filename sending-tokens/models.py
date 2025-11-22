from uagents import Model

# Our payment request and transaction info models. 
# These contain useful information like what wallet to send to and the hassh of the transaction.
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str # Type of coin used. For us its atestfet aka literally a test $fet
 
class TransactionInfo(Model):
    tx_hash: str