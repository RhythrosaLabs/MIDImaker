import tkinter as tk
from midiutil import MIDIFile
import random

class SongGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Generator")

        self.song_names = []

        # Create the GUI elements
        self.key_label = tk.Label(root, text="Select Key:")
        self.key_label.pack()

        self.key_var = tk.StringVar(root)
        self.key_var.set("C")  # Default key is C
        self.key_option_menu = tk.OptionMenu(root, self.key_var, *keys)
        self.key_option_menu.pack()

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.lines = []
        for i in range(7):
            line_frame = tk.Frame(self.frame)
            line_frame.pack()

            line_label = tk.Label(line_frame, text=f"Song {i+1}:")
            line_label.pack(side=tk.LEFT)

            song_name_entry = tk.Entry(line_frame)
            song_name_entry.pack(side=tk.LEFT)

            self.song_names.append(song_name_entry)

            randomize_text_button = tk.Button(line_frame, text="Randomize Text", command=lambda i=i: self.randomize_text(i))
            randomize_text_button.pack(side=tk.LEFT)

            randomize_chords_button = tk.Button(line_frame, text="Randomize Chords", command=lambda i=i: self.randomize_chords(i))
            randomize_chords_button.pack(side=tk.LEFT)

            self.lines.append((line_frame, song_name_entry))

        self.generate_button = tk.Button(root, text="Generate", command=self.generate_songs)
        self.generate_button.pack()

    def generate_songs(self):
        key = self.key_var.get()
        scale = scales[key]

        for i, (_, song_name_entry) in enumerate(self.lines):
            song_name = song_name_entry.get().strip()
            if not song_name:
                continue

            midi = MIDIFile(1)
            song_structure = song_structures[i % len(song_structures)]  # Cycle through song structures

            midi.addTrackName(track=0, time=0, trackName=song_name)
            midi.addTempo(track=0, time=0, tempo=120)

            time = 0

            for section_name in song_structure:
                section_chords = random.choice(chord_progressions[section_name])
                for chord_name in section_chords:
                    chord_notes = get_chord_notes(chord_name[0], key, scales[chord_name[1]])
                    for note in chord_notes:
                        midi.addNote(
                            track=0,
                            channel=0,
                            pitch=note,
                            time=time,
                            duration=1,
                            volume=100
                        )
                    time += 1

            filename = f"{song_name.replace(' ', '_').lower()}.mid"
            with open(filename, "wb") as output_file:
                midi.writeFile(output_file)

    def randomize_text(self, index):
        song_name_entry = self.song_names[index]
        randomized_name = random.choice(song_names_list)
        song_name_entry.delete(0, tk.END)
        song_name_entry.insert(0, randomized_name)

    def randomize_chords(self, index):
        chord_names = list(chords.keys())
        song_chords = []

        for _ in range(8):
            chord_name = random.choice(chord_names)
            scale_name = random.choice(list(scales.keys()))
            song_chords.append((chord_name, scale_name))

            line_frame, _ = self.lines[index]
            chord_labels = line_frame.winfo_children()[:-2]  # Exclude the text and randomize buttons

        for label, (chord_name, scale_name) in zip(chord_labels, song_chords):
            label.config(text=f"{chord_name} in {scale_name}")

    # Update the chord_progressions for the generated song
        song_structure = song_structures[index % len(song_structures)]  # Cycle through song structures
        chord_progressions[song_structure[0]] = song_chords



    def run(self):
        self.root.mainloop()


def get_chord_notes(chord_name, key, scale):
    root_note = notes[key]
    root_index = scale.index(root_note)

    chord_notes = []
    for step in chords[chord_name]:
        note_index = (root_index + step) % len(scale)
        chord_notes.append(scale[note_index])

    return chord_notes


notes = {
    "C": "C",
    "C#": "C#",
    "Db": "C#",
    "D": "D",
    "D#": "D#",
    "Eb": "D#",
    "E": "E",
    "F": "F",
    "F#": "F#",
    "Gb": "F#",
    "G": "G",
    "G#": "G#",
    "Ab": "G#",
    "A": "A",
    "A#": "A#",
    "Bb": "A#",
    "B": "B"
}

keys = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']


scales = {
    "C": [0, 2, 4, 5, 7, 9, 11],
    "C#": [1, 3, 5, 6, 8, 10, 0],
    "Db": [1, 3, 5, 6, 8, 10, 0],
    "D": [2, 4, 6, 7, 9, 11, 1],
    "D#": [3, 5, 7, 8, 10, 0, 2],
    "Eb": [3, 5, 7, 8, 10, 0, 2],
    "E": [4, 6, 8, 9, 11, 1, 3],
    "F": [5, 7, 9, 10, 0, 2, 4],
    "F#": [6, 8, 10, 11, 1, 3, 5],
    "Gb": [6, 8, 10, 11, 1, 3, 5],
    "G": [7, 9, 11, 0, 2, 4, 6],
    "G#": [8, 10, 0, 1, 3, 5, 7],
    "Ab": [8, 10, 0, 1, 3, 5, 7],
    "A": [9, 11, 1, 2, 4, 6, 8],
    "A#": [10, 0, 2, 3, 5, 7, 9],
    "Bb": [10, 0, 2, 3, 5, 7, 9],
    "B": [11, 1, 3, 4, 6, 8, 10]
}

chords = {
    "Major": [0, 4, 7],
    "Minor": [0, 3, 7],
    "Diminished": [0, 3, 6],
    "Augmented": [0, 4, 8],
    # Add more chords as needed
}

chord_progressions = {
    "Intro": [
        ["Minor", "Minor"],  # Em
        ["Major", "Major"],  # C
        ["Minor", "Minor"],  # Am
        ["Minor", "Minor"]   # Bm
    ],
    "Verse": [
        ["Minor", "Minor"],  # Em
        ["Major", "Major"],  # C
        ["Minor", "Minor"],  # Am
        ["Minor", "Minor"]   # Bm
    ],
    "Chorus": [
        ["Minor", "Minor"],  # Em
        ["Major", "Major"],  # C
        ["Minor", "Minor"],  # Am
        ["Minor", "Minor"]   # Bm
    ],
    "Bridge": [
        ["Minor", "Minor"],  # Em
        ["Minor", "Minor"],  # Am
        ["Major", "Major"],  # C
        ["Minor", "Minor"]   # Bm
    ],
    "Outro": [
        ["Minor", "Minor"],  # Em
        ["Minor", "Minor"],  # Am
        ["Major", "Major"],  # C
        ["Minor", "Minor"]   # Bm
    ]
}

song_structures = [
    ["Intro"],
    ["Verse"],
    ["Chorus"],
    ["Verse"],
    ["Chorus"],
    ["Bridge"],
    ["Chorus", "Chorus"],
    ["Outro"]
]

song_names_list = [
    "The Quirky Bananas",
    "Funky Donuts",
    "The Wacky Noodles",
    "Peculiar Pickles",
    "The Bumbling Buffoons",
    "Silly Sausages",
    "Absurd Avocados",
    "The Goofy Gargoyles",
    "Whimsical Walruses",
    "The Laughing Llamas",
    "Oddball Octopuses",
    "Cheesy Chinchillas",
    "The Silly Sloths",
    "Absurd Apples",
    "The Bizarre Bumblebees",
    "Wacky Watermelons",
    "The Quirky Quokkas",
    "Funky Flamingos",
    "The Ridiculous Raccoons",
    "Hilarious Hedgehogs",
    "The Goofy Giraffes",
    "Funny Frogs",
    "The Silly Sharks",
    "Quirky Quails",
    "The Eccentric Elephants",
    "Zany Zebras",
    "The Whacky Walnuts",
    "Absurd Alligators",
    "The Crazy Crayons",
    "Funky Fireflies",
    "The Wacky Wombats",
    "Peculiar Penguins",
    "The Bumbling Butterflies",
    "Silly Seagulls",
    "The Laughing Lizards",
    "Oddball Otters",
    "The Cheesy Chickens",
    "Whimsical Weasels",
    "The Absurd Armadillos",
    "Goofy Grapes",
    "The Quirky Quails",
    "Funky Flamingos",
    "The Ridiculous Raccoons",
    "Hilarious Hedgehogs",
    "The Goofy Giraffes",
    "Funny Frogs",
    "The Silly Sharks",
    "Quirky Quails",
    "The Eccentric Elephants",
    "Zany Zebras"
]

root = tk.Tk()
gui = SongGeneratorGUI(root)
gui.run()
