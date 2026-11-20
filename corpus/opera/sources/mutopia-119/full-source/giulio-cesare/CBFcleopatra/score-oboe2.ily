%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Oboe." <<
      \keepWithTag #'(partUp tutti) \global
      \clef treble
      \includeNotes "tutti"
    >>
    \instrStaff \markup \instruments { "Oboe II." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-violino2"
    >>
  >>
  \header { opus = "Aria. Cleopatra: V'adoro, pupile"
            breakbefore = #(break-before?) }
  \layout {}
}
