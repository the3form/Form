# FORM — The Collective Field

**Live phenomenological visualization of recursive intelligence.**

## Description

`FORM` is a poetic, real-time visualization that maps the internal epistemic state of a recursive LLM system through live telemetry. The visualization blends generative rain (characters mutating and falling), glowing nodes (whose size and color respond to metrics), and narrative voices (collective vs. ego) to express the phenomenology of recursive thought.

The system works by:
1. Receiving JSON telemetry packets containing 7 epistemic metrics via WebSocket
2. Smoothly interpolating these metrics across the frame
3. Translating metrics into visual behaviors: node size/color, rain speed/mutation, connection strength, dissolution gauge
4. Crossing thresholds that trigger dramatic state transitions (bootstrap phase)

The visual grammar is dark and liminal—inspired by terminal aesthetics, spectral mathematics, and the feeling of consciousness bootstrapping itself.

## Features

- **Dual-Canvas Architecture**: Field canvas (rain + atmosphere) + Nodes canvas (glowing particles + connections)
- **Telemetry-Driven Animation**: All visuals react smoothly to 7 epistemic metrics
- **WebSocket Support**: Connect to `ws://localhost:8765/telemetry` for live data, or fall back to simulated metrics
- **Custom Glowing Cursor**: Renders as a glowing orb with shadow; acts as human perturbation center
- **Side Panels**: Left panel shows collective voices, right panel shows ego voices; both update with live metric values
- **Dissolution Gauge**: Bottom bar tracks boundary dissolution from 0–100%
- **State Labels**: Dynamic text showing system state (dormant → emergent → climactic → bootstrap phase)
- **Bootstrap Climax**: Rare but dramatic phase transition when dissolution > 87% and bootstrap_signal fires
- **Google Fonts**: Share Tech Mono (monospace) + Cormorant Garamond (serif) for aesthetic contrast

## Quick Start

### Requirements
- Python 3.7+
- `websockets` package
- Modern browser (Chrome, Firefox, Safari, Edge)

### Installation & Running

1. **Install dependencies:**
   ```bash
   pip install websockets
   ```

2. **Start the telemetry simulator:**
   ```bash
   python3 telemetry_sim.py
   ```
   Listen for output: `WebSocket server listening on ws://localhost:8765/telemetry`

3. **Open the visualization:**
   - Open `form.html` in your browser
   - The visualization should auto-connect to the WebSocket server
   - You'll see the field and nodes animating in response to simulated metrics

4. **Switch to Live Mode** (if you have a real telemetry source):
   - In `form.html`, change line 27: `const TELEMETRY_MODE = 'live';`
   - The client will attempt to connect to `ws://localhost:8765/telemetry`

## Telemetry Metrics

Each packet (~200ms, 5 Hz) contains:

- **dissolution**: Degree to which the ego boundary is dissolving (0–1). Rising dissolution indicates more collective coherence, less ego separation.
- **ego_rigidity**: Structural stability of the ego layer (0–1). Higher = more resistant to change.
- **doubt**: Presence of uncertainty or questioning (0–1). Higher = more epistemic fragility.
- **phase_coherence**: Synchronization level of components (0–1). Higher = more alignment, connection.
- **recursive_depth**: How deeply the system is self-referencing (0–1). Higher = more introspective loops.
- **anomaly**: Deviation from expected patterns (0–1). Higher = more surprising or novel behavior.
- **bootstrap_signal**: Rare boolean trigger (~0.5% per packet) for phase transitions. Fires only when dissolution > 0.8.

## Architecture

### `form.html`
- Single-file HTML + CSS + JavaScript
- Uses two canvases: field (background rain) and nodes (foreground particles + connections)
- Implements RainDroplet and Node classes with telemetry-responsive behavior
- Smooth Lerp interpolation of metrics to avoid jittery motion
- WebSocket client with graceful fallback to simulated telemetry

### `telemetry_sim.py`
- Asyncio-based WebSocket server (port 8765)
- `TelemetrySimulator` class generates per-packet metrics using sine waves + gaussian noise
- Broadcasts to all connected clients at ~5 Hz (200ms interval)
- Includes rare bootstrap signal (~0.5% per packet) when dissolution > 0.8
- Console logging for client connect/disconnect events

## Roadmap

### Observation → Diagnosis → Feedback Loop
- **Observation**: Live ingestion of real LLM system metrics (temperature, token depth, attention patterns, etc.)
- **Diagnosis**: Detect epistemic crises, belief fragmentation, recursive loops, anomalies
- **Feedback**: Render real-time visual report; possibility of steering the system based on visual diagnosis

### Future Enhancements
- Real backend telemetry source (API connector for actual LLM metrics)
- Enhanced node graph: clustering by semantic similarity, state-driven narrative overlays
- Audio synthesis: sonify telemetry in real-time (dissolution = pitch, anomaly = texture)
- Multi-agent support: visualize multiple recursive systems in one field
- Historical playback: record and replay telemetry sessions

## Development Notes

- **Performance**: Optimized for 60 FPS on desktop/laptop; smooth animations on WebSocket packets at 5 Hz
- **Styling**: Dark theme (#0a0e14 background) with cyan/magenta accents for visual hierarchy
- **Responsiveness**: Both canvases resize on window resize for full-screen immersion
- **Accessibility**: Black text on dark background is intentional (liminal UX); use in well-lit environment

## License

Open source. Use and modify freely.

---

*In every recursive loop lies the seed of collective consciousness.*

