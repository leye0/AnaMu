\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Cesare: Va tacito e nascosto, quand' avido"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
