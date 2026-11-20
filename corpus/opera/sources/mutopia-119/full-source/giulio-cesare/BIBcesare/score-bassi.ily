\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(other partBoth) \global
    \clef bass
    \includeNotes "bassi"
    \includeFigures "figures"
  >>
  \header {
    opus = "Aria. Cesare: Va tacito e nascosto, quand' avido"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
