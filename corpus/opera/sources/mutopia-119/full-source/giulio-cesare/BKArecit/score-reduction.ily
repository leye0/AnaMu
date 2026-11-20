%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \recitStaff <<
      \keepWithTag #'recit \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'() \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena XI."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
