\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: Tu la mia stella sei, amabile speranza"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
