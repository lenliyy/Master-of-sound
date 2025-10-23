# Master of Sound

A real-time music visualization project that transforms live audio input into dynamic, abstract visuals. Experience your music in multiple stunning visual styles!

## Features (Latest Version)

### New in Latest Version:
- **Five Distinct Visual Styles:**
  1. **Pulse Particles**: Dynamic particles pulsing with the beat
  2. **Wave Lines**: Flowing wave lines that dance with the music
  3. **Star Field**: Purple-white stars that twinkle and move with sound energy
  4. **Geometric Shapes**: Rotating polygons responding to audio
  5. **Fluid Ripples**: Liquid-like ripples that expand with sound

- **Enhanced Visual Effects:**
  - Improved star field with dynamic movement and color transitions
  - Multi-layered glow effects for better visibility
  - Cross-shaped light rays for stars
  - Smooth color transitions based on sound energy
  - Size and intensity scaling with audio input

- **Interactive Controls:**
  - Style switching buttons at the bottom of the screen
  - Keyboard shortcuts (1-5) for quick style changes
  - Sleek, modern UI with hover effects
  - Real-time style switching without interruption

### Original Features:
- Real-time microphone input processing
- Audio energy analysis
- Smooth visual transitions
- Cross-platform compatibility (Windows/macOS/Linux)
- User-friendly start interface with countdown

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

## How to Use

1. Launch the program
2. Click the red circular "Start" button in the center
3. Wait for the 3-second countdown
4. The visualizer will begin processing audio from your microphone
5. Use the buttons at the bottom or number keys 1-5 to switch between visualization styles:
   - 1: Pulse Particles
   - 2: Wave Lines
   - 3: Star Field (NEW: Purple-White theme)
   - 4: Geometric Shapes
   - 5: Fluid Ripples
6. Close the window to exit

## Tips for Best Experience

- Use in a quiet environment for better audio detection
- Try different types of music to see varied visual effects
- Experiment with all five visualization styles
- For Star Field effect, try music with clear beats for best visual impact
- Allow microphone access when prompted
- Run on a machine with decent graphics capability for smooth animations

## Notes and tips

- On macOS you may need to grant microphone permission to Python or your terminal application.
- If you encounter audio device issues, try running with a different `samplerate` or `blocksize` in the script.
- For better performance, run on a machine with audio hardware and avoid running heavy background processes.

## License

This project is released under the MIT License. See `LICENSE` for details.

## Contact

Repository: https://github.com/lenliyy/Master-of-sound

If you'd like changes (more docs, examples, or translations), tell me what to add.