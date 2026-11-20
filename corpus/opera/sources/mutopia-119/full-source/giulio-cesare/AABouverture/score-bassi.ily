\score {
  \instrStaff \markup "" <<
    \keepWithTag #'up \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    breakbefore = #(break-before?) 
  }
  \layout { indent = \noindent }
}
