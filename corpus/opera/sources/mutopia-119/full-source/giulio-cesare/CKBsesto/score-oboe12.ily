\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "oboe-part"
  >>
  \header {
    opus = "Aria. Sesto: L'aura che spira"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
