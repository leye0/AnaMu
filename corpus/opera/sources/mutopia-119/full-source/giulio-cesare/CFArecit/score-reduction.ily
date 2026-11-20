%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \recitStaff <<
      \keepWithTag #'recit  \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena VI."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
