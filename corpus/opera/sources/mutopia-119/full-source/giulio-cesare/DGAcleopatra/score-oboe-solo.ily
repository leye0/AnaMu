\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "oboe"
  >>
  \header {
    piece = "Scena VII."
    opus = "Recit. Cleopatra: Voi, che mie fide ancelle"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
