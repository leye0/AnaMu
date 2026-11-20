\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    piece = "Scena VII."
    opus = "Aria. Cesare: Alma del gran Pompeo"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}