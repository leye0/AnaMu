\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    {
      \includeNotes "violino1-1"
      R1*22
    }
  >>
  \header {
    opus = "Aria. Cleopatra: Piangerò la sorte mia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
