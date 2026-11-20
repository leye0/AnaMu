%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Oboe." <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "tutti"
    >>
    \instrStaff \markup \instruments { "Oboe I." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-tutti1"
    >>
  >>
  \layout {}
}