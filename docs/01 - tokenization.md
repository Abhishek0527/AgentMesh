# Tokenization

## What is it?

Tokenization is the process of breaking text into smaller units called tokens.

Example:

Input:

I love books

Output:

["I", "love", "books"]

## Why is it needed?

LLMs cannot directly understand raw text.

Before processing, text is converted into tokens.

## Learning Notes

- Tokens are smaller pieces of text.
- A token can be a word, part of a word, punctuation, etc.
- Tokenization happens before embeddings are generated.
- More tokens = more processing cost.

## Flow

Text
↓
Tokenization
↓
Tokens

## Interview Question

Q. Why is tokenization required?

A. Because language models process tokens, not raw text.