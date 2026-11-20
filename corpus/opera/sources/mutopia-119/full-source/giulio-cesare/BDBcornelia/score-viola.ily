\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef alto
    \includeNotes "viola" 
  >>
  \header {
    opus = "Aria. Cornelia: Priva son d'ogni conforto"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}