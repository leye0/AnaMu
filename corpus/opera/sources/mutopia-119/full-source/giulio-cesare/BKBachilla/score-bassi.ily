\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \keepWithTag #'no-basson \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Achilla: Tu sei il cor di questo core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
