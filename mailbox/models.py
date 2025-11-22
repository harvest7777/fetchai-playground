from uagents import Model

# Notice this model is shared between Alice and Bob
# This is because Bob expects this shaped message in his receive handler. So, we should
# create messages with the expected shape
class Message(Model):
    content: str