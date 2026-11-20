\score {
  \instrStaff \markup "" <<
    \keepWithTag #'up \global
    \clef alto
    \includeNotes "viola" 
  >>
  \header {
    piece = "Scena VII."
    opus = "Aria. Cesare: Alma del gran Pompeo"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}