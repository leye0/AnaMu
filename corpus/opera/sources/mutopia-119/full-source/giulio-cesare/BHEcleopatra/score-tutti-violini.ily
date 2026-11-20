\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \set Score.skipBars = ##t
    \includeNotes "violini"
  >>
  \header {
    opus = "Aria. Cleopatra: Tu la mia stella sei, amabile speranza"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}