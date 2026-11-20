\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Sesto: Cara speme, questo core tu cominci a lusingar"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
