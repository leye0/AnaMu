\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    piece = "Scena VII."
    opus = "Recit. Cleopatra: Voi, che mie fide ancelle"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
