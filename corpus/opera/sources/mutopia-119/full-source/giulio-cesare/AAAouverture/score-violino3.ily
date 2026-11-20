\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef treble
    \includeNotes "violino3" 
  >>
  \header {
    piece = "Ouverture."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
