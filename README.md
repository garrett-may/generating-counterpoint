# Generating Counterpoint

This repository contains the source code for my dissertation 'Generating Counterpoint'. This was created as part requirement for my Final Year Individual Project (COMPM091) for my MEng Degree in Computer Science at University College London.

My project focuses on researching the generation of counterpoint, leading to the building of this program, created in Python 3. The program takes in an input melody as a MIDI file and outputs a MIDI file containing the input melody and the generated counterpoint melody.

## Install

To run this project, you will need to install [music21](http://web.mit.edu/music21/). This can be done using pip3:

```
pip3 install music21
```

You may need to set the following environment variables for music21:

 - The MusicXML path, in order to find MusicXML files: `environment.set('musicxmlPath', '/<path-to-folder>/program')`

 - The MIDI path, in order to find MIDI files: `environment.set('midiPath', '/<path-to-folder>/program')`

## Run

Place an input melody as a MIDI file `<filename>.mid` inside the `program/res` folder.

Then, inside the `program/src` folder, run the following:

```
python3 generate_counterpoint.py ../res/<filename>
```

This will output the following files in the `program/res` folder:

 - `<filename>_gcp.mid`, a MIDI file with the input melody and the generated counterpoint melody
 - `<filename>_gcp.ly`, a LilyPond file with the input melody and the generated counterpoint melody
 - `<filename>_gcp.pdf`, a PDF file with the input melody and the generated counterpoint melody

Two files are available as test inputs:

 - `birthday.mid`, the "Happy Birthday" theme, in the key of C major
 - `haydn.mid`, an excerpt of of the Symphony No. 94 "Surprise Symphony" theme by Haydn, in the key of C major
