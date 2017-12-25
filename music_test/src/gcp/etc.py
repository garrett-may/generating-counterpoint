def circle_of_fifths_diff(a, b):
    diff = abs(circle_of_fifths[a] - circle_of_fifths[b])
    return min(diff, octave - diff)
    
def generate_chords(song):        
    major_heuristic = [0,5,4,5,1,4,6,1,5,4,2,4]
    best_chords = []
    for bar in song.elements:
        chord_prob = [0] * 12
        b = [note for note in bar if type(note) is Note]
        note_durations = [note.duration.quarterLength for note in b]
        note_pitches = [int(note.pitch.ps % 12) for note in b]
        for j in range(0, 12):
            profile = rotate(major_profile, j)
            heuristic = rotate(major_heuristic, j)
            note_prob = [1] * 12
            for i in range(0, len(note_pitches)):
                note_pitch = note_pitches[i]
                #fifth_diff = abs(circle_of_fifths[j] - circle_of_fifths[note_pitch]) % octave
                note_prob[note_pitch] = heuristic[note_pitch]
                #note_prob[note_pitch] = note_durations[i] * profile[note_pitch] * (octave - fifth_diff)
                #note_prob[note_pitch] = fifth_diff
            fifth_diff = circle_of_fifths_diff(note_names.index(best_chords[-1][0][0]), j) if len(best_chords) > 0 else 0
            sum_prob = sum(note_prob) + fifth_diff # 0 is C major
            chord_prob[j] += sum_prob
            
        profile = rotate(major_profile, 0)
        best_chord = [(note_names[i], chord_prob[i]) for i in range(0, len(chord_prob))]
        best_chord = sorted(best_chord, key=lambda x: x[1])
        #best_chord = sorted(best_chord, key=lambda tp: tp[1], reverse=True)
        #chord_prob = [chord_prob[i] * profile[i] for i in range(0, len(chord_prob))]
        best_chords += [best_chord]
        print('Best chord: {}'.format(best_chord))
            
def generate_key_naive(song):
    def coefficient(x, y, i):           
        #x_m = sum(x) / 12.0        
        #y_m = sum(y) / 12.0
        x = rotate(x, i)
        y = rotate(y, i)
        num = sum([(x[i]) * (y[i]) for i in chromatic_scale])
        den = (sum([(xi) ** 2 for xi in x]) * sum([(yi) ** 2 for yi in y])) ** 0.5
        return num / den
    
    notes = [note for bar in song.elements for note in bar if type(note) is Note]
    profile_types = [major_profile, minor_profile]
    y = [sum(map(lambda n: n.duration.quarterLength, filter(lambda n: (n.pitch.ps % octave) == p, notes))) for p in chromatic_scale]
    coefficients = [coefficient(x, y, p) for x in profile_types for p in chromatic_scale]
    coefficients = [(note_names[i % octave], key_types[i / octave]) for (i,r) in enumerate(coefficients)]
    return sorted(coefficients, key=lambda r: r[1])[0]
    
def generate_key_Krumhansl(song):
    
    def coefficient(x, y, i):           
        x_m = sum(x) / 12.0        
        y_m = sum(y) / 12.0
        x = rotate(x, i)
        y = rotate(y, i)
        num = sum([(x[i] - x_m) * (y[i] - y_m) for i in chromatic_scale])
        den = (sum([(xi - x_m) ** 2 for xi in x]) * sum([(yi - y_m) ** 2 for yi in y])) ** 0.5
        return num / den
    
    notes = [note for bar in song.elements for note in bar if type(note) is Note]
    profile_types = [major_profile, minor_profile]
    y = [sum(map(lambda n: n.duration.quarterLength, filter(lambda n: (n.pitch.ps % octave) == p, notes))) for p in chromatic_scale]
    coefficients = [coefficient(x, y, p) for x in profile_types for p in chromatic_scale]
    coefficients = [(note_names[i % octave], key_types[i / octave]) for (i,r) in enumerate(coefficients)]
    return sorted(coefficients, key=lambda r: r[1])[0]