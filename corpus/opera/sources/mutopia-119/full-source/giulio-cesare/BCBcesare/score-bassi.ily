\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
    \includeFigures "figures"
  >>
  \header {
    opus = "Aria. Cesare: Empio, dirò, tu sei"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
