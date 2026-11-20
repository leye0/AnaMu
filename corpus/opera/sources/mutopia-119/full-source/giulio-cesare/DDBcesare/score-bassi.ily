\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cesare: Aure, deh, per pietà"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
