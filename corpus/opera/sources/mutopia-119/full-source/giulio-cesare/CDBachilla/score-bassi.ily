\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Achilla: Se a me non sei crudele"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
