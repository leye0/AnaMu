\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino12"
  >>
  \header {
    opus = "Aria. Cleopatra: Se pietà di me non senti"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
