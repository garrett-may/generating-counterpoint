% Lily was here -- automatically converted by /usr/bin/midi2ly from 018-Field01.mid
\version "2.14.0"

\layout {
  \context {
    \Voice
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver"
    \remove "Rest_engraver"
    \consists "Completion_rest_engraver"
  }
}

trackAchannelA = {
  
  \set Staff.instrumentName = "Clipping"
  
  \time 1/4 
  
  \tempo 4 = 120 
  \skip 4 
  | % 2
  
  \time 4/4 
  
}

trackA = <<
  \context Voice = voiceA \trackAchannelA
>>


trackBchannelA = {
  
  \set Staff.instrumentName = "flute"
  
}

trackBchannelB = \relative c {
  r1*22 c'''4 g'4*640/480 f4*160/480 dis d4*320/480 dis f ais,4 
  c g4*640/480 r4*160/480 dis f4*640/480 dis4*160/480 f g4 
  | % 26
  b d c g4*880/480 r4*80/480 g'4*640/480 f4*160/480 dis d4*320/480 
  dis f ais,4 c g4*320/480 r4*160/480 
  | % 29
  <ais d >4 <dis c >4*1280/480 r4*160/480 
  | % 30
  <dis c >4*160/480 <ais d >4*160/480 <dis c >4*160/480 <f d >4*800/480 
  r4*160/480 <ais, d >4 
  | % 31
  <ais f >4 <c g >4*7 
}

trackB = <<
  \context Voice = voiceA \trackBchannelA
  \context Voice = voiceB \trackBchannelB
>>


trackCchannelA = {
  
  \set Staff.instrumentName = "bone"
  
}

trackCchannelB = \relative c {
  r4*9 <ais' d >4*560/480 r4*80/480 <c a >4*80/480 r4*80/480 <ais d >4*80/480 
  r4*80/480 <c a >4*560/480 r4*80/480 <ais g >4*80/480 r4*80/480 <c a >4*80/480 
  r4*80/480 <ais g >4*560/480 r4*80/480 <f a >4*80/480 r4*80/480 <ais g >4*80/480 
  r4*80/480 <f a >4*880/480 r4*3920/480 <g dis >4*560/480 r4*80/480 <f d >4*80/480 
  r4*80/480 <dis g >4*80/480 r4*80/480 <f a >4*560/480 r4*80/480 <g dis >4*80/480 
  r4*80/480 <a f >4*80/480 r4*80/480 <ais g >4*560/480 r4*80/480 <f a >4*80/480 
  r4*80/480 <ais g >4*80/480 r4*80/480 <a f >4*880/480 r4*3920/480 <ais d >4*560/480 
  r4*80/480 <gis c >4*80/480 r4*80/480 <ais d >4*80/480 r4*80/480 <gis c >4*560/480 
  r4*80/480 <ais g >4*80/480 r4*80/480 <c gis >4*80/480 r4*80/480 <ais g >4*560/480 
  r4*80/480 <f gis >4*80/480 r4*80/480 <ais g >4*80/480 r4*80/480 <f gis >4*880/480 
  r4*3920/480 <g dis >4*560/480 r4*80/480 <f d >4*80/480 r4*80/480 <dis g >4*80/480 
  r4*80/480 <f gis >4*560/480 r4*80/480 <g dis >4*80/480 r4*80/480 <f gis >4*80/480 
  r4*80/480 <ais g >4*560/480 r4*80/480 <f gis >4*80/480 r4*80/480 <ais g >4*80/480 
  r4*80/480 <c gis >4*880/480 
}

trackC = <<

  \clef bass
  
  \context Voice = voiceA \trackCchannelA
  \context Voice = voiceB \trackCchannelB
>>


trackDchannelA = {
  
  \set Staff.instrumentName = "tuba"
  
}

trackDchannelB = \relative c {
  r4 c,4*3200/480 r4*160/480 
  | % 3
  g'4*320/480 r4*160/480 c,4*3200/480 r4*160/480 
  | % 5
  g'4*320/480 r4*160/480 c,4*3200/480 r4*160/480 
  | % 7
  g'4*320/480 r4*160/480 c,4*3200/480 r4*160/480 
  | % 9
  g'4*320/480 r4*160/480 gis4*3200/480 r4*160/480 
  | % 11
  dis4*320/480 r4*160/480 gis4*3200/480 r4*160/480 
  | % 13
  dis4*320/480 r4*160/480 gis4*3200/480 r4*160/480 
  | % 15
  dis4*320/480 r4*160/480 gis4*3200/480 r4*160/480 
  | % 17
  g4*320/480 r4*160/480 f4*1760/480 r4*160/480 cis4*1760/480 
  r4*160/480 c4*1760/480 r4*160/480 ais4*800/480 r4*160/480 ais'4*320/480 
  r4*160/480 
  | % 21
  gis4*320/480 r4*160/480 g4*3280/480 r4*80/480 
  | % 23
  g,4 gis16*15 r16 g16*7 r16 c16*7 r16 f16*7 r16 g16*7 r16 c,16*7 
  r16 ais16*7 r16 gis16*15 r16 g16*7 r16 c16*7 r16 gis16*15 r16 ais16*15 
  r16 c8*15 
}

trackD = <<

  \clef bass
  
  \context Voice = voiceA \trackDchannelA
  \context Voice = voiceB \trackDchannelB
>>


trackEchannelA = {
  
  \set Staff.instrumentName = "strings"
  
}

trackEchannelB = {
  
  \set Staff.instrumentName = "strings"
  
}

trackEchannelC = \relative c {
  \voiceThree
  r4 <c'' c, >4*640/480 <d, d' >4*160/480 <dis dis' >4*160/480 
  <f f' >4 
  | % 2
  <g g' >4 <d' d' >2 <c c' >4 
  | % 3
  <d d' >4 <g g, >4*3680/480 r4*160/480 <c,, c' >4*640/480 <d d' >4*160/480 
  <dis dis' >4*160/480 <f f' >4 
  | % 6
  <g g' >4 <d d' >2 <dis dis' >4 
  | % 7
  <f f' >4 <ais ais' >4*7 r4 <c c, >4*640/480 <d, d' >4*160/480 
  <dis dis' >4*160/480 <f f' >4 
  | % 10
  <g g' >4 <d' d' >2 <c c' >4 
  | % 11
  <d d' >4 <g g, >4*3680/480 r4*160/480 <c,, c' >4*640/480 <d d' >4*160/480 
  <dis dis' >4*160/480 <f f' >4 
  | % 14
  <g g' >4 <d d' >2 <dis dis' >4 
  | % 15
  <f f' >4 <ais ais' >4*7 r4 <c, c' >4*640/480 <d d' >4*160/480 
  <dis dis' >4*160/480 <f f' >4 
  | % 18
  <g g' >4 <c c' >2 <ais ais' >4 
  | % 19
  <gis gis' >4 <g g' >4*640/480 <gis gis' >4*160/480 <g g' >4*160/480 
  <dis dis' >4 
  | % 20
  <g g' >4 <f f' >4 <cis cis' >4 <dis dis' >4 
  | % 21
  <f f' >4 <g' g, >4*3040/480 r4*800/480 <c gis >1 d2 dis c b 
  c ais d,4 c2 
  | % 28
  dis4 f g e 
  | % 29
  c <c' gis >1 <ais f >1 <c f, >1 <c g >1 
}

trackEchannelCvoiceB = \relative c {
  \voiceOne
  r4*93 g'''1 f dis gis ais2 c 
}

trackEchannelD = \relative c {
  \voiceFour
  r4 <c, c' >4*3200/480 r4*160/480 
  | % 3
  <g' g' >4*320/480 r4*160/480 <c, c' >4*3200/480 r4*160/480 
  | % 5
  <g' g' >4*320/480 r4*160/480 <c, c' >4*3200/480 r4*160/480 
  | % 7
  <g' g' >4*320/480 r4*160/480 <c, c' >4*3200/480 r4*160/480 
  | % 9
  <g' g' >4*320/480 r4*160/480 <gis gis' >4*3200/480 r4*160/480 
  | % 11
  <dis dis' >4*320/480 r4*160/480 <gis gis' >4*3200/480 r4*160/480 
  | % 13
  <dis dis' >4*320/480 r4*160/480 <gis gis' >4*3200/480 r4*160/480 
  | % 15
  <dis dis' >4*320/480 r4*160/480 <gis gis' >4*3200/480 r4*160/480 
  | % 17
  <g g' >4*320/480 r4*160/480 <f f' >4*1760/480 r4*160/480 <cis cis' >4*1760/480 
  r4*160/480 <c c' >4*1760/480 r4*160/480 <ais ais' >4*800/480 
  r4*160/480 <ais' ais' >4*320/480 r4*160/480 
  | % 21
  <gis gis' >4*320/480 r4*160/480 <g g' >4*7 <g g, >4 <gis, gis' >1 
  <g g' >2 <c c' >2 <f, f' >2 <g g' >2 <c c' >2 <ais ais' >2 <gis gis' >1 
  <g g' >2 <c' c, >2 <gis, gis' >1 <ais ais' >1 <c c' >8*15 
}

trackE = <<
  \context Voice = voiceA \trackEchannelA
  \context Voice = voiceB \trackEchannelB
  \context Voice = voiceC \trackEchannelC
  \context Voice = voiceD \trackEchannelCvoiceB
  \context Voice = voiceE \trackEchannelD
>>


trackFchannelA = {
  
  \set Staff.instrumentName = "horn"
  
}

trackFchannelB = \relative c {
  r4 <g' c dis >4*800/480 r4*160/480 <a d f >4*800/480 r4*160/480 <ais g' dis >4*800/480 
  r4*160/480 <a d f >4*800/480 r4*160/480 <g c dis >4*800/480 r4*160/480 <a d f >4*800/480 
  r4*160/480 <ais g' dis >4*800/480 r4*160/480 <a d f >4*800/480 
  r4*160/480 <g c dis >4*800/480 r4*160/480 <a d f >4*800/480 r4*160/480 <ais g' dis >4*800/480 
  r4*160/480 <a d f >4*800/480 r4*160/480 <g c dis >4*800/480 r4*160/480 <a d f >4*800/480 
  r4*160/480 <ais g' dis >4*800/480 r4*160/480 <a d f >4*800/480 
  r4*160/480 <dis c gis >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis g c, >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis c gis >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis g c, >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis c gis >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis g c, >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis c gis >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <dis g c, >4*800/480 r4*160/480 <f d ais >4*800/480 
  r4*160/480 <gis, dis' c >4*1760/480 r4*160/480 <f' gis, c >4*1760/480 
  r4*160/480 <g, dis' ais >4*1760/480 r4*160/480 <f' gis, cis >4*800/480 
  r4*160/480 <f gis, cis >4*800/480 r4*160/480 <c f d >4*560/480 
  r4*80/480 <c f d >4*80/480 r4*80/480 <c f d >4*80/480 r4*80/480 <c f d >4*560/480 
  r4*80/480 <c f d >4*80/480 r4*80/480 <c f d >4*80/480 r4*80/480 <d g b, >4*1280/480 
  r4*7840/480 c4*400/480 r4*80/480 g'4*560/480 r4*80/480 f r4*80/480 dis 
  r4*80/480 d8 r4*80/480 dis8 r4*80/480 f8 r4*80/480 ais,8. r16 c8. 
  r16 g8. r16 
  | % 29
  <d' ais >8. r16 <dis gis, c >16*15 r16 <f d ais >16*15 r16 <f ais, d >16*7 
  r16 <d g, ais >8 r4*80/480 <f ais, d >8 r4*80/480 <d g, ais >8 
  r4*80/480 <e g, c >16*15 
}

trackF = <<
  \context Voice = voiceA \trackFchannelA
  \context Voice = voiceB \trackFchannelB
>>


trackGchannelA = {
  
  \set Staff.instrumentName = "harp"
  
}

trackGchannelB = \relative c {
  r4 ais'4*160/480 dis g ais dis g ais r4*2720/480 ais,,4*160/480 
  dis g ais dis g ais r4*2720/480 ais,,4*160/480 dis g ais dis 
  g ais r4*2720/480 ais,,4*160/480 dis g ais dis g ais r4*2720/480 c,,4*160/480 
  dis g c dis g ais r4*2720/480 c,,4*160/480 dis g c dis g ais 
  r4*2720/480 c,,4*160/480 dis g c dis g ais r4*2720/480 c,,4*160/480 
  dis g c dis g ais r4*2720/480 c,,4*160/480 dis gis c dis gis 
  c r4*800/480 c,,4*160/480 f gis c f gis c gis f 
  | % 19
  c gis f ais, dis g ais dis g ais r4*800/480 cis,,4*160/480 
  f gis cis f gis cis gis f 
  | % 21
  cis gis f c d g c d g c g d 
  | % 22
  c g d b d g b d g b g d 
  | % 23
  b g d gis, c dis gis c dis gis dis c 
  | % 24
  gis dis c g ais d g ais d g,, c dis 
  | % 25
  g c dis gis,, c f gis c f g,, b d 
  | % 26
  g b d g,, c dis g c dis g,, ais d 
  | % 27
  g ais d gis,, c dis gis c dis gis dis c 
  | % 28
  gis dis c g ais d g ais d g,, c e 
  | % 29
  g c e gis,, c dis gis c dis gis dis c 
  | % 30
  gis dis c ais d f ais d f ais f d 
  | % 31
  ais f d g, ais d g ais d g d ais 
  | % 32
  g d ais g c e g c e g e c 
  | % 33
  g e c 
}

trackG = <<
  \context Voice = voiceA \trackGchannelA
  \context Voice = voiceB \trackGchannelB
>>


trackHchannelA = {
  
  \set Staff.instrumentName = "timpani"
  
}

trackHchannelB = \relative c {
  r4 c4*640/480 c4*160/480 c c2 r2. 
  | % 3
  g4 c4*640/480 c4*160/480 c c2 r2. 
  | % 5
  g4 c4*640/480 c4*160/480 c c2 r2. 
  | % 7
  g4 c4*640/480 c4*160/480 c c2 r2. 
  | % 9
  g4 gis4*640/480 gis4*160/480 gis gis2 r2. 
  | % 11
  dis'4 gis,4*640/480 gis4*160/480 gis gis2 r2. 
  | % 13
  dis'4 gis,4*640/480 gis4*160/480 gis gis2 r2. 
  | % 15
  dis'4 gis,4*640/480 gis4*160/480 gis gis2 r2. 
  | % 17
  g4 f2 r1. c'2 r1 ais4 
  | % 21
  gis g2 r4*640/480 g4*160/480 g g2 r4*8320/480 ais4*160/480 
  ais gis2 r2 g c gis r2 ais r2 c c4 
  | % 32
  g c2 
}

trackH = <<

  \clef bass
  
  \context Voice = voiceA \trackHchannelA
  \context Voice = voiceB \trackHchannelB
>>


trackIchannelA = {
  
  \set Staff.instrumentName = "drum"
  
}

trackIchannelB = \relative c {
  \voiceOne
  r4*1280/480 d,4*80/480 d <d c >4*160/480 r4*3520/480 d4*80/480 
  d <d c >4*160/480 r4*3520/480 d4*80/480 d <d c >4*160/480 r4*3520/480 d4*80/480 
  d <d c >4*160/480 r4*3520/480 d4*80/480 d <d c >4*160/480 r4*3520/480 d4*80/480 
  d <d c >4*160/480 r4*3520/480 d4*80/480 d <d c >4*160/480 r4*3520/480 d4*80/480 
  d <d c >4*160/480 r4*3520/480 d4*80/480 d <d c >4*160/480 r4*3520/480 d4*80/480 
  d <d c >4*160/480 r4*2720/480 a''16 a a a a a a a a a a a 
  | % 22
  a a a a <c,, b'' >4*160/480 r4*10240/480 d4*80/480 d <d c >4*160/480 
  r4*3520/480 d4*80/480 d <d c >4*160/480 r4*2720/480 a''16 a a 
  a a a a a a a a a 
  | % 32
  a a a a <c,, b'' >4*160/480 
}

trackIchannelBvoiceB = \relative c {
  \voiceTwo
  r4*39680/480 d,4*80/480 d <c d >4*160/480 r4*18880/480 d4*80/480 
  d <c d >4*160/480 
}

trackI = <<

  \clef bass
  
  \context Voice = voiceA \trackIchannelA
  \context Voice = voiceB \trackIchannelB
  \context Voice = voiceC \trackIchannelBvoiceB
>>


trackJchannelA = {
  
  \set Staff.instrumentName = "flute"
  
}

trackJchannelB = \relative c {
  r4*42560/480 c'''4 g'4*640/480 f4*160/480 dis d4*320/480 dis 
  f ais,4 c g4*640/480 r4*160/480 dis f4*640/480 dis4*160/480 f 
  g4 b d c g4*880/480 r4*80/480 g'4*640/480 f4*160/480 dis d4*320/480 
  dis f ais,4 c g4*320/480 r4*160/480 <ais d >4 <dis c >4*1280/480 
  r4*160/480 <dis c >4*160/480 <ais d >4*160/480 <dis c >4*160/480 
  <f d >4*800/480 r4*160/480 <ais, d >4 <ais f >4 <c g >4*7 
}

trackJ = <<
  \context Voice = voiceA \trackJchannelA
  \context Voice = voiceB \trackJchannelB
>>


\score {
  <<
    \context Staff=trackB \trackA
    \context Staff=trackB \trackB
    \context Staff=trackC \trackA
    \context Staff=trackC \trackC
    \context Staff=trackD \trackA
    \context Staff=trackD \trackD
    \context Staff=trackE \trackA
    \context Staff=trackE \trackE
    \context Staff=trackF \trackA
    \context Staff=trackF \trackF
    \context Staff=trackG \trackA
    \context Staff=trackG \trackG
    \context Staff=trackH \trackA
    \context Staff=trackH \trackH
    \context Staff=trackI \trackA
    \context Staff=trackI \trackI
    \context Staff=trackJ \trackA
    \context Staff=trackJ \trackJ
  >>
  \layout {}
  \midi {}
}
