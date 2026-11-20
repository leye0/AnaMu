\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassons-part"
  >>
  \header {
    opus = "Aria. Achilla: Tu sei il cor di questo core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
