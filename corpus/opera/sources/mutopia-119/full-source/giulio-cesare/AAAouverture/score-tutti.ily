\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef treble
    \includeNotes "tutti" 
  >>
  \header {
    piece = "Ouverture."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
