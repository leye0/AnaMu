\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(bassi partBoth) \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: Non disperar, chi sa ?"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
