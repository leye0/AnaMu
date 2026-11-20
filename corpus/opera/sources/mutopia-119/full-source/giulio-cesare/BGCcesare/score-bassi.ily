\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
    \includeFigures "figures"
  >>
  \header {
    opus = "Aria. Cesare: Non è si vago e bello"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
