\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Cleopatra: Venere bella"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
