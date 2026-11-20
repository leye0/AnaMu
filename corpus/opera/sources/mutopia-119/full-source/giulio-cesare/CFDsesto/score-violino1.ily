\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Sesto: Cara speme, questo core tu cominci a lusingar"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
