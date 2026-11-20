\score {
  \instrStaff \markup "Corno in F." <<
    \keepWithTag #'(corno partBoth) \global
    \clef treble
    \includeNotes "corno"
  >>
  \header {
    opus = "Aria. Cesare: Va tacito e nascosto, quand' avido"
    breakbefore = #(break-before?)
  }
  \layout { }
}
