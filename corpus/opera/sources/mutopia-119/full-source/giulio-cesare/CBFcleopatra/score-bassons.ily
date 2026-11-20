\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: V'adoro, pupile"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
