%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Violino I." <<
      \keepWithTag #'(partUp tutti) \global
      \clef treble
      \includeNotes "tutti"
    >>
    \instrStaff \markup \instruments { "Violino I." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-violino1"
    >>
  >>
  \header { opus = "Aria. Cleopatra: V'adoro, pupile"
            breakbefore = #(break-before?) }
  \layout {}
}
