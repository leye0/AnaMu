\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Sinfonia."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
