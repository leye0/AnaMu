\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    piece = "Scena VIII."
    opus = "Aria. Cornelia: Nel tuo seno, amico sasso"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
