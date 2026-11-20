\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    piece = "Scena VIII."
    opus = "Aria. Cornelia: Nel tuo seno, amico sasso"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
