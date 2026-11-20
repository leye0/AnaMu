%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup {Viola.} <<
      \keepWithTag #'() \global
      \clef alto
      \includeNotes "viola"
    >>
    \instrStaff \markup \instruments { Viola (Orchestra) } <<
      \keepWithTag #'() \global
      \clef alto
      \includeNotes "orch-viola"
    >>
  >>
  \layout {}
}