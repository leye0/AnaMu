\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cornelia: Priva son d'ogni conforto"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
