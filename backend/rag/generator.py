import os
from dotenv import load_dotenv
import anthropic

from rag.types import RetrievedChunk

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def build_prompt(query, context=None, history=""):
    history_block = history.strip()

    if history_block:
        history_block = f"\n\nConversation History:\n{history_block}"

    if context is None:
        return f"""
        Answer the question in maximum 3 sentences.

        Use the recent conversation history if it helps answer the user's question consistently.{history_block}

        Current Question:
        {query}
        """

    context_text = "\n\n".join(
        document.content
        for document in context
    )

    return f"""
    Answer the question in maximum 3 sentences.

    Use the provided context and the recent conversation history to answer the user's question.

    If the answer is not in the context, say:
    "I could not find relevant information."

    {history_block}

    Context:
    {context_text}

    Current Question:
    {query}
    """


def generate_reponse(
    query,
    context: list[RetrievedChunk] | None = None,
    history="",
):
    prompt = build_prompt(
        query,
        context=context,
        history=history,
    )

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text


def stream_reponse(
    query,
    context: list[RetrievedChunk] | None = None,
    history="",
):
    prompt = build_prompt(
        query,
        context=context,
        history=history,
    )

    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            yield text








