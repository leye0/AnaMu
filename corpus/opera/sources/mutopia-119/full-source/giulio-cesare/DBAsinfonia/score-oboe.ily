\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "oboe"
  >>
  \header {
    piece = "Scena II."
    opus = "Sinfonia."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
