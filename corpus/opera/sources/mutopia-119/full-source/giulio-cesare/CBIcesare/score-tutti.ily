\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "tutti"
  >>
  \header {
    opus = "Aria. Cesare: Se in fiorito"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
