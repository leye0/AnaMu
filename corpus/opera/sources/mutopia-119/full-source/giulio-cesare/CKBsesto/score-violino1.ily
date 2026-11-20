\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Sesto: L'aura che spira"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
