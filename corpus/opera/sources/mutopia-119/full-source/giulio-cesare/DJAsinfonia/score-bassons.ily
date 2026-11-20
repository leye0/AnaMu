\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(not-corno partBoth) \global
    \clef bass
    \includeNotes "bassons"
  >>
  \header {
    piece = "Scena Ultima."
    opus = "Sinfonia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
