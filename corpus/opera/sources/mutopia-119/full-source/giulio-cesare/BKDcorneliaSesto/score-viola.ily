\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef alto
    \includeNotes "viola"
  >>
  \header {
    opus = "Aria. Sesto e Cornelia: Son nato a sospirar/Son nata a lagrimar, e il dolce"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}

