import sys
import abjad
from abjad import *
from abjad.tools import lilypondparsertools
from music21 import *
import music21 as m

#environment.set('musicxmlPath', '/mnt/c/Users/garrett-may/Desktop/music_test')
#environment.set('midiPath', '/mnt/c/Users/garrett-may/Desktop/music_test')

filename = "denemoTest.mid"  #sys.argv[1]

song = m.converter.parse(filename)
for part in song:
	for item in part:
		if(type(item) == note.Note):
			print(str(item.name) + " | " + str(item.octave) + " | " + str(item.duration.type))
			#item.pitch = item.pitch.transpose('m3')

key = song.analyze('Krumhansl')
print(key.tonic.name, key.mode)
			
lpc = lily.translate.LilypondConverter()
lpMusicList = lily.lilyObjects.LyMusicList()
lpc.context = lpMusicList
lpc.appendObjectsToContextFromStream(song)
print(lpc.context)

with open('denemoFinal.ly', 'w') as file:
	file.write(str(lpc.context))
#song.show('midi')
		


#with open(filename, "r") as file:	
	#lines = file.readlines()	
	#lines = [line.replace('\n', '').replace('\r', '') for line in lines]
	#for line in lines:
	#	print(line)
	#str = ''.join(lines)
	#parser = abjad.lilypondparsertools.LilyPondParser('nederlands')
	#parser = abjad.lilypondparsertools.LilyPondParser('nederlands')
	#container = parser(str)
	#print(container)
	#abjad.show(container) 
	#container = lilypondparsertools.parse_reduced_ly_syntax(str)
	#print(container)