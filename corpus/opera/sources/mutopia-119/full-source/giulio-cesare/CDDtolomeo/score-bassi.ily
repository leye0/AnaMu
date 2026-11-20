\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Tolomeo: Sì, spietata, il tuo rigore"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
