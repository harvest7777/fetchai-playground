"""
This simply registers an agent to the AgentVerse by enabling chat protocol and publishing the manifest.
Don't worry if you don't understand what this exactly means. It's essentially the mandatory functions
your agent must implement to be compliant with the AgentVerse protocol.
"""

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