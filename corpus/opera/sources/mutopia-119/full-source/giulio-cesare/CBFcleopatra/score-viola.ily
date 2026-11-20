\score {
  \new StaffGroup <<
    \instrStaff \markup {Viola.} <<
      \set Score.skipBars = ##t
      \keepWithTag #'partUp \global
      \clef alto
      \includeNotes "viola"
    >>
    \instrStaff \markup \instruments { Viola (Orchestra) } <<
      \keepWithTag #'partDown \global
      \clef alto
      \includeNotes "orch-viola"
    >>
  >>
  \header { opus = "Aria. Cleopatra: V'adoro, pupile"
            breakbefore = #(break-before?) }
  \layout {}
}
