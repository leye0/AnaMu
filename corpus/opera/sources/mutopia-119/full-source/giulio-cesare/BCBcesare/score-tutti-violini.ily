\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \set Score.skipBars = ##t
    \includeNotes "tutti" 
  >>
  \header {
    opus = "Aria. Cesare: Empio, dirò, tu sei"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}