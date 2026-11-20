%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Cleopatra. <<
      \keepWithTag #'up  \global
      \cleopatra \includeNotes "cleopatra"
    >> \includeLyrics "cleopatra-lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena VII."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { }
}
