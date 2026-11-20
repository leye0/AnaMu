\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Achilla: Se a me non sei crudele"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
