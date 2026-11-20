\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "tutti"
  >>
  \header {
    opus = "Aria. Cesare: Quel torrente che cade dal monte"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
