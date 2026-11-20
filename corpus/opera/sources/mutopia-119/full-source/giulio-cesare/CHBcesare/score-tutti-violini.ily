\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(full partBoth) \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Cesare: Al lampo dell'armi"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
