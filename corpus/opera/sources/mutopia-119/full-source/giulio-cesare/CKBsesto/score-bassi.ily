\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Sesto: L'aura che spira"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
