\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Tolomeo: L'empio, sleale, indegno"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
