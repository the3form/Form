#!/usr/bin/env python3
"""
FORM Telemetry Simulator
WebSocket server that broadcasts simulated epistemic metrics for the FORM visualization.

Metrics:
- dissolution: degree of field boundary dissolution (0-1)
- ego_rigidity: ego structure stability (0-1)
- doubt: presence of uncertainty (0-1)
- phase_coherence: synchronization of collective elements (0-1)
- recursive_depth: depth of self-referential loops (0-1)
- anomaly: deviation from expected patterns (0-1)
- bootstrap_signal: rare signal triggering phase transition (boolean)
"""

import asyncio
import json
import math
import random
import signal
import sys
from datetime import datetime
import os
from typing import AsyncGenerator, Dict, List

try:
    import websockets
except ImportError:
    print("Error: websockets module not found.")
    print("Install with: pip install websockets")
    sys.exit(1)

try:
    from openai import AsyncOpenAI
except ImportError:
    print("Error: openai module not found.")
    print("Install with: pip install openai")
    sys.exit(1)

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value to range [min_val, max_val]."""
    return max(min_val, min(value, max_val))

def normalize_logprobs(logprobs: Dict[str, float]) -> Dict[str, float]:
    """Convert log probabilities to normalized probabilities."""
    probs = {token: math.exp(logprob) for token, logprob in logprobs.items()}
    total = sum(probs.values())
    return {token: prob / total for token, prob in probs.items()} if total > 0 else {}

def token_confidence(probs: List[float]) -> float:
    """Calculate confidence as the maximum probability."""
    return max(probs) if probs else 0.0

def token_entropy(probs: List[float]) -> float:
    """Calculate Shannon entropy of the probability distribution."""
    if not probs:
        return 0.0
    entropy = 0.0
    for prob in probs:
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

async def stream_llm_telemetry(
    prompt: str,
    model: str = "gpt-4o",
    top_k: int = 5,
) -> AsyncGenerator[Dict[str, float], None]:
    """Stream telemetry from LLM token generation."""
    token_count = 0
    doubt_tokens = []
    confidence_tokens = []
    entropy_tokens = []
    top_prob_history = []
    repeated_tokens = {}

    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        logprobs=True,
        top_logprobs=top_k,
    )

    async for chunk in stream:
        if not chunk.choices or not chunk.choices[0].delta:
            continue

        delta = chunk.choices[0].delta
        logprob_info = chunk.choices[0].logprobs

        if delta.content:
            token_text = delta.content
            repeated_tokens[token_text] = repeated_tokens.get(token_text, 0) + 1

            if logprob_info and logprob_info.content:
                # OpenAI returns a list of top_logprobs for the generated token
                top_logprobs_data = logprob_info.content[0].top_logprobs
                raw_logprobs = {item.token: item.logprob for item in top_logprobs_data}

                normalized = normalize_logprobs(raw_logprobs)
                probs = list(normalized.values())

                confidence = token_confidence(probs)
                entropy = token_entropy(probs)
                top_prob = max(probs) if probs else 0.0

                token_count += 1
                doubt_tokens.append(clamp(1.0 - confidence, 0.0, 1.0))
                confidence_tokens.append(confidence)
                entropy_tokens.append(entropy)
                top_prob_history.append(top_prob)

                if token_count == 0:
                    continue

                avg_confidence = sum(confidence_tokens) / len(confidence_tokens)
                avg_entropy = sum(entropy_tokens) / len(entropy_tokens)
                avg_doubt = sum(doubt_tokens) / len(doubt_tokens)
                avg_top_prob = sum(top_prob_history) / len(top_prob_history)
                repeat_density = sum(repeated_tokens.values()) / max(1, token_count)

                doubt = clamp(avg_doubt, 0.0, 1.0)
                phase_coherence = clamp(1.0 - avg_entropy, 0.0, 1.0)
                ego_rigidity = clamp(avg_confidence * 0.7 + (1.0 - avg_entropy) * 0.3, 0.0, 1.0)
                anomaly = clamp(avg_entropy * 0.8 + (1.0 - avg_top_prob) * 0.2, 0.0, 1.0)
                recursive_depth = clamp(min(1.0, repeat_density * 2.0), 0.0, 1.0)
                dissolution = clamp(0.5 + anomaly * 0.3 + (1.0 - phase_coherence) * 0.2, 0.0, 1.0)

                bootstrap_signal = dissolution > 0.87 and doubt > 0.75

                telemetry = {
                    "dissolution": dissolution,
                    "ego_rigidity": ego_rigidity,
                    "doubt": doubt,
                    "phase_coherence": phase_coherence,
                    "recursive_depth": recursive_depth,
                    "anomaly": anomaly,
                    "bootstrap_signal": bootstrap_signal,
                }

                yield telemetry


class TelemetrySimulator:
    """Generates and broadcasts epistemic telemetry metrics."""

    def __init__(self, update_interval=0.2):  # ~5 Hz
        self.update_interval = update_interval
        self.clients = set()

    async def broadcast(self, message):
        if not self.clients:
            return

        dead = set()
        payload = json.dumps(message)
        results = await asyncio.gather(
            *[client.send(payload) for client in self.clients],
            return_exceptions=True
        )

        for client, result in zip(list(self.clients), results):
            if isinstance(result, Exception):
                dead.add(client)

        self.clients -= dead


    async def telemetry_loop(self):
        """Main telemetry generation loop."""
        print(f"[{datetime.now().isoformat()}] Telemetry simulator started")
        
        prompts = [
            "Explain the philosophy of mind and consciousness in detail.",
            "Discuss the neuroscience of consciousness and brain activity.",
            "Explore the relationship between consciousness and reality.",
            "What is the hard problem of consciousness according to David Chalmers?",
            "Describe altered states of consciousness and their implications.",
            "Analyze the role of consciousness in artificial intelligence.",
            "Examine the evolutionary origins of consciousness.",
            "Discuss qualia and subjective experience in consciousness studies."
        ]
        
        prompt_index = 0
        
        try:
            while True:
                prompt = prompts[prompt_index]
                print(f"[{datetime.now().isoformat()}] Starting telemetry stream with prompt: {prompt[:50]}...")
                
                async for telemetry in stream_llm_telemetry(prompt):
                    telemetry["timestamp"] = datetime.now().isoformat()
                    await self.broadcast(telemetry)
                    await asyncio.sleep(self.update_interval)  # Throttle broadcasts
                
                prompt_index = (prompt_index + 1) % len(prompts)
                print(f"[{datetime.now().isoformat()}] Stream completed, cycling to next prompt...")
                
        except asyncio.CancelledError:
            print(f"[{datetime.now().isoformat()}] Telemetry loop cancelled")
            raise

    async def handle_client(self, websocket):
        """Handle new client connection."""
        client_addr = websocket.remote_address
        self.clients.add(websocket)
        print(f"[{datetime.now().isoformat()}] Client connected: {client_addr}")

        try:
            # Keep connection alive and send telemetry
            async for message in websocket:
                # Clients can send messages, but we ignore them for now
                pass
        except websockets.exceptions.ConnectionClosed:
            print(f"[{datetime.now().isoformat()}] Client disconnected: {client_addr}")
        finally:
            self.clients.discard(websocket)


async def main():
    """Start WebSocket server and telemetry simulator."""
    simulator = TelemetrySimulator(update_interval=0.2)

    # Start telemetry generator task
    telemetry_task = asyncio.create_task(simulator.telemetry_loop())

    # Start WebSocket server
    server = await websockets.serve(
        simulator.handle_client,
        "localhost",
        8765,
        ping_interval=20,
        ping_timeout=10,
    )

    print(f"[{datetime.now().isoformat()}] WebSocket server listening on ws://localhost:8765/telemetry")
    print("Press Ctrl+C to stop.")

    try:
        await asyncio.gather(telemetry_task, server.wait_closed())
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().isoformat()}] Shutting down...")
        server.close()
        await server.wait_closed()
        telemetry_task.cancel()
        try:
            await telemetry_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
