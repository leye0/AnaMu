\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef alto
    \set Score.skipBars = ##t
    \includeNotes "viola"
  >>
  \header {
    opus = "Aria. Cesare: Non è si vago e bello"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
