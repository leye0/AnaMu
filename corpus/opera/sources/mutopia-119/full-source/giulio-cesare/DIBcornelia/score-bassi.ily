\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cornelia: Non ha più che temere"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
