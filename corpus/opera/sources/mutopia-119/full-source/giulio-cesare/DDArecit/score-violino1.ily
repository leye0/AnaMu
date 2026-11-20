\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    piece = "Scena IV."
    opus = "Recit. Cesare: Dall' ondoso periglio salvo mi"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
