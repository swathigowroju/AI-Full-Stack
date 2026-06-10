# AI Chatbot - Week 1

## What it does
A conversational AI chatbot built using Groq API and LLaMA 3.3 model.
Remembers the full conversation history until you type 'quit'.

## How to run
1. Install dependencies: pip install groq colorama
2. Set your Groq API key as environment variable
3. Run: python chatbot.py

## Temperature Experiment
Question: "Write a 2 line poem about rain"

- temperature=0.0 → Softly falls the rain tonight, A soothing melody, a gentle delight.
- temperature=0.5 → Softly falls the rain tonight, a soothing melody to the earth below...
- temperature=1.0 → Softly falls the rain tonight, a soothing melody to the earth below...

Observation: Higher temperature = more creative and descriptive output.
