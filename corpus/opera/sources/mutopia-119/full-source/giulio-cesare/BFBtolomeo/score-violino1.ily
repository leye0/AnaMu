\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \set Score.skipBars = ##t
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Tolomeo: L'empio, sleale, indegno"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
