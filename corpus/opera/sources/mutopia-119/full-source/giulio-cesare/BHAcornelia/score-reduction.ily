%% Aria. Cornelia: Nel tuo seno, amico sasso
\score {
  <<
    \lyricStaff \markup "Cornelia." <<
      \keepWithTag #'partUp \global
      \cornelia \includeNotes "cornelia" 
    >> \includeLyrics "cornelia-lyrics" 
    \new PianoStaff <<
      \new Staff <<
        \keepWithTag #'() \global
        \clef treble
        \set Staff.printPartCombineTexts = ##f
        \partcombine \includeNotes "violino1" \includeNotes "violino2"
      >>
      \new Staff <<
        \keepWithTag #'() \global
        \clef bass
        \includeNotes "bassi"
      >>
    >>
  >>
  \header {
    piece = "Scena VIII."
    opus = "Aria. Cornelia: Nel tuo seno, amico sasso"
    breakbefore = #(break-before?)
  }
  \layout { }
}
