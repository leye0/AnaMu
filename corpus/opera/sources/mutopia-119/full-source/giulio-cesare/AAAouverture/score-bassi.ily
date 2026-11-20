\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    piece = "Ouverture."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
