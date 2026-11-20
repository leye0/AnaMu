\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    piece = "Scena VII."
    opus = "Aria. Cesare: Alma del gran Pompeo"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}