\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Achilla: Dal fulgor di questa spada"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
