\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1" 
  >>
  \header {
    opus = "Aria. Cornelia: Priva son d'ogni conforto"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}