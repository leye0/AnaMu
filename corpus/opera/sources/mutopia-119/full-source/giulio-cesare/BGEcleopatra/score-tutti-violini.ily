\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \set Score.skipBars = ##t
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Cleopatra: Tutto può donna Vezzosa, s'amorosa"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}