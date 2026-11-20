\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "tutti2"
  >>
  \header {
    opus = "Duetto. Cleopatra e Cesare: Caro/Bella, più amabile beltà"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
