\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassons-part"
  >>
  \header {
    opus = "Aria. Cesare: Se in fiorito"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
