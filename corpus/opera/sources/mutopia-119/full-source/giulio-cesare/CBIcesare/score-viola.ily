\score {
  \instrStaff \markup "" <<
    \set Score.skipBars = ##t
    \keepWithTag #'partBoth \global
    \clef alto
    \includeNotes "viola"
  >>
  \header { opus = "Aria. Cesare: Se in fiorito"
            breakbefore = #(break-before?) }
  \layout { indent = \smallindent }
}
