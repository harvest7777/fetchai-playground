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

@agent.on_rest_get("/", Response)
async def handle_get(ctx: Context):
    return {
        "timestamp": str(datetime.now()),
        "text": "Hello from the GET handler!",
        "agent_address": ctx.agent.address,
    }

protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )
    response = "meowwww"
    # is_start_of_chat: AgentContent = isinstance(msg.content[-1], StartSessionContent)
    is_user_message = isinstance(msg.content[-1], TextContent)
    ctx.logger.info(msg)
    if is_user_message:
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                # This will end the chat session
                # EndSessionContent(type="end-session") 
            ]
        ))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

# I believe you have to have this to register it to AgentVerse
agent.include(protocol, publish_manifest=True)
if __name__ == "__main__":
    agent.run()