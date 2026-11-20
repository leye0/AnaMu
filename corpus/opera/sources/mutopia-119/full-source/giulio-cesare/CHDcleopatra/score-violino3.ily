\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino3"
  >>
  \header {
    opus = "Aria. Cleopatra: Se pietà di me non senti"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
