\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassons-part"
  >>
  \header {
    opus = "Aria. Cleopatra: Se pietà di me non senti"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
