\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    piece = "Scena VII."
    opus = "Recit. Cleopatra: Voi, che mie fide ancelle"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
