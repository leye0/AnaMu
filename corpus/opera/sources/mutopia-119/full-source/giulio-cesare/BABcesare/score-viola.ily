\score {
  \instrStaff \markup "" <<
    \set Score.skipBars = ##t
    \keepWithTag #'partUp \global
    \clef alto
    \includeNotes "viola"
  >>
  \header {
    opus = "Aria. Cesare: Presti omai l'egizia terra"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}