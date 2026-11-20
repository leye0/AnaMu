\score {
  \instrStaff \markup "" <<
    \set Score.skipBars = ##t
    \keepWithTag #'partBoth \global
    \clef alto
    \includeNotes "viola"
  >>
  \header {
    opus = "Aria. Cleopatra: Tutto può donna Vezzosa, s'amorosa"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}