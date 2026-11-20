\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: Da tempeste il legno infranto"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
