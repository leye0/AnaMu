\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(not-corno partBoth) \global
    \clef treble
    \includeNotes "oboe2"
  >>
  \header {
    piece = "Scena Ultima."
    opus = "Sinfonia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
