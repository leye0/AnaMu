\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Sesto e Cornelia: Son nato a sospirar/Son nata a lagrimar, e il dolce"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
