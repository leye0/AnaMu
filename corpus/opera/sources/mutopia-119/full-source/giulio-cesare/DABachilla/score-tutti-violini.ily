\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Achilla: Dal fulgor di questa spada"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
