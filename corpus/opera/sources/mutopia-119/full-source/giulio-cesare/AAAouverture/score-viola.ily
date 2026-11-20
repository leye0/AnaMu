\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef alto
    \includeNotes "alto"
  >>
  \header {
    piece = "Ouverture."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
