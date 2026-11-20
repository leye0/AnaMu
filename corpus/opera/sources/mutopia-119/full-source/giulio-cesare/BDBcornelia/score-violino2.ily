\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2" 
  >>
  \header {
    opus = "Aria. Cornelia: Priva son d'ogni conforto"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}