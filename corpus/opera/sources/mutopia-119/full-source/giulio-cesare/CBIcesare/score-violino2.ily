\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    opus = "Aria. Cesare: Se in fiorito"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
