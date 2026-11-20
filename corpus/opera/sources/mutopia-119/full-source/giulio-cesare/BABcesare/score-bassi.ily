\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cesare: Presti omai l'egizia terra"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
