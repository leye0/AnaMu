\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
    \includeFigures "figures"
  >>
  \header {
    opus = "Aria. Sesto: La giustizia ha già sull'arco"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
