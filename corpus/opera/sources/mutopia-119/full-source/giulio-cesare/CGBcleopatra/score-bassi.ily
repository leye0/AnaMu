\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: Venere bella"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
