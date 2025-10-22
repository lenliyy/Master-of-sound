# Master of Sound

A real-time music visualization project that transforms live audio input into dynamic, abstract visuals. Designed for interactive demonstrations and creative performances.

## Features

- Real-time microphone input
- Audio analysis using energy to drive visuals
- Pulse-style particle visualization that mimics a heartbeat
- Click-to-start flow with a 3-second countdown
- Lightweight, cross-platform (Windows/macOS/Linux) using Pygame and sounddevice

## Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
- pygame
- sounddevice
- numpy
- librosa

## Run the visualizer

From the project root, run:

```bash
python music_visualization/music_visualizer.py
```

## How to use

1. Run the program. A round red "Start" button appears in the center of the window.
2. Click the circular button to begin a 3-second countdown.
3. After the countdown, the visualizer will start listening to your microphone input.
4. Speak or play music — particles will pulse outward from the center. Louder sounds create stronger, faster pulses.
5. Close the window to stop the program.

## Notes and tips

- On macOS you may need to grant microphone permission to Python or your terminal application.
- If you encounter audio device issues, try running with a different `samplerate` or `blocksize` in the script.
- For better performance, run on a machine with audio hardware and avoid running heavy background processes.

## License

This project is released under the MIT License. See `LICENSE` for details.

## Contact

Repository: https://github.com/lenliyy/Master-of-sound

If you'd like changes (more docs, examples, or translations), tell me what to add.