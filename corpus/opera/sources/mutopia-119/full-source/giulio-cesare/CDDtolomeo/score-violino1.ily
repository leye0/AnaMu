\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Tolomeo: Sì, spietata, il tuo rigore"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
