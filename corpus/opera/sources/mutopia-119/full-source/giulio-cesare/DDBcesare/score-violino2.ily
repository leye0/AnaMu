\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    opus = "Aria. Cesare: Aure, deh, per pietà"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
