\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "tutti"
  >>
  \header {
    opus = "Aria. Cornelia: Non ha più che temere"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
