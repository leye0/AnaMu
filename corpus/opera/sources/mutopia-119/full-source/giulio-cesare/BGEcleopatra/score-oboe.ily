\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "oboe"
  >>
  \header {
    opus = "Aria. Cleopatra: Tutto può donna Vezzosa, s'amorosa"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}