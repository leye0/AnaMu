\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    opus = "Sinfonia."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
