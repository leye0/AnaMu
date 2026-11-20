\score {
  \instrStaff \markup "" <<
    \set Score.skipBars = ##t
    \keepWithTag #'partBoth \global
    \clef alto
    \includeNotes "viola" 
  >>
  \header {
    opus = "Aria. Tolomeo: L'empio, sleale, indegno"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
