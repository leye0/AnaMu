\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Tolomeo: Domerò la tua fierezza"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
