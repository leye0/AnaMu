\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(not-corno partBoth) \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    piece = "Scena Ultima."
    opus = "Sinfonia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
