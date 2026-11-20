\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cesare: Se in fiorito"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
