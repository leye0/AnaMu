\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    piece = "Scena IV."
    opus = "Recit. Cesare: Dall' ondoso periglio salvo mi"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
