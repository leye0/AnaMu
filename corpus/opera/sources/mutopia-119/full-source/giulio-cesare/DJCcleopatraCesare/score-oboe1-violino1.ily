\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "tutti1"
    { s8 s1.*8 \break }
  >>
  \header {
    opus = "Duetto. Cleopatra e Cesare: Caro/Bella, più amabile beltà"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
