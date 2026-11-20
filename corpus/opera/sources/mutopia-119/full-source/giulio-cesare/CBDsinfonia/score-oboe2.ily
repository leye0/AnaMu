%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Oboe." <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "tutti"
    >>
    \instrStaff \markup \instruments { "Oboe II." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-tutti2"
    >>
  >>
  \layout {}
}