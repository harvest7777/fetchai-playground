from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
from uagents import Context, Protocol, Agent, Model

from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)
load_dotenv()

agent = Agent(
    name="heyyy aganet nent",
    seed=os.getenv("AGENT_SEED_PHRASE"),
    port=8000,
    mailbox=True,
)

class Response(Model):
    timestamp: str 
    text: str
    agent_address: str

# This is an example of a REST endpoint that can be used to test the agent
# Try visiting http://localhost:8000/ in your browser to see the response
# Note the port is dependent on the port you set when initializing the Agent object
@agent.on_rest_get("/", Response)
async def handle_get(ctx: Context):
    return {
        "timestamp": str(datetime.now()),
        "text": "Hello from the GET handler!",
        "agent_address": ctx.agent.address,
    }

# You can make this anything that represents the body of your post request
class Request(Model):
    timestamp: str 
    text: str

# We use the aforementioned defined Request. We'll reuse the response model from earlier for simplicity
# The request and response can be any shape
@agent.on_rest_post("/", Request, Response)
async def handle_post(ctx: Context, request: Request):
    # Check your console after sending a post request!
    ctx.logger.info(f"Received POST request: {request}")
    return {
        "timestamp": str(datetime.now()),
        "text": "I have received your request",
        "agent_address": ctx.agent.address,
    }

# This is needed to be compliant with AgentVerse's chat protocol
protocol = Protocol(spec=chat_protocol_spec)

# This is needed to be compliant with AgentVerse's chat protocol
# This decorator in particular makes this function get called when we get a message through 
# chat protocol
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    # Hardcoded response, your logic from LangGraph/LangChain/CrewAi/etc would go here
    response = "meowwww"

    # Here's an example on how to check various metadata such as first message or if the message
    # was sent by a user
    # is_start_of_chat: AgentContent = isinstance(msg.content[-1], StartSessionContent)
    is_user_message = isinstance(msg.content[-1], TextContent)

    ctx.logger.info(msg)

    if is_user_message:
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                # This will end the chat session on each messsage (no conversation)
                # EndSessionContent(type="end-session") 
            ]
        ))

# This is needed to be compliant with AgentVerse's chat protocol
@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

# This is needed to get registered to the AgentVerse
agent.include(protocol, publish_manifest=True)
if __name__ == "__main__":
    agent.run()