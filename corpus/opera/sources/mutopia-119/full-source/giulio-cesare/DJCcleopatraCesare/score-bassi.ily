\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Duetto. Cleopatra e Cesare: Caro/Bella, più amabile beltà"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
