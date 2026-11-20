\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Cleopatra: Da tempeste il legno infranto"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
