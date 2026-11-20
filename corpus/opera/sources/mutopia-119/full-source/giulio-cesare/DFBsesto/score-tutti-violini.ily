\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Sesto: La giustizia ha già sull'arco"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
