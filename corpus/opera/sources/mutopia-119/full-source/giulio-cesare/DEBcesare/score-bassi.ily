\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cesare: Quel torrente che cade dal monte"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
