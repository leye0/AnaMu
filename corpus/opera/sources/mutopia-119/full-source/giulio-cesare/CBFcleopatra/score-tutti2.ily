%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup {Violino II.} <<
      \keepWithTag #'(partUp) \global
      \clef treble
      \includeNotes "violino2"
    >>
    \instrStaff \markup \instruments { "Violino II." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-violino2"
    >>
  >>
  \header { opus = "Aria. Cleopatra: V'adoro, pupile"
            breakbefore = #(break-before?) }
  \layout {}
}
