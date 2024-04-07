from music21 import converter

def midi_to_frequency(midi_note):
    return 440 * (2 ** ((midi_note - 69) / 12))

def get_notes_from_midi(midi_file):
    # Load MIDI file
    midi_stream = converter.parse(midi_file)

    # Extract notes with duration and convert to frequencies
    notes_with_frequency = []
    for part in midi_stream.parts:
        for element in part.flat.notes:
            if element.isNote:
                note_info = {
                    "frequency": midi_to_frequency(element.pitch.midi),
                    "duration": element.duration.quarterLength
                }
                notes_with_frequency.append(note_info)

    return notes_with_frequency

# Example usage
if __name__ == "__main__":
    midi_file = "midi.mid"  # Replace "example.mid" with your MIDI file path
    notes = get_notes_from_midi(midi_file)
    print("Notes in MIDI file with frequency:")
    for note in notes:
        print("Frequency:", note["frequency"], "Hz, Duration:", note["duration"])
