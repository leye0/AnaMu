\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Tolomeo: Domerò la tua fierezza"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
