%% Aria. Cornelia: Nel tuo seno, amico sasso
\score {
  \new OrchestraStaffGroup <<
    \new InstrumentStaffGroup <<
      \instrStaff \markup "(Violino I.)" <<
        \keepWithTag #'up \global
        \clef treble \includeNotes #"violino1"
      >>
      \instrStaff \markup "(Violino II.)" <<
        \keepWithTag #'() \global
        \clef treble \includeNotes #"violino2"
      >>
      \lyricStaff \markup "Cornelia." <<
        \keepWithTag #'() \global
        \cornelia \includeNotes #"cornelia" 
        >> \includeLyrics #"cornelia-lyrics" 
    >>
    \instrStaff \markup "(Bassi.)" <<
      \scoreInit
      \keepWithTag #'() \global
      \clef bass \includeNotes #"bassi"
    >>
  >>
  
  \header {
    scene = "SCENA VIII."
    scenedescr = \markup \center-align {
      \line { \smallCaps Cornelia, e poi \smallCaps Nireno che sopraviene; }
      \line { \smallCaps Cleopatra e \smallCaps Nireno in disparte. } }
    breakbefore = #(break-before?) 
  }
  \layout { #(define tweak-key (*current-piece*)) }
  \midi { \tempo 4 = 44 }
}
